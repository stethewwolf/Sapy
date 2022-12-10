# Sapy
# Copyright (C) 2018 stefano prina <stefano-prina@outlook.it> <stethewwolf@gmail.com>
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

from sapy_modules.utils import loggers as LoggerFactory
from sapy_modules.utils import config as SingleConfig
import sapy_modules.utils.db as db_iface
from sapy_modules.utils import constants as SapyConstants
from sapy_modules.commands.command import Command
from sapy_modules.utils import values as SapyValues
from sapy_modules.core import loms
from sapy_modules.core import moms
from sapy_modules.core import tags
from sapy_modules.core import profiles
from sapy_modules.core import objectives as objs
import os, sqlite3

class SetEnv( Command ):
    short_arg   = SapyConstants.COMMANDS.SET_ENV.SHORT_ARG
    long_arg    = SapyConstants.COMMANDS.SET_ENV.LONG_ARG
    cmd_help    = SapyConstants.COMMANDS.SET_ENV.HELP
    cmd_type    = SapyConstants.COMMANDS.SET_ENV.TYPE
    cmd_action  = SapyConstants.COMMANDS.SET_ENV.ACTION

    def __init__( self, param  = None ):
        super().__init__( )
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))

    def run( self ):
        SapyValues.init()
        self.home_app()
        self.database()
        SapyValues.set_value('lom',loms.get_loms()[0])
    
    def home_app(self):
        if not os.path.exists( self.cfg['private']['home'] ) :
            os.makedirs( self.cfg['private']['home'] )
            SingleConfig.save( self.cfg )
            self.logger.debug("created app home dir")
        else:
            self.logger.debug("app home dir yet present")

    def database(self):
        # open db connection

        if not os.path.exists( self.cfg['private']['data'] ) :
            db_iface.open()
            cur = db_iface.get_cursor()
            cur.execute(SapyValues.get_value('db.create.app_meta') )
            cur.execute(SapyValues.get_value('db.populate.app_meta'),(SapyConstants.APP.VERSION,))
            db_iface.commit()
            cur.close()
            moms.create_tables()
            loms.create_tables()
            tags.create_tables()
            objs.create_tables()
            profiles.create_tables()
        else:
            db_iface.open()

