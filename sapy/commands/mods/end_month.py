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

from  sapy.commands.command import Command
import  sapy.utils.loggers as LoggerFactory
from  sapy.commands.setters import SetCause, SetValue, SetLom, SetDate
from  sapy.commands.runs import RunAdd
import  sapy.core.objectives as objs
import  sapy.core.loms as loms
import  sapy.utils.values as SapyValues
import datetime
import calendar

class EndMonth(Command):
    short_arg = None
    long_arg = 'end-month'
    cmd_help = 'ends the month'
    cmd_type = None
    cmd_action = 'store_true'

    def __init__(self, param=None):
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))
    
    def run(self):
        self.logger.debug("start")
        sd = datetime.date(
            SapyValues.get_value("date").year,
            SapyValues.get_value("date").month,
            1
        )
        
        ed = datetime.date(
            SapyValues.get_value("date").year,
            SapyValues.get_value("date").month,
            calendar.monthrange(
            SapyValues.get_value("date").year,
            SapyValues.get_value("date").month
            )[0]
        )

        print("objectives this month was:")
        for o in objs.get_objs(self.logger):
            if o.duedate.month == SapyValues.get_value("date").month:
                print("|\t{}\t|\t{}\t|".format(o.description,o.duedate))
       
        #TODO ask for complete objectives



        l_real = loms.get_lom(name="real")

        l_b = l_real.balance(start_date=sd,end_date=ed)

        l_planned = loms.get_lom(name="expected")

        p_b = l_planned.balance(start_date=sd,end_date=ed)

        print("============================")
        print("expected balance :",p_b)
        print("real balance :",l_b)
        print("============================")

        self.logger.debug("end")
