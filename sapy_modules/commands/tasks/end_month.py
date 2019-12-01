from sapy_modules.commands.command import Command
import sapy_modules.core.mlogger as LoggerFactory
from sapy_modules.commands.setter import SetCause, SetValue, SetLom, SetDate
from sapy_modules.commands.run import RunAdd
import sapy_modules.sapy.objectives as objs
import sapy_modules.sapy.lom as loms
import sapy_modules.core.values as SapyValues
import datetime
import calendar

class EndMonth(Command):
    short_arg = None
    long_arg = 'end-month'
    cmd_help = 'ends the month'
    cmd_type = None
    cmd_action = 'store_true'

    def __init__(self, param=None):
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))
    
    def run(self):
        self.logger.debug("start")
        sd = datetime.date(
            SapyValues.get_value("date").year,
            SapyValues.get_value("date").month,
            1
        )
        
        ed = datetime.date(
            SapyValues.get_value("date").year,
            SapyValues.get_value("date").month,
            calendar.monthrange(
            SapyValues.get_value("date").year,
            SapyValues.get_value("date").month
            )[0]
        )

        print("objectives this month was:")
        for o in objs.get_objs(self.logger):
            if o.duedate.month == SapyValues.get_value("date").month:
                print("|\t{}\t|\t{}\t|".format(o.description,o.duedate))
       
        #TODO ask for complete objectives



        l_real = loms.get_lom(name="real")

        l_b = l_real.balance(start_date=sd,end_date=ed)

        l_planned = loms.get_lom(name="expected")

        p_b = l_planned.balance(start_date=sd,end_date=ed)

        print("============================")
        print("expected balance :",p_b)
        print("real balance :",l_b)
        print("============================")

        self.logger.debug("end")
