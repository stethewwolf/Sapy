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

__all__ = [
    'SetDaily',
    'SetEndDate',
    'SetEnv',
    'SetId',
    'SetMonthly',
    'SetLom',
    'SetStartDate',
    'SetValue',
    'SetWeekly',
    'SetCause',
    'SetDate',
    'SetName'
    ]

# deprecated to keep older scripts who import this from breaking
from sapy.commands.setters.set_daily import SetDaily
from sapy.commands.setters.set_end_date import SetEndDate
from sapy.commands.setters.set_env import SetEnv
from sapy.commands.setters.set_lom import SetLom
from sapy.commands.setters.set_monthly import SetMonthly
from sapy.commands.setters.set_id import SetId
from sapy.commands.setters.set_start_date import SetStartDate
from sapy.commands.setters.set_value import SetValue
from sapy.commands.setters.set_weekly import SetWeekly
from sapy.commands.setters.set_cause import SetCause
from sapy.commands.setters.set_date import SetDate
from sapy.commands.setters.set_name import SetName
