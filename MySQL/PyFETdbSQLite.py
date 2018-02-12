# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 23:15:19 2016

@author: aguimera
"""

import deepdish as dd
import numpy as np
import matplotlib.pyplot as plt
import gc
import sqlite3 as sql
import pickle
from PyFET.DataStructures import *
from PyFET.ExportData import *

class PyFETdb():
    def __init__(self,DBFile):
        sql.register_adapter(bool, int)
        sql.register_converter("BOOLEAN", lambda v: bool(int(v)))
        
        self.DBFileName = DBFile
        self.con = sql.connect(DBFile,isolation_level=None)
        self.cur = self.con.cursor()
    
    def CreateTables(self):
        # Make some fresh tables using executescript()
        self.cur.executescript('''
        DROP TABLE IF EXISTS ACcharact;
        DROP TABLE IF EXISTS DCcharact;
        DROP TABLE IF EXISTS Wafers;
        DROP TABLE IF EXISTS Devices;
        DROP TABLE IF EXISTS Trts;
        DROP TABLE IF EXISTS Authors;
         
        CREATE TABLE `Wafers` (
            `Id`	     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            `Name`	     TEXT NOT NULL UNIQUE,
            `Masks`	     TEXT,
            `Comments`	TEXT);
        
        CREATE TABLE "Devices" (
            `id`	     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            `Name`	     TEXT NOT NULL UNIQUE,
            `Wafer_id`	INTEGER NOT NULL,
            `Comments`	TEXT);
        
        CREATE TABLE "Trts" (
            `id`	     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            `Name`	     TEXT NOT NULL UNIQUE,
            `Device_id`	INTEGER NOT NULL,
            'Wafer_id'   INTEGER NOT NULL,
            `DCMeas`     INTEGER,
            `ACMeas`     INTEGER,
            `Width`	     REAL,
            `Length`	REAL,
            `Pass`	     REAL,
            `Shape`      TEXT,
            `Comments`	TEXT);
        
        CREATE TABLE "Authors" (
            `id`	     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            `Name`	     TEXT NOT NULL UNIQUE);

        CREATE TABLE `ACcharact` (
            `id`	     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            `Trt_id`	INTEGER NOT NULL,
            `DateTime`	TEXT NOT NULL,
            `Data`	     BLOB NOT NULL ,
            `DCchatact_id`	INTEGER,
            `Wafer_id`   INTEGER NOT NULL,
            `Device_id`  INTEGER NOT NULL,
            `Author_id`  INTEGER,
            `IsOK`       BOOLEAN,
            `FileName`   TEXT,
            `Solution`	TEXT,
            `pH`	     REAL,
            `Comments`	TEXT);
        
        CREATE TABLE `DCcharact` (
            `id`	     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            `Trt_id`	INTEGER NOT NULL,
            `DateTime`	TEXT NOT NULL,
            `Data`	     BLOB NOT NULL,
            `Wafer_id`  INTEGER NOT NULL,
            `Device_id` INTEGER NOT NULL,
            `Author_id`  INTEGER,
            `IsOK`       BOOLEAN,
            `FileName`   TEXT,
            `Solution`	TEXT,
            `pH`	     REAL,
            `Comments`	TEXT);  
          
        ''')        
                
    def GetId(self, Table, Value, Field='Name', NewVals=None):
        
        query = "SELECT id FROM {} WHERE {} = ?".format(Table, Field)        
        self.cur.execute(query, (Value,))
        Res = self.cur.fetchall()
       
        if len(Res)==0:
            if NewVals:
                self.NewRow(Table=Table, Fields=NewVals)
                ID = self.cur.lastrowid
            else:
                ID = None        
        if len(Res)==1:
            ID = Res[0][0]
                
        if len(Res)>1: 
            print 'Warning', query, Res
            ID = Res[0][0]         
            
        return ID
    
    def NewRow(self, Table, Fields):
        colums = ' , '.join(Fields.keys())
        places = ' , '.join(['?']*len(Fields))
        query = "INSERT INTO {}({}) VALUES ({})".format(Table,colums,places)
        
        self.cur.execute(query,Fields.values())       

    def MultiSelect(self, Table, Conditions, FieldsOut = None, Order=None):
        
        if FieldsOut:
            Fields = ' , '.join(FieldsOut)
        else:                
            Fields = ' , '.join(Conditions.keys())
        
        Cond = ' = ? AND '.join(Conditions.keys())
        query = "SELECT {} FROM {} WHERE {} = ?".format(Fields,Table,Cond)   
        
        if Order:
            query = '{} ORDER BY {}'.format(query,Order)

        self.cur.execute(query,Conditions.values())
        
        return self.cur.fetchall()
        
    def InsertCharact(self, DCVals, Fields, ACVals=None, OptFields=None):

        Author = Fields['Author']
        Wafer = Fields['Wafer']
        Device = Fields['Device']
        Trt = Fields['Trt']
        
        Author_id = self.GetId(Table='Authors', Value=Author, 
                              NewVals={'Name': Author})
        
        Wafer_id = self.GetId(Table='Wafers', Value=Wafer, 
                              NewVals={'Name': Wafer})

        Device_id = self.GetId(Table='Devices', Value=Device, 
                              NewVals={'Name': Device,
                                       'Wafer_id':Wafer_id})
        
        Trt_id = self.GetId(Table='Trts', Value=Trt, 
                              NewVals={'Name': Trt,
                                       'Wafer_id':Wafer_id,
                                       'Device_id':Device_id})         
        
        Rows = self.MultiSelect('DCcharact',
                         {'Trt_id':Trt_id,
                          'DateTime':DCVals['DateTime'].isoformat()})
        
        if len(Rows)==0:
            NewData = {'Trt_id':Trt_id,
                       'Wafer_id':Wafer_id,
                       'Device_id':Device_id,
                       'Author_id':Author_id,
                       'Data':pickle.dumps(DCVals),
                       'DateTime': DCVals['DateTime'].isoformat()}
                       
            if 'IsOK' in DCVals: NewData['IsOK'] = DCVals['IsOK']            
            if OptFields: NewData.update(OptFields)
            
            self.NewRow(Table='DCcharact',Fields=NewData)
            DCchatact_id = self.cur.lastrowid
            
            DCMeas = len(self.MultiSelect('DCcharact',{'Trt_id':Trt_id,}))
            self.cur.execute("UPDATE Trts SET DCMeas = ? WHERE id = ?",
                             (DCMeas,Trt_id))
        else:
            print 'WARNING EXISTS', Rows
        
        if ACVals:
            Rows = self.MultiSelect('ACcharact',
                         {'Trt_id':Trt_id,
                          'DateTime':ACVals['DateTime'].isoformat()})
            if len(Rows)==0:
                NewData = {'Trt_id':Trt_id,
                           'Wafer_id':Wafer_id,
                           'Device_id':Device_id,
                           'Author_id':Author_id,
                           'DCchatact_id':DCchatact_id,
                           'Data':pickle.dumps(ACVals),
                           'DateTime': ACVals['DateTime'].isoformat()}
        
                if 'IsOK' in DCVals: NewData['IsOK'] = DCVals['IsOK']
                if OptFields: NewData.update(OptFields)
                
                self.NewRow(Table='ACcharact',Fields=NewData)
                
                ACMeas = len(self.MultiSelect('ACcharact',{'Trt_id':Trt_id,}))
                self.cur.execute("UPDATE Trts SET ACMeas = ? WHERE id = ?",
                             (ACMeas,Trt_id))
            else:
                print 'WARNING EXISTS', Rows

        self.con.commit()
        
    def GetDCTrt (self,TrtName):

        query = 'SELECT DCcharact.DateTime, DCcharact.Data, DCcharact.id from DCcharact where DCcharact.Trt_id = ? order by DCcharact.DateTime'        
        self.cur.execute(query,(TrtName,))
        
        Res = self.cur.fetchall()
        
        DCVals = {}
        for cy,re in enumerate(Res):
            DCVals['Cy{0:03d}'.format(cy)] = pickle.loads(re[1])
            
        return DCVals
            
if __name__ == '__main__':

    plt.close('all')
    

    MyDB = PyFETdb('./SQLdb/TestDb.sqlite')
#    MyDB.CreateTables()

##############################################################################
## Upload files
##############################################################################
#    plt.ioff()
#    FileNames = glob.glob('./Data/B9355O15-T3*')
#    
#    Fields = {}
#    Fields['Author'] = 'AGB'
#    Fields['Wafer'] = 'B9355O15'
#    Fields['Device'] = 'B9355O15-T3'
#
#    OptFields = {}
#    OptFields['Solution'] = 'PBS'    
#    OptFields['Comments'] = 'Trial'
#
#    for ifile, filen in enumerate(FileNames):
#        print 'Load {} {} of {}'.format(filen.split('/')[-1], ifile, len(FileNames)) 
#        
#        plt.close('all')
#        
#        DataIn = dd.io.load(filen)
#        
#        if type(DataIn)==dict:
#            DevDCVals = DataIn
#            DevACVals = None
#            
#        if type(DataIn)==tuple:
#            DevDCVals = DataIn[0]
#            DevACVals = None
#            if len(DataIn)>1:
#                DevACVals = DataIn[1]
#        
#        
#        CheckIsOK (DevDCVals,DevACVals, RdsRange = [400,10e3])
#        
#        if DevACVals:
#            FitACNoise(DevACVals,Fmin=50, Fmax=7e3)
#            InterpolatePSD(DevACVals,Points=100)
#    
#        
##        GenReportPDF (DevDCVals,DevACVals,'./Reports/{}'.format(filen.split('/')[-1]))
#        
#        OptFields['FileName'] = filen.split('/')[-1]
#
#        for ch in DevDCVals:
#            Fields['Trt'] = '{}-{}'.format(Fields['Device'],ch)
#            
#            if ch=='Gate': 
#                if 'DateTime' not in DevDCVals[ch]:
#                    DevDCVals[ch]['DateTime'] = DevDCVals['Ch02']['DateTime']
#                    
#                MyDB.InsertCharact(DCVals = DevDCVals[ch],
#                   ACVals = None,
#                   Fields = Fields,
#                   OptFields = OptFields)
#                continue       
#           
#            if DevACVals:
#                MyDB.InsertCharact(DCVals = DevDCVals[ch],
#                               ACVals = DevACVals[ch],
#                               Fields = Fields,
#                               OptFields = OptFields)  
#            else:
#                MyDB.InsertCharact(DCVals = DevDCVals[ch],
#                               ACVals = None,
#                               Fields = Fields,
#                               OptFields = OptFields)  
                
    
###############################################################################
### Get data
###############################################################################
    plt.ion()

    DataDB = MyDB.MultiSelect('DCcharact',{'Trt_id':10,'IsOk':True},
                              FieldsOut=('Data','DateTime'),Order='DateTime')

    DCVals = {}
    for cy,re in enumerate(DataDB):
        DCVals['Cy{0:03d}'.format(cy)] = pickle.loads(re[0])

    
    FigDC,AxsDC = CreateDCFigure()

    PlotDC(DCVals,AxsDC,legend=True)

    
    print 'Collect ', gc.collect()