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

from string import Template
import os
from pathlib import Path

# app values
__app_name__ = 'sapy'
__app_description__ = 'App implementing the Japanese Kakeibo method'
__version__ = '2.3.1'
__author__ = 'Stefano Prina'
__author_email__ = 'stethewwolf@posteo.net'
__app_url__ = 'https://sapy.stethewwolf.eu'
__app_license__ = 'GPL3'

# app files names
__db_file_name__ = 'data.sqlite3'
__conf_file_name__ = 'conf.ini'
__sapy_home__ = '.sapy'

# db
__db_create_app_meta__ = """
    CREATE TABLE IF NOT EXISTS  "app_meta" (
        "id"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        "key"  TEXT NOT NULL UNIQUE,
        "value" TEXT NOT NULL
    ) """

__db__populate_app_meta__ = """
        INSERT INTO "app_meta" ("key","value") VALUES ("app_version",?)
    """

# frequencies
__frequency_tag__ = 'frequency'
__frequency_daily__ = 'daily'
__frequency_monthly__ = 'monthly'
__frequency_weekly__ = 'weekly'
__frequency_none__ = None

# gui
__glade_files_path__ = [
    os.path.join(
        os.environ["HOME"], 
        '.local', 'share', 'sapy', 'sapy.glade'),
    '/app/share/sapy/sapy.glade',
    'sapy/gtk/sapy.glade',
    os.path.join(Path(__file__).parents[2], 'gtk', 'sapy.glade'),
    os.path.join(Path(__file__).parents[1], 'gtk', 'sapy.glade')
]

# dates
__date_formats__ = [
            '%d-%m-%Y',
            '%Y-%m-%d',
            '%d-%m-%y',
            '%y-%m-%d',
            '%c'
            ]

__date_separators__ = [
        '-',
        ' ',
        '/',
        '|',
        ':',
        '.'
        ]
