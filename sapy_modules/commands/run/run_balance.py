#
#   File : run_graph.py
#   Author : stefano prina <stethewwolf@null.net>
#

from sapy_modules.core import LoggerFactory
from sapy_modules.core import SingleConfig
from sapy_modules.core import SapyConstants
import sapy_modules.core.values as SapyValues
from sapy_modules.commands.command import Command
import datetime
import sapy_modules.sapy.lom as loms

class RunBalance ( Command ):
    short_arg = "b"
    long_arg = "balance"
    cmd_help = "print the actual balance of the list"
    cmd_type = None
    cmd_action = "store_true"

    def __init__( self, param ):
        super().__init__()
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))

    def run( self ):
        self.logger.debug("start")

        l = loms.get_lom( SapyValues.get_value('lom') )

        ed = SapyValues.get_value('end_date')

        l = loms.get_lom( SapyValues.get_value('lom') )
        
        print('------------------------------')
        print(l.name)
        print('------------------------------')
        print(' balance : ' + str( l.balance(end_date=ed)) )
        print('------------------------------')
        self.logger.debug("end")