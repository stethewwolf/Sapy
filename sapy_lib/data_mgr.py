#!/usr/bin/python

from lom import *
from mom import *
import json,os

_DEBUG_ = True

class Data_mgr ( object ) :
    if _DEBUG_ :
        print ("__ Data mgr __ : init")
    def __init__ ( self  , datafile ) :
        self.loms = list()
        self.datafile = datafile

    def new_lom ( self, name  ) :
        tmp = lom()
        tmp.name = name
        self.loms.append(tmp)

    def remove ( self ) :
        pass

    def from_jsonable ( self, raw ):
        for item in raw :
            tmp = lom ();
            tmp.fromJsonable(item)
            self.loms.append(tmp)

        if _DEBUG_ :
            print ( self.loms)

    def to_jsonable ( self ):
        tmp = []
        for lom in self.loms :
            tmp.append(lom.toJsonable())

        return tmp

    def list_loms(self):
        return [ l.name for l in self.loms ]

    def list_moms(self,lom):
        return [l for l in self.loms if l.name==lom ][0].movements
        #return  self.loms[lom].movements

    def load(self):
        if _DEBUG_ :
            print ("__ Data Mgr __: load_saved_data : \n" + os.path.abspath( self.datafile ))

        if os.path.isfile( os.path.abspath( self.datafile ) ) :
            datafile = open( os.path.abspath( self.datafile ), "r")
            rawdata = json.load( datafile )
            datafile.close()
            for tmp_data in rawdata :
                tmp_lom = lom()
                tmp_lom.fromJsonable( tmp_data )
                self.loms.append(tmp_lom)

        elif _DEBUG_ :
            print (" no file " +  os.path.abspath( self.datafile ))

        else :
            print ( "no file %s available", self.datafile )


    def dump(self):
        rawdata = []
        for tmp_lom in self.loms :
            rawdata.append( tmp_lom.to_jsonable())

        if os.path.isfile( os.path.abspath( self.datafile ) ) :
            datafile = open( os.path.abspath( self.datafile ), "w")
            json.dump(rawdata,datafile)
            datafile.close()
        pass