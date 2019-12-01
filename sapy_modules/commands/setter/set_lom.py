#
#   File : set_expecetd.py
#   Author : stefano prina <stethewwolf@null.net>
#

from sapy_modules.core import LoggerFactory
from sapy_modules.core import SingleConfig
from sapy_modules.core import SapyConstants
from sapy_modules.commands.command import Command
import sapy_modules.core.values as SapyValues
import sapy_modules.sapy.lom as loms

class SetLom ( Command ):
    short_arg = None
    long_arg = 'lom'
    cmd_help = 'specify the list of money ( lom )'
    cmd_type = str
    cmd_action = None 

    def __init__( self, param ):
        super().__init__( )
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))
        self.name=param

    def run( self ):
        self.logger.debug("start")

        l = loms.get_lom(name=self.name)

        if l:
            SapyValues.set_value('lom', l.id)

        self.logger.debug("end")