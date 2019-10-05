
#   File : run_add.py
#   Author : stefano prina <stethewwolf@null.net>
#

from sapy_modules.core import LoggerFactory
from sapy_modules.core import SingleConfig
from sapy_modules.core import SapyConstants
from sapy_modules.commands.command import Command
from sapy_modules.sapy.moms.mom import Mom
import sapy_modules.core.values as SapyValues
import sapy_modules.sapy.loms.lom as loms
import datetime


class RunAdd ( Command ):
    short_arg = SapyConstants.COMMANDS.RUN_ADD.SHORT_ARG
    long_arg = SapyConstants.COMMANDS.RUN_ADD.LONG_ARG
    cmd_help = SapyConstants.COMMANDS.RUN_ADD.HELP
    cmd_type = SapyConstants.COMMANDS.RUN_ADD.TYPE
    cmd_action = SapyConstants.COMMANDS.RUN_ADD.ACTION

    def __init__( self, param ):
        super().__init__( )
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))

    
    def run( self ):
        self.logger.debug("start")
        mlist=[]

        l = loms.get_lom( SapyValues.get_value('lom') )

        sd = SapyValues.get_value('start_date')
        ed = SapyValues.get_value('end_date')
        f = SapyValues.get_value('frequency')

        if sd != ed and ed > sd and f :
            if f == SapyConstants.FREQUENCY.DAILY:
                step = datetime.timedelta(days=1)

            if f == SapyConstants.FREQUENCY.WEEKLY:
                step = datetime.timedelta(days=7)

            if f == SapyConstants.FREQUENCY.MONTHLY:
                step = datetime.timedelta(days=30)
            
            itr = datetime.timedelta(days=0)

            while itr + sd <= ed :
                mlist.append( Mom ( 
                    value = SapyValues.get_value( 'value' ),
                    cause = SapyValues.get_value( 'cause' ),
                    time = sd + itr 
                    )        
                )

                itr += step

        else:
            mlist.append( Mom ( 
                value = SapyValues.get_value( 'value' ),
                cause = SapyValues.get_value( 'cause' ),
                )        
            )

        l.add(mlist)

        self.logger.debug("end")