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


from sapy.utils import loggers as logger_factory
from sapy.utils import values
from sapy.utils import printers
import sapy.utils.constants
from sapy.commands.command import Command
from sapy.commands.setters import set_name 
import sapy.core.profiles as profiles
import sapy.core.loms as loms
import sapy.core.moms as moms
import datetime


class RunAdd(Command):
    short_arg = 'a'
    long_arg = 'add'
    cmd_help = 'add new item, takes : mom | | pro '
    cmd_type = str
    cmd_action = None

    def __init__(self, param):
        super().__init__()
        self.logger = logger_factory.getLogger(str(self.__class__))
        self.target = param

    def run(self):
        self.logger.debug('start')

        if self.target == 'mom':
            add_mom()
        elif self.target == 'pro':
            add_profile()
        else:
            print('invalid targget :{}'.format(self.target))

        self.logger.debug("end")

def add_mom():
    mlist = []
    lom_name = values.get_value('lom')
    start_date = values.get_value('start_date')
    end_date = values.get_value('end_date')
    freq = values.get_value('frequency')

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
                value=values.get_value('value'),
                cause=values.get_value('cause'),
                year=(start_date + itr).year,
                month=(start_date + itr).month,
                day=(start_date + itr).day
                )
            )

            itr += step

    else:
        mlist.append(moms.Mom(
            value = values.get_value('value'),
            cause = values.get_value('cause'),
            year = start_date.year,
            month = start_date.month,
            day = start_date.day
            )
        )
    
    lom = loms.get_lom(name=lom_name)
    lom.add(mlist)


def add_profile():
    new_pro_name = "New Profile"

    if values.has_value(set_name.__name_tag__):
        new_pro_name = values.get_value(set_name.__name_tag__)

    p = profiles.Profile(name=new_pro_name)

    printers.print_list('[ Id ] Profiles', ['[ {} ] {}'.format(p.profile_id, p.name)])

