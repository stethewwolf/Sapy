#!/usr/bin/env python3
#
# Sapy
# Copyright (C) 2018 stefano prina <stethewwolf@posteo.net>
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

from sapy.commands.commandline_parser import CommandLine_Parser
from sapy.utils import loggers as LoggerFactory
import sapy.utils.db as db_iface


def run():
    # setup logging service
    logger = LoggerFactory.getLogger('sapy')

    # the app starts
    logger.debug('sapy start')

    clp = CommandLine_Parser()

    command_list = clp.parse()

    logger.debug('start run commands')
    for cmd in command_list:
        logger.debug('running command ' + str(cmd.__class__))
        cmd.run()

    # close db connection
    db_iface.close()

    # the app ends
    logger.debug('sapy end')


if __name__ == "__main__":
    run()
