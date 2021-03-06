# Sapy
# Copyright (C) 2018 stefano prina <stefano-prina@outlook.it> <stethewwolf@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from sapy_modules.core import LoggerFactory
from sapy_modules.core import SingleConfig
from sapy_modules.core import SapyConstants
import sapy_modules.core.values as SapyValues
from sapy_modules.commands.command import Command
from datetime import datetime

class SetEnd ( Command ):
    short_arg = SapyConstants.COMMANDS.SET_END.SHORT_ARG
    long_arg = SapyConstants.COMMANDS.SET_END.LONG_ARG
    cmd_help = SapyConstants.COMMANDS.SET_END.HELP
    cmd_type = SapyConstants.COMMANDS.SET_END.TYPE
    cmd_action = SapyConstants.COMMANDS.SET_END.ACTION

    def __init__( self, param ):
        super().__init__( )
        self.logger = LoggerFactory.getLogger(str(self.__class__))
        self.__param = param


    def run( self ):
        self.logger.debug("start")

        SapyValues.set_value('end_date', parse_date(self.__param,self.logger))

        self.logger.debug("end")


def parse_date( param, mlogger ):
    date = datetime.today().date()
    parsed = False
    
    count_frm = 0
    while count_frm < len(SapyConstants.DATE.FORMATS) and not parsed :

        count_sep = 0
        while count_sep < len(SapyConstants.DATE.SEPARATORS) and not parsed :
            l_date_fomrat = SapyConstants.DATE.FORMATS[count_frm].replace('-', SapyConstants.DATE.SEPARATORS[count_sep])
       
            try :
                date = datetime.strptime(param, l_date_fomrat).date()
                parsed = True
                mlogger.debug("parsed whit : " + l_date_fomrat)
            except :
                mlogger.debug("failed parsing whit : " + l_date_fomrat)
            
            count_sep += 1

        count_frm =+ 1 
    else :
        if parsed :
            mlogger.debug("parsed")
        elif count_frm >= len(SapyConstants.DATE.SEPARATORS):
            mlogger.debug("checked all date separators")
        else :
            mlogger.error("failed to parse " + param)

    return date