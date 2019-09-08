#
#   File : run_graph.py
#   Author : stefano prina <stethewwolf@null.net>
#

from sapy_modules.core import LoggerFactory
from sapy_modules.core import SingleConfig
from sapy_modules.core import SapyConstants
from sapy_modules.commands.command import Command

class RunImport ( Command ):
    short_arg = SapyConstants.COMMANDS.RUN_IMPORT.SHORT_ARG
    long_arg = SapyConstants.COMMANDS.RUN_IMPORT.LONG_ARG
    cmd_help = SapyConstants.COMMANDS.RUN_IMPORT.HELP
    cmd_type = SapyConstants.COMMANDS.RUN_IMPORT.TYPE
    cmd_action = SapyConstants.COMMANDS.RUN_IMPORT.ACTION

    def __init__( self, param ):
        super().__init__()
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))

    def run( self ):
        self.logger.debug("start")

        self.logger.warn("not implemented")

        self.logger.debug("end")