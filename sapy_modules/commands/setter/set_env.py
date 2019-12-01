#
#   File : run_graph.py
#   Author : stefano prina <stethewwolf@null.net>
#

from sapy_modules.core import LoggerFactory
from sapy_modules.core import SingleConfig
import sapy_modules.core.db as db_iface
from sapy_modules.core import SapyConstants
from sapy_modules.commands.command import Command
import sapy_modules.core.values as SapyValues
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

            cur.execute( SapyValues.get_value('db.create.moms') )
            cur.execute( SapyValues.get_value('db.create.mom_in_lom') )
            cur.execute( SapyValues.get_value('db.create.loms') )
            cur.execute( SapyValues.get_value('db.populate.lom') )
            cur.execute( SapyValues.get_value('db.create.objectives') )
            cur.execute( SapyValues.get_value('db.create.tags') )
            cur.execute( SapyValues.get_value('db.create.tag_in_mom') )

            db_iface.commit()
            cur.close()
        else :
            db_iface.open()

