#
#   File : run_graph.py
#   Author : stefano prina <stethewwolf@null.net>
#

from sapy_modules.core import LoggerFactory
from sapy_modules.core import SingleConfig
from sapy_modules.core import SapyConstants
from sapy_modules.commands.command import Command
import sapy_modules.sapy.mom as moms
import sapy_modules.commands.setter.set_end as se
import csv, pathlib
import sapy_modules.sapy.lom as loms
import sapy_modules.core.values as SapyValues

class RunImport ( Command ):
    short_arg = SapyConstants.COMMANDS.RUN_IMPORT.SHORT_ARG
    long_arg = SapyConstants.COMMANDS.RUN_IMPORT.LONG_ARG
    cmd_help = SapyConstants.COMMANDS.RUN_IMPORT.HELP
    cmd_type = SapyConstants.COMMANDS.RUN_IMPORT.TYPE
    cmd_action = SapyConstants.COMMANDS.RUN_IMPORT.ACTION

    def __init__( self, param ):
        super().__init__()
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))
        self.file = pathlib.Path( param )


    def run( self ):
        self.logger.debug("start")

        l = loms.get_lom( SapyValues.get_value('lom') )

        mlist = []
        with self.file.open('r') as data_file:
            data = csv.DictReader( data_file, fieldnames=[
                'date',
                'cause',
                'value'
            ] )

            for raw in data:
                mlist.append( moms.Mom( 
                    time  = se.parse_date( raw['date'], self.logger ),
                    cause = raw['cause'],
                    value = float( raw['value'] )
                 ) ) 

        l.add(mlist)

        self.logger.debug("end")