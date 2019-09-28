
#   File : run_add.py
#   Author : stefano prina <stethewwolf@null.net>
#

from sapy_modules.core import LoggerFactory
from sapy_modules.core import SingleConfig
from sapy_modules.core import SapyConstants
from sapy_modules.commands.command import Command
from sapy_modules.sapy.moms.mom import Mom
import sapy_modules.core.values as SapyValues

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

        self.logger.warn("not implemented")
 
        m = Mom( value = SapyValues.get_value( 'value' ),
                cause = SapyValues.get_value( 'cause' )
                 )

        self.logger.debug(m.to_dict())

        self.logger.debug("end")