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

__all__ = [
    'SetDaily', 
    'SetEnd', 
    'SetEnv', 
    'SetId', 
    'SetMonthly', 
    'SetLom',
    'SetStart',
    'SetValue',
    'SetWeekly',
    'SetCause',
    'SetDate',
    'SetName'
    ]

# deprecated to keep older scripts who import this from breaking
from sapy_modules.commands.setter.set_daily     import SetDaily
from sapy_modules.commands.setter.set_end       import SetEnd
from sapy_modules.commands.setter.set_env       import SetEnv
from sapy_modules.commands.setter.set_lom       import SetLom
from sapy_modules.commands.setter.set_monthly   import SetMonthly
from sapy_modules.commands.setter.set_id        import SetId
from sapy_modules.commands.setter.set_start     import SetStart
from sapy_modules.commands.setter.set_value     import SetValue
from sapy_modules.commands.setter.set_weekly    import SetWeekly
from sapy_modules.commands.setter.set_cause     import SetCause
from sapy_modules.commands.setter.set_date      import SetDate
from sapy_modules.commands.setter.set_name      import SetName