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

from sapy.utils import loggers
from sapy.utils import values
from sapy.commands.command import Command
from sapy.commands.setters import set_id
from sapy.core import profiles, moms

class RunRemove (Command):
    short_arg = 'r'
    long_arg = 'rm'
    cmd_help = 'remove target : mom | profile'
    cmd_type = str
    cmd_action = None

    def __init__(self, param):
        super().__init__()
        self.logger = loggers.getLogger(str(self.__class__))
        self.target = param

    def run(self):
        id_to_remove = values.get_value(set_id.__id_tag__)

        if self.target == 'mom':
            rm_mom(id_to_remove)
        elif self.target == 'profile':
            rm_profile(id_to_remove)
        else:
            print('invalid targget :{}'.format(self.target))


def rm_mom(target_id):
    moms.delete_mom(target_id)

def rm_profile(target_id):
    profile = profiles.get_profile(id=target_id)
    if profile:
        profile.remove_profile()
