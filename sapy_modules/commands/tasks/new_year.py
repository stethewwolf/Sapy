# Sapy
# Copyright (C) 2018 stefano prina <stethewwolf@null.net> <stethewwolf@gmail.com>
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

from sapy_modules.commands.command import Command
import fileinput
import sapy_modules.core.mlogger as LoggerFactory
from sapy_modules.commands.setter import *
from sapy_modules.commands.run import RunAdd

class NewYear(Command):
    short_arg = None
    long_arg = 'new-year'
    cmd_help = 'start a new year'
    cmd_type = None
    cmd_action = 'store_true'

    def __init__(self, param=None):
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))
    
    def run(self):
        self.logger.debug("start")
        print("do you want add objectives for this new year ?[Y/n]")
        r = '.'
        while r != 'Y' and r != 'n' and '' != r:
            r = input().strip() 

        if r == 'Y' or r == '':
            flag = True
            while flag:
                SetCause(input("insert description:").strip()).run()
                date = input("insert due date:").strip()
                if len(date) > 8:
                    SetDate(date).run()
                RunAdd('obj').run()
                r = input('continue? [Y/n]').strip()
                if r != 'Y' and r != '':
                    flag=False

        print("are you aware if outcomes for the next year  ?[Y/n]")
        r = '.'
        while r != 'Y' and r != 'n' and '' != r:
            r = input().strip() 

        if r == 'Y' or r == '':
            flag = True
            while flag:
                SetLom("expected")
                SetCause(input("insert cause:").strip()).run()
                SetValue(input("insert value:").strip()).run()
                date = input("insert due date:").strip()
                if len(date) > 8:
                    SetDate(date).run()
                RunAdd('mom').run()

                r = input('continue? [Y/n]').strip()
                if r != 'Y' and r != '':
                    flag=False

        self.logger.debug("end")

        