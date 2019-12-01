#
#   File : set_real.py
#   Author : stefano prina <stethewwolf@null.net>
#

from sapy_modules.core import LoggerFactory
from sapy_modules.core import SingleConfig
from sapy_modules.core import SapyConstants
from sapy_modules.commands.command import Command
import sapy_modules.core.values as SapyValues

class SetId ( Command ):
    short_arg = None
    long_arg = 'id'
    cmd_help = 'specify id for operation'
    cmd_type = str
    cmd_action = None

    def __init__( self, param ):
        super().__init__()
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))
        self.id=param

    def run( self ):
        self.logger.debug("start")

        SapyValues.set_value('id', self.id)

        self.logger.debug("end")