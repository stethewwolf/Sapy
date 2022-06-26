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

from sapy_modules.utils import loggers as LoggerFactory
from sapy_modules.utils import config as SingleConfig
from sapy_modules.utils import constants as SapyConstants
from sapy_modules.utils import values as SapyValues
from sapy_modules.commands.command import Command
import datetime
import sapy_modules.core.loms 
import sapy_modules.core.tags 
import sapy_modules.core.objectives as objs

class RunList ( Command ):
    short_arg = 'l'
    long_arg = 'list' 
    cmd_help = 'list things, target lom | mom | tag | obj '
    cmd_type = str
    cmd_action = None

    def __init__( self, param ):
        super().__init__()
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))
        self.target = param

    def run( self ):
        self.logger.debug("start")

        if self.target == 'mom' :
            self.list_mom()
        elif self.target == 'lom':
            self.list_lom()
        elif self.target == 'obj':
            self.list_obj()
        elif self.target == 'tag':
            self.list_tag()
        else :
            print('invalid targget :{}'.format(self.target))

        self.logger.debug("end")

    def list_mom(self):
        sd = SapyValues.get_value('start_date')
        ed = SapyValues.get_value('end_date')

        if sd == ed : 
            sd = datetime.datetime.today().date() - datetime.timedelta(days=15)
            ed = datetime.datetime.today().date() + datetime.timedelta(days=15)
        
        l = SapyValues.get_value('lom')
        
        print('------------------------------')
        print(l.name)
        print('------------------------------')
        print('\tid\t|\ttime\t|\tvalue\t|\tcause\t')
        for m in l.get_moms(start_date=sd, end_date=ed ):
            print('\t{}\t|\t{}\t|\t{}\t|\t{}\t'.format(m.id,m.time,m.value,m.cause))
        print('------------------------------')
        print(' balance : ' + str( l.balance(sd,ed)) )
        print('------------------------------')

    def list_lom(self):
        print('------------------------------')
        print('\tid\t|\tname\t')
        print('------------------------------')
        for l in loms.get_loms():
            print('\t{}\t|\t{}\t'.format(l.id,l.name))
        print('------------------------------')
        return loms.get_loms()

    def list_tag(self):
        print('------------------------------')
        print('\tid\t|\tname\t')
        print('------------------------------')
        for t in tags.get_tags():
            print('\t{}\t|\t{}\t'.format(t.id,t.name))
        print('------------------------------')

    def list_obj(self):
        print('------------------------------')
        print('\tid\t|\tdescription\t|\tduedate\t|')
        print('------------------------------')
        for t in objs.get_objs(self.logger):
            print('\t{}\t|\t{}\t|\t{}\t'.format(t.id,t.description,t.duedate))
        print('------------------------------')
