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
    'NewYear',
    'NewMonth',
    'EndWeek',
    'EndMonth'
    ]

# deprecated to keep older scripts who import this from breaking
from sapy_modules.commands.tasks.new_year    import NewYear
from sapy_modules.commands.tasks.new_month   import NewMonth
from sapy_modules.commands.tasks.end_week    import EndWeek
from sapy_modules.commands.tasks.end_month   import EndMonth
