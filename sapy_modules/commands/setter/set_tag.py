#
#   File : set_cause.py
#   Author : stefano prina <stethewwolf@null.net>
#

from sapy_modules.core import LoggerFactory
from sapy_modules.core import SingleConfig
from sapy_modules.core import SapyConstants
from sapy_modules.commands.command import Command
import sapy_modules.core.values as SapyValues
import sapy_modules.sapy.tags as tags

class SetTag ( Command ):
    short_arg = None
    long_arg = 'tag'
    cmd_help = 'set the tag for the mom'
    cmd_type = str
    cmd_action = None

    def __init__( self, param ):
        super().__init__()
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))
        self.name = param

    def run( self ):
        self.logger.debug("start")

        t_id = tags.get_tag(name=self.name).id
        SapyValues.set_value( 'tag', t_id )

        self.logger.debug("end")