#
#   File : set_name.py
#   Author : stefano prina <stethewwolf@null.net>
#

from sapy_modules.core import LoggerFactory
from sapy_modules.core import SingleConfig
from sapy_modules.core import SapyConstants
from sapy_modules.commands.command import Command
import sapy_modules.core.values as SapyValues

class SetName ( Command ):
    short_arg = None
    long_arg = 'name'
    cmd_help = 'set the name'
    cmd_type = str
    cmd_action = None

    def __init__( self, param ):
        super().__init__()
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))
        self.__param = param

    def run( self ):
        self.logger.debug("start")

        SapyValues.set_value('name', self.__param)

        self.logger.debug("end")