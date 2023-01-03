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

from sapy.utils import loggers as LoggerFactory
from sapy.commands.command import Command
import sapy.core.moms as moms
from sapy.commands.setters import set_end as se
import csv
import pathlib
import sapy.core.loms as loms
import sapy.utils.values as SapyValues


class RunImport (Command):
    short_arg = 'i'
    long_arg = 'import'
    cmd_help = 'import data from csv file'
    cmd_type = str
    cmd_action = None

    def __init__(self, param):
        super().__init__()
        self.logger = LoggerFactory.getLogger(str(self.__class__))
        self.file = pathlib.Path(param)

    def run(self):
        self.logger.debug("start")

        lom = self.values.get_value('lom')

        mlist = []
        with self.file.open('r') as data_file:
            data = csv.DictReader(
                data_file,
                fieldnames=[
                    'date',
                    'cause',
                    'value'])

            for raw in data:
                mlist.append(moms.Mom(
                    day=se.parse_date(raw['date'], self.logger).day,
                    month=se.parse_date(raw['date'], self.logger).month,
                    year=se.parse_date(raw['date'], self.logger).year,
                    cause=raw['cause'],
                    value=float(raw['value'])))

        lom.add(mlist)

        self.logger.debug("end")
