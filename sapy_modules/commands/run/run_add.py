
#   File : run_add.py
#   Author : stefano prina <stethewwolf@null.net>
#

from sapy_modules.core import LoggerFactory
from sapy_modules.core import SingleConfig
from sapy_modules.core import SapyConstants
from sapy_modules.commands.command import Command
import sapy_modules.core.values as SapyValues
import sapy_modules.sapy.lom as loms
import sapy_modules.sapy.mom as moms
import sapy_modules.sapy.tags as tags
import sapy_modules.sapy.objectives as objs
import datetime


class RunAdd(Command):
    short_arg   = 'a'
    long_arg    = 'add'
    cmd_help    = 'add new item, takes : mom | lom | obj | tag'
    cmd_type    = str
    cmd_action  = None

    def __init__(self, param):
        super().__init__()
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))
        self.target = param

    
    def run(self):
        self.logger.debug('start')

        if self.target == 'mom' :
            self.add_mom()
        elif self.target == 'lom':
            self.add_lom()
        elif self.target == 'obj':
            self.add_obj()
        elif self.target == 'tag':
            self.add_tag()
        else :
            print('invalid targget :{}'.format(self.target))

        self.logger.debug("end")

    def add_mom(self):
        mlist=[]
        l = loms.get_lom( SapyValues.get_value('lom') )

        sd = SapyValues.get_value('start_date')
        ed = SapyValues.get_value('end_date')
        f = SapyValues.get_value('frequency')

        if sd != ed and ed > sd and f :
            if f == SapyConstants.FREQUENCY.DAILY:
                step = datetime.timedelta(days=1)

            if f == SapyConstants.FREQUENCY.WEEKLY:
                step = datetime.timedelta(days=7)

            if f == SapyConstants.FREQUENCY.MONTHLY:
                step = datetime.timedelta(days=30)
            
            itr = datetime.timedelta(days=0)

            while itr + sd <= ed :
                mlist.append( moms.Mom ( 
                    value = SapyValues.get_value( 'value' ),
                    cause = SapyValues.get_value( 'cause' ),
                    time = sd + itr 
                    )        
                )

                itr += step

        else:
            mlist.append( moms.Mom ( 
                value = SapyValues.get_value( 'value' ),
                cause = SapyValues.get_value( 'cause' ),
                time = sd 
                )        
            )

        l.add(mlist)

        print ('Lom')
        print('------------------------------')
        print ('|\tid\t|\tname\t|')
        print('|\t{}\t|\t{}\t|'.format(l.id,l.name))
        print('------------------------------')
        print ('New Moms')
        print('------------------------------')
        print ('|\tid\t|\tvalue\t|\tcause\t|\tdate\t|')
        for m in mlist:
            print ('|\t{}\t|\t{}\t|\t{}\t|\t{}\t|'.format(m.id,m.value,m.cause,m.time))
        print('------------------------------')
    
    def add_lom(self):
        l = loms.Lom(name=SapyValues.get_value('name')) 
        print ('New Lom')
        print('------------------------------')
        print ('|\tid\t|\tname\t|')
        print('|\t{}\t|\t{}\t|'.format(l.id,l.name))
        print('------------------------------')

    def add_obj(self):
        ed = SapyValues.get_value('end_date')
        o = objs.Objective(description=SapyValues.get_value('cause'),duedate=ed) 
        print ('New Objective')
        print('------------------------------')
        print ('|\tid\t|\tdescription\t\t|\tdue date\t|')
        print('|\t{}\t|\t{}\t|\t{}\t|'.format(o.id,o.description,o.duedate))
        print('------------------------------')
    
    def add_tag(self):
        l = tags.Tag(name=SapyValues.get_value('name')) 
        print ('New Tag')
        print('------------------------------')
        print ('|\tid\t|\tname\t|')
        print('|\t{}\t|\t{}\t|'.format(l.id,l.name))
        print('------------------------------')