# Sapy
# Copyright (C) 2018 stefano prina <stethewwolf@posteo.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from sapy.utils import loggers as LoggerFactory
import sapy.utils.db as db_iface
import sapy.utils.constants
from sapy.commands.command import Command
from sapy.core import loms
from sapy.core import moms
from sapy.core import tags
from sapy.core import profiles
from sapy.core import objectives as objs
import os
import sqlite3


class SetEnv(Command):
    short_arg = None
    long_arg = None
    cmd_help = None
    cmd_type = None
    cmd_action = None

    def __init__(self, param=None):
        super().__init__()
        self.logger = LoggerFactory.getLogger(str(self.__class__))

    def run(self):
        if 'SAPY_HOME' in os.environ:
            sapy_home_dir = os.environ['SAPY_HOME']
        else:
            # no value stored on env for SAPY_HOME,
            # setting default to ~/.sapy
            sapy_home_dir = os.path.join(
                os.environ['HOME'], sapy.utils.constants.__sapy_home__)
        
        sapy_db_file = os.path.join(
            sapy_home_dir, sapy.utils.constants.__db_file_name__)
        sapy_conf_file = os.path.join(
            sapy_home_dir, sapy.utils.constants.__conf_file_name__)
        
        # check if sapy_home exists, if no, create it
        if not os.path.exists(sapy_home_dir):
            os.makedirs(sapy_home_dir)
            self.logger.debug("created app home dir")
        else:
            self.logger.debug("app home dir yet present")
        
        # check if sapy conf file exists, if yes load confs
        if os.path.exists(sapy_conf_file):
            self.cfg.load(sapy_conf_file)
        
        # check if db file exists, if not create it
        populate_db_file = False
        if not os.path.exists(sapy_db_file):
            populate_db_file = True
            
        db_iface.open(sapy_db_file)
        
        if populate_db_file:
            cur = db_iface.get_cursor()
            cur.execute(sapy.utils.constants.__db_create_app_meta__)
            db_iface.commit()
            cur.close()
            moms.create_tables()
            loms.create_tables()
            tags.create_tables()
            objs.create_tables()
            profiles.create_tables()



