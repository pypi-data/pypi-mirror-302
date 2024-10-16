#
# Copyright (c) 2011, Canonical Ltd
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__all__ = [
    'PGBouncerFixture',
    ]

import itertools
import os.path
import signal
import socket
import subprocess
import time

from fixtures import Fixture, TempDir
import psycopg2
from testtools.content import content_from_file


def countdown(duration=60, sleep=0.1):
    """Provide a countdown iterator that sleeps between iterations.

    Yields the current iteration count, starting from 1.  The duration can be
    in fractional seconds.
    """
    start = time.time()
    stop = start + duration
    for iteration in itertools.count(1):
        now = time.time()
        if now < stop:
            yield iteration
            time.sleep(sleep)
        else:
            break


def _allocate_ports(n=1):
    """Allocate `n` unused ports.

    There is a small race condition here (between the time we allocate the
    port, and the time it actually gets used), but for the purposes for which
    this function gets used it isn't a problem in practice.
    """
    sockets = [socket.socket() for _ in range(n)]
    try:
        for s in sockets:
            s.bind(('localhost', 0))
        return [s.getsockname()[1] for s in sockets]
    finally:
        for s in sockets:
            s.close()


class PGBouncerFixture(Fixture):
    """Programmatically configure and run pgbouncer.

    Minimal usage:

      >>> bouncer = PGBouncerFixture()
      >>> bouncer.databases['mydb'] = 'host=hostname dbname=foo'
      >>> bouncer.users['user1'] = 'credentials'
      >>> with bouncer:
      ...     connection = psycopg2.connect(
      ...         database="mydb", host=bouncer.host, port=bouncer.port,
      ...         user="user1", password="credentials")

    """

    def __init__(self):
        super().__init__()
        # defaults
        # pgbouncer -> path to pgbouncer executable
        self.pgbouncer = 'pgbouncer'
        # dbname -> connect string
        self.databases = {}
        # username -> details
        self.users = {}
        # list of usernames that can run all console queries
        self.admin_users = []
        # list of usernames that can run readonly console queries
        self.stats_users = []
        self.pool_mode = 'session'
        self.unix_socket_dir = None
        self.process = None
        # Username and password that the fixture itself uses to run console
        # queries.  Since this fixture is only for testing, there's no harm
        # in hardcoding these.
        self.fixture_admin_username = '_pgbouncerfixture'
        self.fixture_admin_password = 'trusted'

    def setUp(self):
        super().setUp()
        self.addCleanup(self.stop)
        self.host = '127.0.0.1'
        self.port = _allocate_ports()[0]
        self.configdir = self.useFixture(TempDir())
        self.auth_type = 'trust'
        self.setUpConf()
        self.start()

    def setUpConf(self):
        """Create a pgbouncer.ini file."""
        self.inipath = os.path.join(self.configdir.path, 'pgbouncer.ini')
        self.authpath = os.path.join(self.configdir.path, 'users.txt')
        self.logpath = os.path.join(self.configdir.path, 'pgbouncer.log')
        self.pidpath = os.path.join(self.configdir.path, 'pgbouncer.pid')
        self.outputpath = os.path.join(self.configdir.path, 'output')
        with open(self.inipath, 'w') as inifile:
            inifile.write('[databases]\n')
            for item in self.databases.items():
                inifile.write('%s = %s\n' % item)
            inifile.write('[pgbouncer]\n')
            inifile.write('pool_mode = {}\n'.format(self.pool_mode))
            inifile.write('listen_port = {}\n'.format(self.port))
            inifile.write('listen_addr = {}\n'.format(self.host))
            if self.unix_socket_dir is not None:
                inifile.write(
                    'unix_socket_dir = {}\n'.format(self.unix_socket_dir))
            inifile.write('auth_type = {}\n'.format(self.auth_type))
            inifile.write('auth_file = {}\n'.format(self.authpath))
            inifile.write('logfile = {}\n'.format(self.logpath))
            inifile.write('pidfile = {}\n'.format(self.pidpath))
            adminusers = ','.join(
                [self.fixture_admin_username] + self.admin_users)
            inifile.write('admin_users = {}\n'.format(adminusers))
            statsusers = ','.join(self.stats_users)
            inifile.write('stats_users = {}\n'.format(statsusers))
        with open(self.authpath, 'w') as authfile:
            authfile.write(
                '"%s" "%s"\n' %
                (self.fixture_admin_username, self.fixture_admin_password))
            for user_creds in self.users.items():
                authfile.write('"%s" "%s"\n' % user_creds)

    @property
    def is_running(self):
        return (
            # pgbouncer has been started.
            self.process is not None and
            # pgbouncer has not yet exited.
            self.process.poll() is None)

    def get_pgbouncer_version(self):
        assert self.is_running
        with psycopg2.connect(
            host=self.host,
            port=self.port,
            database="pgbouncer",
            user=self.fixture_admin_username,
            password=self.fixture_admin_password,
        ) as con:
            return con.server_version

    def stop(self):
        if not self.is_running:
            return
        if self.get_pgbouncer_version() >= 12300:
            self.process.send_signal(signal.SIGQUIT)
        else:
            self.process.terminate()
        for iteration in countdown():
            if self.process.poll() is not None:
                break
        else:
            raise Exception(
                'Time-out waiting for pgbouncer to exit.')

    def start(self):
        if self.is_running:
            return
        # Add /usr/sbin if necessary to the PATH for magic just-works
        # behavior with Ubuntu.
        env = os.environ.copy()
        if not self.pgbouncer.startswith('/'):
            path = env['PATH'].split(os.pathsep)
            if '/usr/sbin' not in path:
                path.append('/usr/sbin')
                env['PATH'] = os.pathsep.join(path)

        with open(self.outputpath, "wb") as outputfile:
            with open(os.devnull, "rb") as devnull:
                self.process = subprocess.Popen(
                    [self.pgbouncer, self.inipath], env=env, stdin=devnull,
                    stdout=outputfile, stderr=outputfile)

        self.addDetail(
            os.path.basename(self.outputpath),
            content_from_file(self.outputpath))

        # Wait for the PID file to appear.
        for iteration in countdown():
            if os.path.isfile(self.pidpath):
                with open(self.pidpath, "rb") as pidfile:
                    if pidfile.read().strip().isdigit():
                        break
        else:
            raise Exception(
                'Time-out waiting for pgbouncer to create PID file.')
