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
import sapy.utils.loggers
import sapy.utils.values as sapy_values
from sapy.commands.command import Command
import sapy.commands.setters.set_end_date as sed
import sapy.commands.setters.set_start_date as ssd
import sapy.utils.dates as dts

__date_tag__ = 'date'

class SetDate (Command):
    short_arg = "d"
    long_arg = "date"
    cmd_help = "set the date for the operation"
    cmd_type = str
    cmd_action = None

    def __init__(self, param):
        super().__init__()
        self.logger = sapy.utils.loggers.getLogger(str(self.__class__))
        self.__param = param

    def run(self):
        sapy_values.set_value(
            __date_tag__, dts.parse_date(self.__param, self.logger))
        sapy_values.set_value(
            ssd.__start_date_tag__, dts.parse_date(self.__param, self.logger))
        sapy_values.set_value(
            sed.__end_date_tag__, dts.parse_date(self.__param, self.logger))

