#!/bin/environment python
from mom import *

class lom (object): # list of movements
    import datetime
    import mom

    def __init__ (
        self,
        name = "list of movements",
        ):
        self.name = name
        self.movements = [] # array ordinato per data
        self.balance = 0
        self.pos_sum = 0
        self.neg_sum = 0

    def insert (self, m) :
        self.movements.append(m)
        self.movements.sort(key=lambda x : x.date, reverse=False )
        self.balance = self.balance + m.direction*m.price
        if m.direction >= 0 :
            self.pos_sum += m.price
        else :
            self.neg_sum += m.price

    def remove ( self , m) :
        try:
            self.movements.remove(mom)
            self.balance -= m.direction*m.price
            if m.direction >= 0 :
                self.pos_sum -= m.price
            else :
                self.neg_sum -= m.price
        except :
            print("impssible delete " + mom)

    def toJsonable ( self ) :
        lomJsonable = {
            'name' : self.name,
            'movements' : [],
            'balance' : self.balance,
            'pos_sum' : self.pos_sum,
            'neg_sum' : self.neg_sum,
        }

        for mom in self.movements :
            jmom = mom.toJsonable()
            lomJsonable['movements'].append(jmom)

        return lomJsonable

    def fromJsonable( self, jsonable ) :
        self.name=jsonable['name']

        tmp_pos_sum = 0
        tmp_neg_sum = 0

        for jmom in jsonable['movements'] :
            newMom = mom()
            newMom.fromJsonable(jmom)

            if newMom.direction >= 0 :
                tmp_pos_sum += newMom.price
            else :
                tmp_neg_sum += newMom.price

            self.movements.append(newMom)

        self.movements.sort(key=lambda x : x.date, reverse=False )

        if tmp_pos_sum != jsonable['pos_sum'] :
            print("something went wrong whit pos_sum, using fresh calculated one")
            self.pos_sum = tmp_pos_sum
        else :
            self.pos_sum = jsonable['neg_sum']

        if tmp_neg_sum != jsonable['neg_sum'] :
            print("something went wrong whit neg_sum, using fresh calculated one")
            self.neg_sum = tmp_neg_sum
        else :
            self.neg_sum = jsonable['neg_sum']

    def findOnDate ( self, date ) :
        return [ m for m in self.movements if m.date == date ]

    def getInPeriod ( self, startDate, timeDelta ) :
        return [ m for m in self.movements if ( (m.date >= startDate ) and ( m.date <= startDate+timeDelta ) )]

    def balanceAtDay ( self, startDate, endDate, baseBalance=0 ):
        balance = 0
        if baseBalance != 0 :
            balance = baseBalance

        for m in self.movements :
            if m.date < endDate and m.date >= startDate:
                #print m.direction*m.price
                balance += m.direction*m.price

        return balance
