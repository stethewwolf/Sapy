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
import sapy_modules.sapy.loms.lom as loms

class RunList ( Command ):
    short_arg = SapyConstants.COMMANDS.RUN_LIST.SHORT_ARG
    long_arg = SapyConstants.COMMANDS.RUN_LIST.LONG_ARG
    cmd_help = SapyConstants.COMMANDS.RUN_LIST.HELP
    cmd_type = SapyConstants.COMMANDS.RUN_LIST.TYPE
    cmd_action = SapyConstants.COMMANDS.RUN_LIST.ACTION

    def __init__( self, param ):
        super().__init__()
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))

    def run( self ):
        self.logger.debug("start")

        sd = SapyValues.get_value('start_date')
        ed = SapyValues.get_value('end_date')

        if sd == ed : 
            sd = datetime.datetime.today().date() - datetime.timedelta(days=15)
            ed = datetime.datetime.today().date() + datetime.timedelta(days=15)
        
        l = loms.get_lom( SapyValues.get_value('lom') )
        

        print('------------------------------')
        print(l.name)
        print('------------------------------')
        print(' id |  time  | value | cause  ')
        for m in l.get_moms(start_date=sd, end_date=ed ):
            print(str( m.id ) + " | " + str( m.time ) + " | " + str( m.value ) + " | " + m.cause )
        print('------------------------------')
        self.logger.debug("end")