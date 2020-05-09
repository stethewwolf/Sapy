# Sapy
# Copyright (C) 2018 stefano prina <stethewwolf@null.net> <stethewwolf@gmail.com>
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

import logging, sys

loggerList = []
logLevel = logging.INFO
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def getLogger( name ):
    global logLevel
    logger = logging.getLogger( name )
    logger.setLevel(logLevel)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logLevel)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    loggerList.append(logger)

    return logger

def setLogFile( file ):
    handler = logging.StreamHandler(file)
    handler.setLevel(logLevel)
    handler.setFormatter(formatter)

    for l in loggerList:
        l.addHandler(handler)
