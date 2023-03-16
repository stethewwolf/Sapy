# Sapy
# Copyright (C) 2022 stefano prina <stethewwolf@posteo.net>
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

import datetime
import sapy.utils.constants as sapy_constants


def parse_date(param, mlogger):
    date = datetime.datetime.today().date()
    parsed = False
    count_frm = 0
    while count_frm < len(sapy_constants.__date_formats__) and not parsed:

        count_sep = 0
        while count_sep < len(sapy_constants.__date_separators__) and not parsed:
            l_date_fomrat = sapy_constants.__date_formats__[count_frm].replace(
                '-', sapy_constants.__date_separators__[count_sep])

            try:
                date = datetime.strptime(param, l_date_fomrat).date()
                parsed = True
                mlogger.debug("parsed whit : " + l_date_fomrat)
            except:
                mlogger.debug("failed parsing whit : " + l_date_fomrat)
            count_sep += 1

        count_frm = +1
    else:
        if parsed:
            mlogger.debug("parsed")
        elif count_frm >= len(sapy_constants.__date_separators__):
            mlogger.debug("checked all date separators")
        else:
            mlogger.error("failed to parse " + param)

    return date
