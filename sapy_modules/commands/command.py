

#   File : command.py
#   Author : stefano prina <stethewwolf@null.net>
#

from sapy_modules.core import LoggerFactory
from sapy_modules.core import SingleConfig
from sapy_modules.core import SapyConstants

class Command (object):
    short_arg = SapyConstants.COMMANDS.CMD.SHORT_ARG
    long_arg = SapyConstants.COMMANDS.CMD.LONG_ARG
    cmd_help = SapyConstants.COMMANDS.CMD.HELP
    cmd_type = SapyConstants.COMMANDS.CMD.TYPE
    cmd_action = SapyConstants.COMMANDS.CMD.ACTION

    def __init__( self, param = None ):
        self.cfg = SingleConfig.getConfig()

    def run( self ):
        pass