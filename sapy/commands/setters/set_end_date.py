# Sapy
# Copyright (C) 2018 stefano prina <stethewwolf@posteo.net>
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
import sapy.utils.values as vls
import sapy.utils.dates as dts
from sapy.commands.command import Command

__end_date_tag__ = 'end-date'

class SetEndDate (Command):
    short_arg = None
    long_arg = 'end-date'
    cmd_help = 'set end date'
    cmd_type = str
    cmd_action = None

    def __init__(self, param):
        super().__init__()
        self.logger = sapy.utils.loggers.getLogger(str(self.__class__))
        self.__param = param

    def run(self):
        self.logger.debug("start")

        vls.set_value(
            __end_date_tag__,
            dts.parse_date(self.__param, self.logger))

        self.logger.debug("end")



