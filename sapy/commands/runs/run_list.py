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

import sapy.utils.values as sapy_values
import sapy.utils.printers as prntrs
import sapy.utils.loggers
from sapy.commands.command import Command
import sapy.commands.setters.set_end_date as sed
import datetime
import sapy.core.loms as loms
import sapy.core.profiles as profiles



class RunList (Command):
    short_arg = 'l'
    long_arg = 'list'
    cmd_help = 'list items, possibles values are  moms | loms | profiles'
    cmd_type = str
    cmd_action = None

    def __init__(self, param):
        super().__init__()
        self.logger = sapy.utils.loggers.getLogger(str(self.__class__))
        self.target = param

    def run(self):
        self.logger.debug("start")

        if self.target == 'moms':
            list_moms()
        elif self.target == 'loms':
            list_loms()
        elif self.target == 'profiles':
            list_profiles()
        else:
            print('invalid targget :{}'.format(self.target))

        self.logger.debug("end")


def list_moms():
    profile_id = profiles.get_default_profile_id()
    profile = profiles.get_profile(id=profile_id)
    start_date = None
    end_date = None
    
    if sapy_values.has_value(sed.__end_date_tag__):
        end_date = sapy_values.get_value(sed.__end_date_tag__)
        
    if sapy_values.has_value(sed.__start_date_tag__):
        star_date = sapy_values.get_value(sed.__start_date_tag__)
    
    lom = 'planned'
    
    moms = []
    if lom == 'occurred':
        moms = profile.get_occurred_moms(start_date, end_date)
    elif lom == 'planned':
        moms = profile.get_planned_moms(start_date, end_date)
    
    moms_str_list = []

    for mom in moms:
        moms_str_list.append('{} {} {} {}'.format(
            mom.id, mom.time, mom.value, mom.cause))

    headers = ['Id', 'Date', 'Value', 'Description']
    
    prntrs.print_table(
        'Moms from {} list {}'.format(profile.name, lom),
        headers, moms_str_list)


def list_loms():
    loms_str_list = []
    for lom in loms.get_loms():
        loms_str_list.append('[ {} ] {}'.format(lom.id, lom.name))
    prntrs.print_list('[ Id ] Loms', loms_str_list)
    pass


def list_profiles():
    profiles_str_list = []
    for pro in profiles.get_profiles():
        profiles_str_list.append('[ {} ] {}'.format(pro.profile_id, pro.name))
    prntrs.print_list('[ Id ] Profiles', profiles_str_list)
    

"""



    def list_mom(self):
        sd = self.values.get_value('start_date')
        ed = self.values.get_value('end_date')

        if sd == ed:
            sd = datetime.datetime.today().date() - datetime.timedelta(days=15)
            ed = datetime.datetime.today().date() + datetime.timedelta(days=15)

        lom = self.values.get_value('lom')

        print('------------------------------')
        print(lom.name)
        printfile:///home/stethewwolf/Projects/Applications/Sapy/sapy/utils/loggers.py
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

"""
