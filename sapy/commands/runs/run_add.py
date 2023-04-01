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
from sapy.utils import constants
from sapy.commands.command import Command
from sapy.commands.setters import set_name, set_start_date, set_end_date, set_lom, set_cause, set_value, set_daily, set_monthly, set_weekly, set_date
import sapy.core.profiles as profiles
import sapy.core.loms as loms
import sapy.core.moms as moms
import datetime


class RunAdd(Command):
    short_arg = 'a'
    long_arg = 'add'
    cmd_help = 'add new item, takes : mom | pro '
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
    profile_id = profiles.get_default_profile_id()
    profile = profiles.get_profile(id=profile_id)
    lom = loms.get_lom(name='Occurred')
    mlist = []
    start_date = None
    end_date = None
    date = None
    mom_date = None
    freq = constants.__frequency_none__
    mom_cause = 'cause'
    mom_value = 0.5

    if values.has_value(set_lom.__lom_tag__):
       lom = values.get_value(set_lom.__lom_tag__)
   
    if values.has_value(set_date.__date_tag__):
       date = values.get_value(set_date.__date_tag__)

    if not date:
        if values.has_value(set_start_date.__start_date_tag__):
            start_date = values.get_value(set_start_date.__start_date_tag__)

        if values.has_value(set_end_date.__end_date_tag__):
            end_date = values.get_value(set_end_date.__end_date_tag__)

    if values.has_value(set_cause.__cause_tag__):
        mom_cause = values.get_value(set_cause.__cause_tag__)
    else:
        if values.has_value(set_name.__name_tag__):
            mom_cause = values.get_value(set_name.__name_tag__)
   
    if values.has_value(set_value.__value_tag__):
        mom_value = values.get_value(set_value.__value_tag__)

    if values.has_value(constants.__frequency_tag__):
        freq = values.get_value(constants.__frequency_tag__)

    if start_date != end_date and end_date > start_date and freq:
        if freq == constants.__frequency_daily__:
            step = datetime.timedelta(days=1)

        if freq == constants.__frequency_weekly__:
            step = datetime.timedelta(days=7)

        if freq == constants.__frequency_monthly__:
            step = datetime.timedelta(days=30)

        itr = datetime.timedelta(days=0)

        while itr + start_date <= end_date:
            mlist.append(moms.Mom(
                value = mom_value,
                cause = mom_cause,
                year = (start_date + itr).year,
                month = (start_date + itr).month,
                day = (start_date + itr).day
                )
            )

            itr += step

    else:
        if mom_date: 
            mlist.append(moms.Mom(
                value = mom_value,
                cause = mom_cause,
                year = start_date.year,
                month = start_date.month,
                day = start_date.day
                )
            )
        else:
            mlist.append(moms.Mom(
                value = mom_value,
                cause = mom_cause,
                )
            )
    
    if lom.name == 'Occurred':
        profile.add_occurred_mom(mlist)
    elif lom.name == 'Planned':
        profile.add_planned_mom(mlist)


def add_profile():
    new_pro_name = "New Profile"

    if values.has_value(set_name.__name_tag__):
        new_pro_name = values.get_value(set_name.__name_tag__)

    p = profiles.Profile(name=new_pro_name)

    printers.print_list('[ Id ] Profiles', ['[ {} ] {}'.format(p.profile_id, p.name)])

