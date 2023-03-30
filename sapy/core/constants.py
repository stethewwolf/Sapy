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

from string import Template

class APP :
    NAME            = 'Sapy'
    DESCRIPTION     = 'A spending traking tool'
    HOME            = '.sapy'
    CONF_FILE       = 'conf.ini'
    VERSION         = '2.0.0'
    AUTHORS         = """
                        Stefano Prina <stethewwolf@gmail.com>
                         """

class DATE:
    FORMATS = [ 
            '%d-%m-%Y',
            '%Y-%m-%d',
            '%d-%m-%y', 
            '%y-%m-%d', 
            '%c'
            ]
    SEPARATORS = [ 
        '-', 
        ' ', 
        '/', 
        '|', 
        ':', 
        '.'
        ]

class FREQUENCY:
    DAILY   = 'daily'
    MONTHLY = 'monthly'
    WEEKLY  = 'weekly'
    NONE    = None
