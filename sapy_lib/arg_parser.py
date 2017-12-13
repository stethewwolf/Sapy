#!/usr/bin/env python
#
#   File : arg_parse.py
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

import argparse
from sapy_lib.icli import Icli
from sapy_lib.gui import gui

_DEBUG_ = True


class Master(object):
    def __init__(self, name=None, version=None, description=None, data=None):
        if _DEBUG_:
            print ("__ init Master __ ")

        self.data = data
        self.parser = argparse.ArgumentParser(prog=name,  description=description)
        self.icli = Icli(data)
        self.gui = gui(self.data)

        # setting parameter 
        ## cli - command line interface 
        self.parser.add_argument('--cli', action='store_true', help='list moms')

        ## icli - interactive command line interface
        self.parser.add_argument('--icli', action='store_true', help='list moms')

        ## gui - graphical user interface
        self.parser.add_argument('--gui', action='store_true', help='list moms')

    def parse(self):
        if _DEBUG_:
            print ("__ parse Master __ ")

        self.arguments = self.parser.parse_args()

    def run(self):
        if _DEBUG_:
            print ("__ run Master __")

        if self.arguments.cli:
            print (" passed --cli : not yet implemented")
        if self.arguments.icli:
            self.icli.run()
        if self.arguments.gui:
            print (" passed --gui : working in progress")
            self.gui.run()

# from sapi_lib.lom import lo
# from sapi_lib.mom import *

# import csv,logging,os,json,argparse,datetime,
# import matplotlib.pyplot as plt


### parsing arguments
# parser.add_argument('-a', metavar="val", type=float, nargs='+', help='add movement of money , refered to today')
# parser.add_argument('-c', metavar="cause", help='specify cause')
# parser.add_argument('--real', dest='lom',  action='store_const', const=moms['real_moms'], default=moms['real_moms'], help='add a real movement [default]')
# parser.add_argument('--expc', dest='lom',  action='store_const', const=moms['expected_moms'], default=moms['real_moms'], help='add a expc movement [default=real]')
# parser.add_argument('-l',action='store_true', help='list moms')
# parser.add_argument('-p',action='store_true', help='insert period')
# parser.add_argument('-i', metavar="file_name", help='import from file_name')
# parser.add_argument('-sd', metavar="dd-mm-yyyy", help='day start dd-mm-yyyy')
# parser.add_argument('-ed', metavar="dd-mm-yyyy", help='day end dd-mm-yyyy')
# parser.add_argument('-b', action='store_true', help='print balance')
#
# args = parser.parse_args()
# print args
# if args.a  and not args.p:
#    print "one"
#    newmom = mom()
#    if args.a >= 0 :
#        newmom.Price(args.a[0])
#        newmom.Direction(1)
#    else :
#        newmom.Price(-1*args.a)
#        newmom.Direction(-1)
#    newmom.Date(datetime.date.today())
#    args.lom.insert(newmom)
#    args.a = None
#
# if args.l :
#    today = datetime.date.today()
#    minusDelta = datetime.timedelta(days=-15)
#    plusDelta = datetime.timedelta(days=30)
#    print("start from : "+str(today)+" to : "+str(today+minusDelta+plusDelta))
#    for entry in args.lom.getInPeriod(today+minusDelta, plusDelta ) :
#        print( entry.toString() )
#
#    print "balance : "+str(args.lom.balance)
#
# if args.b :
#    realData = []
#    expectedData = []
#    startDate = datetime.date.today() - datetime.timedelta(days=30)
#    endDate = datetime.date.today() + datetime.timedelta(days=30)
#
#    real_baseBalance = moms["real_moms"].balanceAtDay(datetime.date.min,startDate)
#   realData.append(real_baseBalance)
#    expc_baseBalance = moms["expected_moms"].balanceAtDay(datetime.date.min,startDate)
#    expectedData.append(expc_baseBalance)
#
#    while startDate <= endDate :
#        real_baseBalance = moms["real_moms"].balanceAtDay(startDate,startDate+datetime.timedelta(days=1),real_baseBalance)
#        expc_baseBalance = moms["expected_moms"].balanceAtDay(startDate,startDate+datetime.timedelta(days=1),expc_baseBalance)
#        realData.append(real_baseBalance)
#        expectedData.append(expc_baseBalance)
#
#        startDate += datetime.timedelta(days=1)
#
#    plt.plot(expectedData)
#    plt.plot(realData)
#    plt.axvline(x=30,color='k', linestyle='--')
#    plt.show()
#
# if args.i and os.path.isfile(args.i):
#    fp=open(args.i,"r")
#    reader = csv.reader(fp)
#    for row in reader :
#        tmp = row[2].replace(".","")
#        tmp = tmp.replace(",",".")
#        try :
#            price = float(tmp)
#            dir=-1
#            if price >= 0 :
#                dir = 1
#
#            newmom = mom(dir*price,dir,row[1])
#            date_array = row[0].split("/")
#            date = datetime.date(int(date_array[2]),int(date_array[1]),int(date_array[0]))
#            newmom.Date(date)
#            try:
#                args.lom.insert(newmom)
#            except :
#                print("cat append mom to")
#        except :
#            print(str(type(row[2])) + " | " +row[2]+" is not floatable")
#
# if args.a and args.p and args.sd and args.ed :
#    sd = datetime.date(int(args.sd.split("-")[2]),int(args.sd.split("-")[1]),int(args.sd.split("-")[0]))
#    ed = datetime.date(int(args.ed.split("-")[2]),int(args.ed.split("-")[1]),int(args.ed.split("-")[0]))
#
#    while (( ed - sd ) >= datetime.timedelta(days=0)  ) :
#        newmom = mom()
#        if args.a >= 0 :
#            newmom.Price(args.a[0])
#            newmom.Direction(1)
#        else :
#            newmom.Price(-1*args.a)
#            newmom.Direction(-1)
#
#        newmom.Date(sd)
#        args.lom.insert(newmom)
#        print newmom.toString()
#        print sd
#        sd += datetime.timedelta(days=1)
#
