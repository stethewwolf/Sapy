#
#   File : set_date.py
#   Author : stefano prina <stethewwolf@null.net>
#

from sapy_modules.core import LoggerFactory
from sapy_modules.core import SingleConfig
from sapy_modules.core import SapyConstants
from sapy_modules.commands.command import Command
import sapy_modules.commands.setter.set_end as se
import sapy_modules.core.values as SapyValues

class SetDate ( Command ):
    short_arg = "d"
    long_arg = "date"
    cmd_help = "set the date for the operation"
    cmd_type = str
    cmd_action = None

    def __init__( self, param ):
        super().__init__()
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))
        self.__param = param

    def run( self ):
        self.logger.debug("start")

        SapyValues.set_value( 'start_date', se.parse_date( self.__param, self.logger ) )
        SapyValues.set_value( 'end_date', se.parse_date( self.__param, self.logger ) )

        self.logger.debug("end")