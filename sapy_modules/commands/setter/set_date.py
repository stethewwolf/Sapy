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

from sapy_modules.core import LoggerFactory
from sapy_modules.core import SingleConfig
from sapy_modules.core import SapyConstants
from sapy_modules.commands.command import Command
import sapy_modules.commands.setter.set_end as se
import sapy_modules.core.values as SapyValues

class SetDate (Command):
    short_arg = "d"
    long_arg = "date"
    cmd_help = "set the date for the operation"
    cmd_type = str
    cmd_action = None

    def __init__(self, param):
        super().__init__()
        self.logger = LoggerFactory.getLogger(str(self.__class__))
        self.__param = param

    def run(self):
        self.logger.debug("start")

        SapyValues.set_value('start_date', se.parse_date(self.__param, self.logger))
        SapyValues.set_value('end_date', se.parse_date(self.__param, self.logger))

        self.logger.debug("end")