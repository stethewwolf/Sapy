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

from  sapy.utils import loggers as logger_factory
from  sapy.utils import config 
from  sapy.utils import constants 
from  sapy.utils import values as sapy_values
from  sapy.commands.command import Command
from  sapy.core import loms 

__lom_tag__ = "lom"

class SetLom ( Command ):
    short_arg = None
    long_arg = 'lom'
    cmd_help = 'specify the list of money ( lom )'
    cmd_type = str
    cmd_action = None 

    def __init__(self, param):
        super().__init__( )
        self.logger = logger_factory.getLogger(str( self.__class__ ))
        self.lom_value=param

    def run(self):
        self.logger.debug("start")

        lom = None
        lom_id = None

        try:
            lom_id = int(self.lom_value)
        except Exception as ex:
            self.logger.debug("lom value is not integer: "+str(ex))

        if lom_id:
            lom = loms.get_lom(id=lom_id)
        else:
            lom = loms.get_lom(name=self.lom_value)

        if lom:
            sapy_values.set_value(__lom_tag__, lom)

        self.logger.debug("end")
