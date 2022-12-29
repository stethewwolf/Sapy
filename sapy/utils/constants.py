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

from string import Template


class APP:
    NAME = 'Sapy'
    DESCRIPTION = 'A spending traking tool'
    HOME = '.sapy'
    CONF_FILE = 'conf.ini'
    VERSION = '2.2.0'
    AUTHORS = """
        Stefano Prina <stethewwolf@posteo.net
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


class DB:
    FILE = 'data.sqlite3'


class COMMANDS:
    class CMD:
        SHORT_ARG = "c"
        LONG_ARG = "command"
        HELP = "this is a command"
        TYPE = None
        ACTION = 'store_true'

    class RUN_GRAPH:
        SHORT_ARG = "g"
        LONG_ARG = "graph"
        HELP = "print the graph"
        TYPE = None
        ACTION = 'store_true'

    class RUN_IMPORT:
        SHORT_ARG = "i"
        LONG_ARG = "import"
        HELP = "import data from csv file"
        TYPE = str
        ACTION = None

    class RUN_VERSION:
        SHORT_ARG = "V"
        LONG_ARG = "version"
        HELP = "print the version"
        TYPE = None
        ACTION = 'store_true'

    class SET_DAILY:
        SHORT_ARG = "D"
        LONG_ARG = "daily"
        HELP = "set daily occurance"
        TYPE = None
        ACTION = 'store_true'

    class SET_END:
        SHORT_ARG = None
        LONG_ARG = "end-date"
        HELP = "set end date"
        TYPE = str
        ACTION = None

    class SET_ENV:
        SHORT_ARG = None
        LONG_ARG = None
        HELP = None
        TYPE = None
        ACTION = None

    class SET_MONTHLY:
        SHORT_ARG = None
        LONG_ARG = "monthly"
        HELP = "set monthly occurrance"
        TYPE = None
        ACTION = 'store_true'

    class SET_START:
        SHORT_ARG   = None
        LONG_ARG    = "start-date"
        HELP    = "set start date"
        TYPE    = str
        ACTION  = None


    class SET_VALUE:
        SHORT_ARG   = "v"
        LONG_ARG    = "value"
        HELP    = "set value"
        TYPE    = float
        ACTION  = None


    class SET_WEEKLY:
        SHORT_ARG   = None
        LONG_ARG    = "weekly"
        HELP    = "set weekly occurrance"
        TYPE    = None
        ACTION  = 'store_true'

    class SET_CAUSE:
        SHORT_ARG   = "c"
        LONG_ARG    = "cause"
        HELP    = "set cause"
        TYPE    = str
        ACTION  = None

class FREQUENCY:
    DAILY   = 'daily'
    MONTHLY = 'monthly'
    WEEKLY  = 'weekly'
    NONE    = None
