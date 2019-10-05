#
#   File : run_graph.py
#   Author : stefano prina <stethewwolf@null.net>
#

from sapy_modules.core import LoggerFactory
from sapy_modules.core import SingleConfig
from sapy_modules.core import SapyConstants
from sapy_modules.commands.command import Command
import datetime
import sapy_modules.sapy.loms.lom as loms
import sapy_modules.core.values as SapyValues

class RunRemove ( Command ):
    short_arg = SapyConstants.COMMANDS.RUN_REMOVE.SHORT_ARG
    long_arg = SapyConstants.COMMANDS.RUN_REMOVE.LONG_ARG
    cmd_help = SapyConstants.COMMANDS.RUN_REMOVE.HELP
    cmd_type = SapyConstants.COMMANDS.RUN_REMOVE.TYPE
    cmd_action = SapyConstants.COMMANDS.RUN_REMOVE.ACTION

    def __init__( self, param ):
        super().__init__()
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))
        self.id2rm = param

    def run( self ):
        self.logger.debug("start")

        l = loms.get_lom( SapyValues.get_value('lom') )

        mlist = l.get_moms( id = self.id2rm )

        mlist[0].delete()

        self.logger.debug("end")