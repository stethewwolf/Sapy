
from sapy_modules.commands.command import Command
import sapy_modules.core.mlogger as LoggerFactory
from sapy_modules.commands.setter import SetCause, SetValue, SetLom, SetDate
from sapy_modules.commands.run import RunAdd
import sapy_modules.sapy.objectives as objs
import sapy_modules.sapy.lom as loms
from datetime import datetime

class NewMonth(Command):
    short_arg = None
    long_arg = 'new-month'
    cmd_help = 'start a new month'
    cmd_type = None
    cmd_action = 'store_true'

    def __init__(self, param=None):
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))
    
    def run(self):
        self.logger.debug("start")
        print("objectives for next month are:")
        for o in objs.get_objs(self.logger):
            if o.duedate.month == datetime.today().month:
                print("|\t{}\t|\t{}\t|".format(o.description,o.duedate))

        print("do you want add objectives for this new month ?[Y/n]")
        r = '.'
        while r != 'Y' and r != 'n' and '' != r:
            r = input().strip() 

        if r == 'Y' or r == '':
            flag = True
            while flag:
                SetCause(input("insert description:").strip()).run()
                date = input("insert due date:").strip()
                if len(date) > 8:
                    SetDate(date).run()
                RunAdd('obj').run()
                r = input('continue? [Y/n]').strip()
                if r != 'Y' and r != '':
                    flag=False
        
        print("incomes for next month are:")
        for m in loms.get_lom(name="expected").get_moms():
           if m.time.month == datetime.today().month and m.value > 0 :
                print("|\t{}\t|\t{}\t|\t{}\t|".format(m.cause,m.value,m.time))

        print("are you aware if incomes for the next month ?[Y/n]")
        r = '.'
        while r != 'Y' and r != 'n' and '' != r:
            r = input().strip() 

        if r == 'Y' or r == '':
            flag = True
            while flag:
                SetLom("expected")
                SetCause(input("insert cause:").strip()).run()
                SetValue(input("insert value:").strip()).run()
                date = input("insert due date:").strip()
                if len(date) > 8:
                    SetDate(date).run()
                RunAdd('mom').run()

                r = input('continue? [Y/n]').strip()
                if r != 'Y' and r != '':
                    flag=False

        self.logger.debug("end")

        print("outcomes for next month are:")
        for m in loms.get_lom(name="expected").get_moms():
           if m.time.month == datetime.today().month and m.value < 0 :
                print("|\t{}\t|\t{}\t|\t{}\t|".format(m.cause,m.value,m.time))


        print("are you aware if outcomes for the next month ?[Y/n]")
        r = '.'
        while r != 'Y' and r != 'n' and '' != r:
            r = input().strip() 

        if r == 'Y' or r == '':
            flag = True
            while flag:
                SetLom("expected")
                SetCause(input("insert cause:").strip()).run()
                SetValue(input("insert value:").strip()).run()
                date = input("insert due date:").strip()
                if len(date) > 8:
                    SetDate(date).run()
                RunAdd('mom').run()

                r = input('continue? [Y/n]').strip()
                if r != 'Y' and r != '':
                    flag=False

        self.logger.debug("end")

        