#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 00:02:49 2018

@author: aguimera
"""

import numpy as np
import matplotlib.pyplot as plt
import itertools as it
import pandas as pd


def TextFileReader(FileName):
    FileIn = open(FileName, 'r')

    State = 'Header'
    HeaderInfo = ''
    HeadL = None
    for nl, line in enumerate(FileIn):
        if State == 'Header':
            HeaderInfo = HeaderInfo + line
            if line.startswith('Nb header lines'):
                HeadL = int(line.split(':')[1])-2
            if HeadL is not None:
                if nl == HeadL:
                    State = 'Footer'
        elif State == 'Footer':
            State = 'Values'
            Data = {}
            Data['HeaderInfo'] = HeaderInfo
            line = line.replace('\r', '')
            line = line.replace('\n', '')
            Fields = line.split('\t')
            SortDict = {}
            for col, f in enumerate(Fields):
                SortDict.update({col: f})
                Data.update({f: np.array([])})
        elif State == 'Values':
            line = line.replace(',', '.')
            line = line.replace('\r', '')
            line = line.replace('\n', '')
            Dats = line.split('\t')
            for col, d in enumerate(Dats):
                field = SortDict[col]
                v = Data[field]
                df = float(d)
                v = np.hstack([v, df]) if np.size(v) else np.array([df])
                Data[field] = v

    return Data


class MpytDataBase(object):
    PropRemoveChars = ('-', '(', ')', '<', '>', ' ', '.', '|')

    def __init__(self, FileName, DataDict=None):
        if DataDict is None:
            DataDict = TextFileReader(FileName)

        Units = {}
        for k, v in DataDict.iteritems():
            k = k.split('/')
            prop = k[0]
            for char in self.PropRemoveChars:
                prop = prop.replace(char, '')
            if len(k) > 1:
                Units.update({prop: k[1]})
            self.__setattr__(prop, v)
        self.__setattr__('Units', Units)
   
    
#Scan rate --- To stabilize
    def getScanRate(self):
        dU = np.diff(self.Ewe)
        dt = np.diff(self.time)
        self.ScanRate = round(np.mean(abs(dU/dt)*1000), 0)    

    
#For a pure capacitor Icapacitive = C * dU/dt --> C = Icapacitive /(dU/dt)
#Icapacitive taken from the mean of the +/-I at the center of the potential window    
    def getCap(self): 
        Capacitance = []
        area = 5e-6
        ScanRate = self.ScanRate
        
        data = {'I': self.I, 'Ewe': self.Ewe, 'cyclenumber': self.cyclenumber}
        df = pd.DataFrame(data)  
        
        EweStep = abs(df['Ewe'][1] - df['Ewe'][0]) #Ewe error
        dfCycles = df.groupby('cyclenumber')   
        
        for cycle in dfCycles: #for each cycle
            dfCyData = cycle[1]
            PotWin = [max(dfCyData['Ewe']), min(dfCyData['Ewe'])] 
            CenterPotWin = PotWin[0] + PotWin[1] #center of PW
            
            I_cap0 = []
            n = 0
                
            while(len(I_cap0) < 2):
                n = n + 1
                 #selects values > PotWin center
                condition1 = dfCyData['Ewe'] > CenterPotWin - EweStep * n
                
                #selects values < PotWin center
                condition2 = dfCyData['Ewe'] < CenterPotWin + EweStep * n 
                
                #2 values, one + and one - corresponding to the 2 Icap
                I_cap0 = dfCyData[condition1 & condition2]['I'].values 
                
                #Averaged Icap
                I_cap1 = np.mean(abs(I_cap0))
                    
                #C [mF/cm2] = Icapacitive / ScanRate / Area * 1000 
            Capacitance.append(round(I_cap1/area/ScanRate*1e3,2))
        self.__setattr__('Capacitance', Capacitance)


#Charge Storage Capacitance (CSC), Injected charge 'independently' from time
#CSC = integral(cathodic or anodic current* time) 
#CSC = integral(I(<0 or >0)*U(range(I<0 or >0))/ScanRate)
    def getCSC(self):
        
        CSC_Cath = []
        CSC_An = []
        
        data = {'I': self.I, 'Ewe': self.Ewe, 'cyclenumber': self.cyclenumber}
        df = pd.DataFrame(data)  
        dfCycles = df.groupby('cyclenumber')  
        ScanRate = self.ScanRate
        area = 5e-6

        for cycle in dfCycles:
            dfCyData = cycle[1]
            
            #Changing the sign of ScanRate leads to exponential functions
            #These are very relevant at the edges of PotWin
            #Abrupt change of the sign of I 
            #That reduces SIGNIFICANTLY the integrated area
            #Including the firs point of I from the other sign compensates this
            
            condition1 = dfCyData['Ewe'] < 0 #Negative Limit of PotWin
            Irange1 = min(abs(dfCyData[condition1]['I'].values)) #Min I due to exp
            
            condition2 = dfCyData['Ewe'] > 0 #Positive Limit of PotWin
            Irange2 = min(abs(dfCyData[condition2]['I'].values)) #Max I due to exp
            
            condition3 = dfCyData['I'] <= Irange1 #Cathodic current
            condition4 = dfCyData['I'] >= Irange2 #Anodic current
            
            #Integration within the stablished ranges [mA*V]
            CSC_Cath0 = np.trapz(dfCyData[condition3]['I'].values, dfCyData[condition3]['Ewe'].values)
            CSC_An0 = np.trapz(dfCyData[condition4]['I'].values, dfCyData[condition4]['Ewe'].values)  
            
            #CSC [mC/cm2] = int(I*V)/scanRate/area*1000
            CSC_Cath.append(round(CSC_Cath0/area/ScanRate*1e3,2))
            CSC_An.append(round(CSC_An0/area/ScanRate*1e3,2))
        
        self.__setattr__('CSC_Cath', CSC_Cath)
        self.__setattr__('CSC_An', CSC_An)
        
        
if __name__ == "__main__":

#    FileName = './TestFiles/B5_Cor64_D1_Eup4_M12_01_CV.mpt'
    FileName = './TestFiles/B5_Cor64_D1_Eup4_M12_01_CV.mpt'
#    FileName = 'B12_MEA1_57_13_B2_M14_Pulses_1M_8mCcm2_02_CP Fast.mpt'
    
    MpytData = MpytDataBase(FileName=FileName)


    
    
    
