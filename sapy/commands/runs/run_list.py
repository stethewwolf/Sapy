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

from sapy.utils import loggers as LoggerFactory
from sapy.commands.command import Command
import datetime
import sapy.core.loms as loms
import sapy.core.profiles as profiles
import sapy.core.tags as tags
import sapy.core.objectives as objs


class RunList (Command):
    short_arg = 'l'
    long_arg = 'list'
    cmd_help = 'list things, target pro | lom | mom | pro | tag | obj '
    cmd_type = str
    cmd_action = None

    def __init__(self, param):
        super().__init__()
        self.logger = LoggerFactory.getLogger(str(self.__class__))
        self.target = param

    def run(self):
        self.logger.debug("start")

        if self.target == 'mom':
            self.list_mom()
        elif self.target == 'lom':
            self.list_lom()
        elif self.target == 'pro':
            self.list_profiles()
        elif self.target == 'obj':
            self.list_obj()
        elif self.target == 'tag':
            self.list_tag()
        else:
            print('invalid targget :{}'.format(self.target))

        self.logger.debug("end")

    def list_mom(self):
        sd = self.values.get_value('start_date')
        ed = self.values.get_value('end_date')

        if sd == ed:
            sd = datetime.datetime.today().date() - datetime.timedelta(days=15)
            ed = datetime.datetime.today().date() + datetime.timedelta(days=15)

        lom = self.values.get_value('lom')

        print('------------------------------')
        print(lom.name)
        print('------------------------------')
        print('\tid\t|\ttime\t|\tvalue\t|\tcause\t')
        for m in lom.get_moms(start_date=sd, end_date=ed):
            print('\t{}\t|\t{}\t|\t{}\t|\t{}\t'.format(
                m.id, m.time, m.value, m.cause))
        print('------------------------------')
        print(' balance : ' + str(lom.balance(sd, ed)))
        print('------------------------------')

    def list_profiles(self):
        print('------------------------------')
        print('\tid\t|\tname\t')
        print('------------------------------')
        for pro in profiles.get_profiles():
            print('\t{}\t|\t{}\t'.format(pro.profile_id, pro.name))
        print('------------------------------')
        return loms.get_loms()

    def list_lom(self):
        print('------------------------------')
        print('\tid\t|\tname\t')
        print('------------------------------')
        for lom in loms.get_loms():
            print('\t{}\t|\t{}\t'.format(lom.id, lom.name))
        print('------------------------------')
        return loms.get_loms()

    def list_tag(self):
        print('------------------------------')
        print('\tid\t|\tname\t')
        print('------------------------------')
        for t in tags.get_tags():
            print('\t{}\t|\t{}\t'.format(t.id, t.name))
        print('------------------------------')

    def list_obj(self):
        print('------------------------------')
        print('\tid\t|\tdescription\t|\tduedate\t|')
        print('------------------------------')
        for t in objs.get_objs(self.logger):
            print('\t{}\t|\t{}\t|\t{}\t'.format(
                t.id, t.description, t.duedate))
        print('------------------------------')
