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
    CREATE_LOMS             = """   CREATE TABLE "loms" (
	                                    "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	                                    "name"	TEXT NOT NULL UNIQUE
                                    ) """

    CREATE_MOMS          = """   CREATE TABLE "moms" (
	                                    "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	                                    "value"	REAL NOT NULL,
	                                    "cause"	TEXT,
	                                    "date"	TEXT NOT NULL
                                    ) """ 

    CREATE_MOM_IN_LOM    = """   CREATE TABLE "mom_in_lom" (
	                                    "mom_id"	INTEGER NOT NULL,
	                                    "lom_id"	INTEGER NOT NULL,
	                                    PRIMARY KEY("lom_id","mom_id")
                                    ) """
                                    
    POPULATE_LOM         = """ INSERT INTO "loms" ("id","name") VALUES (1,'real'),(2,'expected'); """

    MOM_CREATE_QUERY    =  Template( 'INSERT INTO moms ("value", "cause", "date") values ( "$value","$cause","$date");' )
    MOM_SEARCH_BY_ID_QUERY    =  Template( 'SELECT * from moms WHERE id=$id;')
    MOM_SEARCH_BY_CAUSE_QUERY    =  Template( 'SELECT * from moms WHERE cause=$cause;')



class COMMANDS:
    class CMD:
        SHORT_ARG   = "c"
        LONG_ARG    = "command"
        HELP    = "this is a command"
        TYPE    = None
        ACTION  = 'store_true'


    class RUN_ADD:
        SHORT_ARG   = "a"
        LONG_ARG    = "add"
        HELP    = "add new movements of money"
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

    class RUN_REMOVE:
        SHORT_ARG   = "r"
        LONG_ARG    = "remove"
        HELP    = "remove movements of money"
        TYPE    = int
        ACTION  = None


    class RUN_LIST:
        SHORT_ARG   = "l"
        LONG_ARG    = "list"
        HELP    = "list movements of money"
        TYPE    = None
        ACTION  = 'store_true'


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


    class SET_DB:
        SHORT_ARG   = None
        LONG_ARG    = "db"
        HELP    = "set database path"
        TYPE    = str
        ACTION  = None


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


    class SET_EXPECTED:
        SHORT_ARG   = "E"
        LONG_ARG    = "expected"
        HELP    = "work on expected list"
        TYPE    = None
        ACTION  = 'store_true'
        

    class SET_MONTHLY:
        SHORT_ARG   = None
        LONG_ARG    = "monthly"
        HELP    = "set monthly occurrance"
        TYPE    = None
        ACTION  = 'store_true'


    class SET_REAL:
        SHORT_ARG   = None
        LONG_ARG    = "real"
        HELP    = "work on real list"
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


class LOMS:
    EXPCTD = 'expected'
    REAL    = 'real'