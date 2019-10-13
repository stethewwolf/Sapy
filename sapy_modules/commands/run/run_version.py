#
#   File : run_graph.py
#   Author : stefano prina <stethewwolf@null.net>
#

from sapy_modules.core import LoggerFactory
from sapy_modules.core import SingleConfig
from sapy_modules.core import SapyConstants
from sapy_modules.commands.command import Command

class RunVersion ( Command ):
    short_arg = SapyConstants.COMMANDS.RUN_VERSION.SHORT_ARG
    long_arg = SapyConstants.COMMANDS.RUN_VERSION.LONG_ARG
    cmd_help = SapyConstants.COMMANDS.RUN_VERSION.HELP
    cmd_type = SapyConstants.COMMANDS.RUN_VERSION.TYPE
    cmd_action = SapyConstants.COMMANDS.RUN_VERSION.ACTION

    def __init__( self, param ):
        super().__init__()
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))

    def run( self ):
        self.logger.debug("start")

        print(SapyConstants.APP.NAME + " - " + SapyConstants.APP.VERSION )
        print("\t" + SapyConstants.APP.AUTHORS )

        self.logger.debug("end")