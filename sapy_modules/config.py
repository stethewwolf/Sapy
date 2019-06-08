#
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

import configparser,os

class Config:
    _APP_HOME = '.sapy'
    _CONF_FILE = 'conf.ini'
    _DATA_FILE = 'conf.ini'
    
    instance = None

    def __init__(self):
        if not __Config.instance:
            Config.instance = configparser.ConfigParser()

            if os.path.exists(
                os.path.join( os.environ['HOME'], Config._APP_HOME, Config._DATA_FILE )
            ) :
                Config.instance.read(
                        os.path.join( 
                            os.environ['HOME'], Config._APP_HOME, Config._DATA_FILE 
                            )
                    )


            Config.instance['private']['home'] = os.path.join( os.environ['HOME'], '' )
            Config.instance['private']['conf'] = os.path.join( os.environ['HOME'], '.sapy', 'conf.ini' )
            Config.instance['private']['db'] = os.path.join( os.environ['HOME'], '.sapy', 'data.sqlite' )

            
    def __getattr__(self, name):
        return getattr(self.instance, name)
