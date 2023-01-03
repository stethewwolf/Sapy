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
from sapy.commands.command import Command
import datetime
import sapy.core.loms
import sapy.core.tags as tags
import sapy.core.objectives as objs


class RunRemove (Command):
    short_arg = 'r'
    long_arg = 'rm'
    cmd_help = 'remove target : lom | mom | tag | obj'
    cmd_type = str
    cmd_action = None

    def __init__(self, param):
        super().__init__()
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))
        self.target = param

    def run(self):
        self.logger.debug("start")
        
        self.id2rm = SapyValues.get_value('id')

        if self.target == 'mom':
            self.rm_mom()
        elif self.target == 'lom':
            self.rm_lom()
        elif self.target == 'obj':
            self.rm_obj()
        elif self.target == 'tag':
            self.rm_tag()
        else:
            print('invalid targget :{}'.format(self.target))

        self.logger.debug("end")

    def rm_mom(self):
        lom = self.values.get_value('lom')
        mlist = lom.get_moms(id=self.id2rm)
        mlist[0].delete()

    def rm_lom(self):
        lom = loms.get_lom(id=self.id2rm )

        mlist = l.get_moms()

        for m in  mlist :
            m.delete()

        l.delete()

    def rm_tag(self):
        t = tags.get_tag(id=self.id2rm)
        t.delete()
        pass

    def rm_obj(self):
        o = objs.get_obj(self.id2rm, self.logger)
        o.delete()
        pass
