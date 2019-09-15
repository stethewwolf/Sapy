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
import sapy_modules.core.constants as SapyConstants

__instance = None

def getConfig():
    global __instance

    if not __instance :
        __instance = configparser.ConfigParser()
        __instance['private'] = {
                'home' : os.path.join( os.environ['HOME'], SapyConstants.APP.HOME),
                'conf' : os.path.join( os.environ['HOME'], SapyConstants.APP.HOME, SapyConstants.APP.CONF_FILE ),
                'data' : os.path.join( os.environ['HOME'], SapyConstants.APP.HOME, SapyConstants.DB.FILE )
            }  

        if os.path.exists(
            __instance['private']['conf'] 
        ) :
            __instance.read( __instance['private']['conf'] ) 

    return __instance

def save( cfg ):
    with open( cfg['private']['conf'], 'w') as file:
        cfg.write(file)