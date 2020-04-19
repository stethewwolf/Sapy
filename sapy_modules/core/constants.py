#
#   Author : stefano prina 

from string import Template

class APP :
    NAME            = 'Sapy'
    DESCRIPTION     = 'A spending traking tool'
    HOME            = '.sapy'
    CONF_FILE       = 'conf.ini'
    VERSION         = '1.0.0'
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


class DB:
    FILE                    = 'data.sqlite3'


class COMMANDS:
    class CMD:
        SHORT_ARG   = "c"
        LONG_ARG    = "command"
        HELP    = "this is a command"
        TYPE    = None
        ACTION  = 'store_true'


    class RUN_GRAPH:
        SHORT_ARG   = "g"
        LONG_ARG    = "graph"
        HELP    = "print the graph"
        TYPE    = None
        ACTION  = 'store_true'


    class RUN_GUI:
        SHORT_ARG   = None
        LONG_ARG    = "gui"
        HELP    = "run the application in grafical mode"
        TYPE    = None
        ACTION  = 'store_true'


    class RUN_IMPORT:
        SHORT_ARG   = "i"
        LONG_ARG    = "import"
        HELP    = "import data from csv file"
        TYPE    = str
        ACTION  = None


    class RUN_VERSION:
        SHORT_ARG   = "V"
        LONG_ARG    = "version"
        HELP    = "print the version"
        TYPE    = None
        ACTION  = 'store_true'


    class SET_DAILY:
        SHORT_ARG   = "D"
        LONG_ARG    = "daily"
        HELP    = "set daily occurance"
        TYPE    = None
        ACTION  = 'store_true'


    class SET_END:
        SHORT_ARG   = None
        LONG_ARG    = "end-date"
        HELP    = "set end date"
        TYPE    = str
        ACTION  = None


    class SET_ENV:
        SHORT_ARG   = None
        LONG_ARG    = None
        HELP    = None
        TYPE    = None
        ACTION  = None


    class SET_MONTHLY:
        SHORT_ARG   = None
        LONG_ARG    = "monthly"
        HELP    = "set monthly occurrance"
        TYPE    = None
        ACTION  = 'store_true'


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
