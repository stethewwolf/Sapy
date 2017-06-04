#!/usr/bin/python
#
#   File : icli.py
#   Author : stefano prina
#
# MIT License
#
# Copyright (c) 2017 Stefano Prina <stethewwolf@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
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

import datetime
from mom import Mom

_DEBUG_ = False


def list_cmd(data, cmd):
    # TODO: check cmd[0]
    if cmd[0] == "help" or cmd == "list":
        print ("""
        usage :
            list loms
            list moms <lom>
        """)
    elif cmd[0] == "loms":
        for key in data.list_lom():
            print (key)
    elif cmd[0] == "moms":
        # TODO: ask for day , default today
        # TODO: ask for number of day , default 1 day
        # TODO: check fot cmd[1]
        if cmd[1] in data.list_lom():
            for key in data.list_moms(cmd[1]):
                print key.to_string()
        else:
            print (cmd[1] + " not found ")

    return True


def add_cmd(data, cmd):
    # TODO: check cmd[0]
    if cmd[0] == "help" or cmd == "add":
        print ("""
        usage :
            add lom
            add mom <lom>

            data will be asked step by step
        """)
    if cmd[0] == "lom":
        name = raw_input("insert name : ")
        data.new_lom(name)
    if cmd[0] == "mom":
        print (" not yet implemented ")
        price = raw_input("     insert price : ")
        cause = raw_input("     insert cause")
        agent = raw_input("     insert agent")
        payee = raw_input("     insert payee")
        day = raw_input("     insert day [dd] : ")
        month = raw_input("     insert month [mm] : ")
        year = raw_input("     insert year [yyyy] : ")
        if len(cmd) == 3:
            number = cmd[2]
        # TODO: check date imput values
        date = None
        if year and month and day:
            date = datetime.date(year,month,day)
        # TODO : choise time
        mom = Mom()
        if price:
            mom.price(float(price))
        if cause:
            mom.cause(cause)
        if agent:
            mom.agent(agent)
        if payee:
            mom.payee(payee)
        if date:
            mom.date(date)
        # TODO: ask for multiple insertions
        if cmd[1]:
            if len(cmd) == 3:
                data.add_n_mom(lom_name=cmd[1],mom=mom,n=number)
            else:
                data.add_mom(lom_name=cmd[1],mom=mom)
        else:
            return False
    return True


def load_cmd(data, cmd):
    print (" not yet implemented ")
    return True


def remove_cmd(data, cmd):
    print (" not yet implemented ")
    return True


def display_cmd(data, cmd):
    print (" not yet implemented ")
    return True


def help_cmd(data, cmd):
    print """
        Available command :
            help : display this message
            quit : exit program
            list : list moms or loms
            add : add moms
            display : display a graph
            remove : remove moms
            load : load data from file
    """
    return True


def quit_cmd(data, cmd):
    if _DEBUG_:
        print ("__ Icli __ : running quit ")
    return False


class Icli(object):
    def __init__(self, data):
        if _DEBUG_:
            print ("__ Icli __ : init ")

        self.commands = {
            'list': list_cmd,  # Command("list", list, "show moms"),
            'add': add_cmd,  # Command("add", add, "add moms"),
            'load': load_cmd,  # Command("load", load, "load moms"),
            'quit': quit_cmd,  # Command("quit", quit, "exit from program"),
            'help': help_cmd,  # Command("help", help, "print help"),
            'display': display_cmd,
            'remove': remove_cmd  # Command("remove", remove, "remove moms"commands)
        }
        if _DEBUG_:
            print ("__ Icli __ : commands ")
            print (self.commands)

        self.data = data

    def run(self):
        flag = True
        print ("available command")
        print self.commands.keys()
        print ("type <command> help to get more info")

        while flag:
            # TODO: check if cmd string is empty
            cmd = raw_input(" sapy => ").split()
            if cmd[0] in self.commands.keys():
                if _DEBUG_:
                    print (cmd[0] + " : this is  a valid command")
                if len(cmd) > 1:
                    flag = self.commands[cmd[0]](self.data, cmd[1:])
                else:
                    flag = self.commands[cmd[0]](self.data, cmd[0])
            else:
                print (cmd[0] + " : this is not a valid command")
        pass
