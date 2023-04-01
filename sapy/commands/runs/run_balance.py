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


from sapy.utils import loggers, values, printers
from sapy.commands.command import Command
from sapy.commands.setters import set_lom
from sapy.core import profiles, loms


class RunBalance (Command):
    short_arg = "b"
    long_arg = "balance"
    cmd_help = "print the actual balance"
    cmd_type = None
    cmd_action = "store_true"

    def __init__(self, param):
        super().__init__()
        self.logger = loggers.getLogger(str(self.__class__))

    def run(self):
        profile_id = profiles.get_default_profile_id()
        lom = loms.get_lom(name='Occurred')
        start_date = None
        end_date = None
        
        if values.has_value(set_lom.__lom_tag__):
            lom = values.get_value(set_lom.__lom_tag__)

        profile = profiles.get_profile(id=profile_id)

        balance = []

        if lom.name == 'Occurred':
            balance = [ profile.name, 'Occurred', start_date, end_date, profile.get_occurred_balance(start_date, end_date) ]

        if lom.name == 'Planned':
            balance = [ profile.name, 'Planned', start_date, end_date, profile.get_planned_balance(start_date, end_date) ]

        #printers.print_list('balance', balance)
        printers.print_table(['Profile', 'Lom', 'Start Date', 'End Date', 'Balance'], balance)
