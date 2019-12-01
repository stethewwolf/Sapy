from sapy_modules.commands.command import Command
import sapy_modules.core.mlogger as LoggerFactory
from sapy_modules.commands.setter import SetCause, SetValue, SetLom, SetDate, SetStart, SetEnd
from sapy_modules.commands.run import RunAdd, RunList
import sapy_modules.sapy.objectives as objs
import sapy_modules.sapy.lom as loms
from datetime import datetime, timedelta

class EndWeek(Command):
    short_arg = None
    long_arg = 'end-week'
    cmd_help = 'ends the week, and insert real movement'
    cmd_type = None
    cmd_action = 'store_true'

    def __init__(self, param=None):
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))
    
    def run(self):
        self.logger.debug("start")
        se = (datetime.today()-timedelta(days=7)).date()
        ed = datetime.today().date()

        print("objectives for this month are:")
        SetStart( str( se ) )
        SetEnd( str( ed ) )
        RunList("obj")
        
        # TODO: add ask for import them from file

        print("outcomes for this week:")
        for m in loms.get_lom(name="expected").get_moms():
           if m.time <= ed and m.time > se and m.value < 0 :
                print("|\t{}\t|\t{}\t|\t{}\t|".format(m.cause,m.value,m.time))

        print("did you have incomes this week?[Y/n]")
        r = '.'
        while r != 'Y' and r != 'n' and '' != r:
            r = input().strip() 

        if r == 'Y' or r == '':
            flag = True
            while flag:
                SetLom("real")
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

        print("outcomes for this week:")
        for m in loms.get_lom(name="expected").get_moms():
           if m.time <= ed and m.time > se and m.value < 0 :
                print("|\t{}\t|\t{}\t|\t{}\t|".format(m.cause,m.value,m.time))

        print("did you have outcomes this week ?[Y/n]")
        r = '.'
        while r != 'Y' and r != 'n' and '' != r:
            r = input().strip() 

        if r == 'Y' or r == '':
            flag = True
            while flag:
                SetLom("real")
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
