
import sqlite3
from sapy_modules.core import SingleConfig

connession = None

def open():
    global  connession
    if not connession :
        connession = sqlite3.connect( SingleConfig.getConfig()['private']['data'] )
    pass

def get_cursor():
    global connession

    if not connession :
        open()

    return connession.cursor()

def commit():
    global connession

    if connession :
        connession.commit()

def close():
    global connession

    if connession :
        connession.close()

