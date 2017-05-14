#!/bin/environment python
import datetime

class mom (object): # movment of money
    import datetime

    def __init__ (
        self,
        price = 0,
        direction = 1,
        cause = "not specified",
        agent = "not specified",
        payee = "not specified",
        date = datetime.date.today()
        ):
        self.price = price
        self.direction = direction
        self.cause = cause # description of money movement
        self.agent = agent # specify who move money
        self.payee = payee  # specify who recived money
        self.date = date

    def Price( self, price = None ) :
        if price :
            self.price = price
        else :
            return self.price
        return True

    def Direction ( self , direction = None ) :
        if direction :
            self.direction=direction
        else :
            return self.direction
        return True

    def Cause ( self , cause = None ) :
        if cause :
            self.cause=cause
        else :
            return self.cause
        return True

    def Agent ( self, agent = None ) :
        if agent :
            self.agent = agent
        else :
            return self.agent
        return True

    def Payee (self, payee = None ) :
        if payee :
            self.payee = payee
        else :
            return self.payee
        return True

    def Date( self, date = None ) :
        if date :
            self.date = date
        else :
            return self.date
        return True

    def toString ( self , separator = " " ) :
        return str(self.direction)+separator+str(self.price)+separator+self.cause+separator+self.agent+separator+self.payee+separator+self.date.isoformat()

    def toJsonable ( self ) :
        tmpData = {
            'price' : self.price ,
            'direction' : self.direction ,
            'cause' : self.cause ,
            'agent' : self.agent ,
            'payee' : self.payee ,
            'date' : {
                'year' : self.date.year ,
                'month' : self.date.month ,
                'day' :  self.date.day ,
            } ,
        }
        return tmpData

    def fromJsonable (self , JString ) :
        self.price = JString['price']
        self.direction = JString['direction']
        self.cause = JString['cause']
        self.agent = JString['agent']
        self.payee = JString['payee']
        self.date = datetime.date(JString['date']['year'],JString['date']['month'],JString['date']['day'])
        pass

    def Id ( self ) :
        return self.id

    def compare (self):
        pass
