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


from sapy.utils import loggers as LoggerFactory
import sapy.utils.constants
from sapy.commands.command import Command
import sapy.core.profiles as profiles
import sapy.core.loms as loms
import sapy.core.moms as moms
import sapy.core.tags as tags
import sapy.core.objectives as objs
import datetime


class RunAdd(Command):
    short_arg = 'a'
    long_arg = 'add'
    cmd_help = 'add new item, takes : mom | lom | pro | obj | tag'
    cmd_type = str
    cmd_action = None

    def __init__(self, param):
        super().__init__()
        self.logger = LoggerFactory.getLogger(str(self.__class__))
        self.target = param

    def run(self):
        self.logger.debug('start')

        if self.target == 'mom':
            self.add_mom()
        elif self.target == 'pro':
            self.add_profile()
        elif self.target == 'obj':
            self.add_obj()
        elif self.target == 'tag':
            self.add_tag()
        else:
            print('invalid targget :{}'.format(self.target))

        self.logger.debug("end")

    def add_mom(self):
        mlist = []
        lom_name = self.values.get_value('lom')

        start_date = self.values.get_value('start_date')
        end_date = self.values.get_value('end_date')
        freq = self.values.get_value('frequency')

        if start_date != end_date and end_date > start_date and freq:
            if freq == sapy.utils.constants.__frequency_daily__:
                step = datetime.timedelta(days=1)

            if freq == sapy.utils.constants.__frequency_weekly__:
                step = datetime.timedelta(days=7)

            if freq == sapy.utils.constants.__frequency_monthly__:
                step = datetime.timedelta(days=30)

            itr = datetime.timedelta(days=0)

            while itr + start_date <= end_date:
                mlist.append(moms.Mom(
                    value=self.values.get_value('value'),
                    cause=self.values.get_value('cause'),
                    year=(start_date + itr).year,
                    month=(start_date + itr).month,
                    day=(start_date + itr).day
                    )
                )

                itr += step

        else:
            mlist.append(moms.Mom(
                value=self.values.get_value('value'),
                cause=self.values.get_value('cause'),
                year=start_date.year,
                month=start_date.month,
                day=start_date.day
                )
            )
        
        lom = loms.get_lom(name=lom_name)
        lom.add(mlist)

        print('Lom')
        print('------------------------------')
        print('|\tid\t|\tname\t|')
        print('|\t{}\t|\t{}\t|'.format(lom.id, lom.name))
        print('------------------------------')
        print('New Moms')
        print('------------------------------')
        print('|\tid\t|\tvalue\t|\tcause\t|\tdate\t|')
        for m in mlist:
            print('|\t{}\t|\t{}\t|\t{}\t|\t{}\t|'.format(
                m.id, m.value, m.cause, m.time))
        print('------------------------------')

    def add_profile(self):
        p = profiles.Profile(name=SapyValues.get_value('name'))
        print('New Profile')
        print('------------------------------')
        print('|\tid\t|\tname\t|')
        print('|\t{}\t|\t{}\t|'.format(p.id, p.name))
        print('------------------------------')

    def add_obj(self):
        ed = self.values.get_value('end_date')
        o = objs.Objective(
            description=self.values.get_value('cause'), duedate=ed)
        print('New Objective')
        print('------------------------------')
        print('|\tid\t|\tdescription\t\t|\tdue date\t|')
        print('|\t{}\t|\t{}\t|\t{}\t|'.format(o.id, o.description, o.duedate))
        print('------------------------------')

    def add_tag(self):
        tag = tags.Tag(name=self.values.get_value('name'))
        print('New Tag')
        print('------------------------------')
        print('|\tid\t|\tname\t|')
        print('|\t{}\t|\t{}\t|'.format(tag.id, tag.name))
        print('------------------------------')
