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

from sapy.utils import loggers as LoggerFactory
from sapy.utils import config as sapy_config
import sapy.utils.values as sapy_values


class Command (object):
    short_arg = 'c'
    long_arg = 'command'
    cmd_help = 'this is a command'
    cmd_type = None
    cmd_action = 'store_true'

    def __init__(self, param=None):
        self.cfg = sapy_config.get_config()
        self.values = sapy_values
        
    def run(self):
        pass
