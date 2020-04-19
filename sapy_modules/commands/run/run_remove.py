#
#   File : run_graph.py
#   Author : stefano prina <stethewwolf@null.net>
#

from sapy_modules.core import LoggerFactory
from sapy_modules.core import SingleConfig
from sapy_modules.core import SapyConstants
from sapy_modules.commands.command import Command
import datetime
import sapy_modules.sapy.lom as loms
import sapy_modules.sapy.tags as tags
import sapy_modules.sapy.objectives as objs
import sapy_modules.core.values as SapyValues

class RunRemove ( Command ):
    short_arg = 'r'
    long_arg = 'rm'
    cmd_help = 'remove target : lom | mom | tag | obj'
    cmd_type = str
    cmd_action = None

    def __init__( self, param ):
        super().__init__()
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))
        self.target = param

    def run( self ):
        self.logger.debug("start")
        
        self.id2rm = SapyValues.get_value('id')

        if self.target == 'mom' :
            self.rm_mom()
        elif self.target == 'lom':
            self.rm_lom()
        elif self.target == 'obj':
            self.rm_obj()
        elif self.target == 'tag':
            self.rm_tag()
        else :
            print('invalid targget :{}'.format(self.target))

        self.logger.debug("end")

    def rm_mom(self):
        l = SapyValues.get_value('lom')
        mlist = l.get_moms( id = self.id2rm )
        mlist[0].delete()

    def rm_lom(self):
        l = loms.get_lom( id=self.id2rm )

        mlist = l.get_moms()

        for m in  mlist :
            m.delete()

        l.delete()

    def rm_tag(self):
        t = tags.get_tag(id=self.id2rm)
        t.delete()
        pass

    def rm_obj(self):
        o = objs.get_obj(self.id2rm, self.logger)
        o.delete()
        pass
