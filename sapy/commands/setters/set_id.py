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

from  sapy.utils import loggers as LoggerFactory
from  sapy.utils import config as SingleConfig
from  sapy.utils import constants as SapyConstants
from  sapy.utils import values as SapyValues
from  sapy.commands.command import Command


class SetId ( Command ):
    short_arg = None
    long_arg = 'id'
    cmd_help = 'specify id for operation'
    cmd_type = str
    cmd_action = None

    def __init__( self, param ):
        super().__init__()
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))
        self.id=param

    def run( self ):
        self.logger.debug("start")

        SapyValues.set_value('id', self.id)

        self.logger.debug("end")
