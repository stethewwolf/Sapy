#   Author : stefano prina 
#
# MIT License
# 
# Copyright (c) 2017 Stefano Prina <stethewwolf@gmail.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without sestriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
#     The above copyright notice and this permission notice shall be included in all
#     copies or substantial portions of the Software.
# 
#     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#     IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#     FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#     AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#     LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#     OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#     SOFTWARE.

import sapy_modules.config as SingleConfig
import os, sqlite3
import sapy_modules.mlogger as loggerFactory

class SetUpEnv( object ):
    def __init__( self ):
        self.cfg = SingleConfig.getConfig()
        self.logger = loggerFactory.getLogger( str( self.__class__ ))

    def run( self ):
        self.home_app()
        self.database()
        pass
    
    def home_app(self):
        if not os.path.exists( self.cfg['private']['home'] ) :
            os.makedirs( self.cfg['private']['home'] )
            SingleConfig.save( self.cfg )
            self.logger.debug("created app home dir")
        else:
            self.logger.debug("app home dir yet present")

    def database(self):
        print(self.cfg['private']['data'])
        if not os.path.exists( self.cfg['private']['data'] ) :
            con = sqlite3.connect(self.cfg['private']['data'])
            cur = con.cursor()

            cur.execute( self.cfg['private']['db_create_table_days'  ] ) 
            cur.execute( self.cfg['private']['db_create_table_month' ] )
            cur.execute( self.cfg['private']['db_create_table_year'  ] )
            cur.execute( self.cfg['private']['db_create_table_list'  ] )
            cur.execute( self.cfg['private']['db_populate_table_list'] )
            cur.execute( self.cfg['private']['db_create_table_moms'  ] )
            cur.execute( self.cfg['private']['db_create_table_ops'   ] )

            con.commit()
            cur.close()

