# Sapy
# Copyright (C) 2018 stefano prina <stefano-prina@outlook.it> <stethewwolf@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import configparser,os
import  sapy.core.constants as SapyConstants
from datetime import datetime

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
