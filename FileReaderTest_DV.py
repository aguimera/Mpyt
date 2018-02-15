#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 22:00:36 2018

@author: aguimera
"""

import numpy as np
import matplotlib.pyplot as plt
import itertools as it
import pandas as pd


class mptData(object):
    PropRemoveChars = ('-', '(', ')', '<', '>', ' ', '.', '|')

    def __init__(self, DataDict):
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

#TODO check it properlly
    def calcPotentialWindow(self):
        Emin = np.round(np.max(self.Ewe), 1)
        Emax = np.round(np.max(self.Ewe), 1)
        self.PotWin = (Emin, Emax)

    def calcScanRate(self):    
#        data = {'Ewe': myDat.Ewe, 'time': myDat.time}
#        df = pd.DataFrame(data)
        dU = np.diff(self.Ewe)
        dt = np.diff(self.time)
        self.sr0 = round(np.mean(abs(dU/dt)*1000), 0)       

def getPotentialWindow(myDat):
    PotWin = [round(max(myDat.Ewe),1), round(min(myDat.Ewe),1)]
    
    return PotWin
    

def getCyclesData(myDat, analysis):
    X = []
    Y = []
    area = 5e-6*16
    
    fig, ax = plt.subplots()
  
    
    if analysis == 'I_U':
        
        data = {'I': myDat.I, 'Ewe': myDat.Ewe, 'cyclenumber': myDat.cyclenumber}
        df = pd.DataFrame(data)  
        dfCycles = df.groupby('cyclenumber') 
            
        for cycle in dfCycles:
            cyclenumber = cycle[0]
            dfCyData = cycle[1]
            I = dfCyData['I']
            U = dfCyData['Ewe']
                
            ax.plot(U, I*1e6, label = str(int(cyclenumber)))
            ax.legend()
            ax.set_xlabel('Uwe vs Uref [V]')
            ax.set_ylabel('Current [nA]')
                    
                                        
    if analysis == 'J_U':

        data = {'I': myDat.I, 'Ewe': myDat.Ewe, 'cyclenumber': myDat.cyclenumber}
        df = pd.DataFrame(data)  
        dfCycles = df.groupby('cyclenumber') 
        
        for cycle in dfCycles:
            cyclenumber = cycle[0]
            dfCyData = cycle[1]
            
            J = dfCyData['I']/area
            U = dfCyData['Ewe']
    
            ax.plot(U, J, label = str(int(cyclenumber)))
            ax.legend()
            ax.set_xlabel('Uwe vs Uref [V]')
            ax.set_ylabel('Current [mA/cm2]')
    
    if analysis == 'CSC':
        
        CSC_Cath = []
        CSC_An = []
        
        data = {'I': myDat.I, 'Ewe': myDat.Ewe, 'cyclenumber': myDat.cyclenumber}
        df = pd.DataFrame(data)  
        dfCycles = df.groupby('cyclenumber')  
        ScanRate = getScanRate(myDat)
        area = 5e-6

        for cycle in dfCycles:
            dfCyData = cycle[1]
            
            condition1 = dfCyData['Ewe'] < 0
            Irange1 = min(abs(dfCyData[condition1]['I'].values))
            
            condition2 = dfCyData['Ewe'] > 0
            Irange2 = min(abs(dfCyData[condition2]['I'].values))
            
            condition3 = dfCyData['I'] <= Irange1
            condition4 = dfCyData['I'] >= Irange2
            
            CSC_Cath0 = np.trapz(dfCyData[condition3]['I'].values, dfCyData[condition3]['Ewe'].values)
            CSC_An0 = np.trapz(dfCyData[condition4]['I'].values, dfCyData[condition4]['Ewe'].values)  
            
            CSC_Cath.append(round(CSC_Cath0/area/ScanRate*1e3,2))
            CSC_An.append(round(CSC_An0/area/ScanRate*1e3,2))
        
        ax.plot(CSC_Cath, label = 'Cathodic')
        ax.plot(CSC_An, label = 'Anodic')
        ax.set_xlabel('Cycle #')
        ax.set_ylabel('CSC [mC/cm2]')
        ax.legend()

    if analysis == 'Capacitance':
        
        Capacitance = []
        ScanRate = getScanRate(myDat)
        area = 5e-6
        
        data = {'I': myDat.I, 'Ewe': myDat.Ewe, 'cyclenumber': myDat.cyclenumber}
        df = pd.DataFrame(data)  
        EweStep = abs(df['Ewe'][1] - df['Ewe'][0])
        dfCycles = df.groupby('cyclenumber')   
        
        for cycle in dfCycles:
            dfCyData = cycle[1]
            PotWin = [max(dfCyData['Ewe']), min(dfCyData['Ewe'])]
            CenterPotWin = PotWin[0] + PotWin[1]
            
            I_cap0 = []
            n = 0
                
            while(len(I_cap0) < 2):
                n = n + 1
                condition1 = dfCyData['Ewe'] > CenterPotWin - EweStep * n
                condition2 = dfCyData['Ewe'] < CenterPotWin + EweStep * n
                I_cap0 = dfCyData[condition1 & condition2]['I'].values
                I_cap1 = np.mean(abs(I_cap0))
                    
            Capacitance.append(round(I_cap1/area/ScanRate*1e3,2))
        
        ax.plot(Capacitance)
        ax.set_xlabel('Cycle #')
        ax.set_ylabel('Capacitance [mF/cm2]')
                
    if analysis == 'EIS_Z':
        
        data = {'|Z|': myDat.Z, 'freq': myDat.freq, 'cyclenumber': myDat.cyclenumber}
        df = pd.DataFrame(data)  
        dfCycles = df.groupby('cyclenumber')   

        for cycle in dfCycles:
            dfCyData = cycle[1]
            Z = dfCyData['|Z|']
            freq = dfCyData['freq']       
            
            ax.set_title('EIS')
            ax.loglog(freq, Z)
            ax.set_ylabel('|Z| [Ohm]')
            ax.set_xlabel('Frequency [Hz]')

    if analysis == 'EIS_Phase':
        
        data = {'freq': myDat.freq,  'PhaseZ': myDat.PhaseZ, 'cyclenumber': myDat.cyclenumber}
        df = pd.DataFrame(data)  
        dfCycles = df.groupby('cyclenumber') 
        
        for cycle in dfCycles:
            dfCyData = cycle[1]
            freq = dfCyData['freq']       
            PhaseZ = dfCyData['PhaseZ']

            ax.set_ylim([-90, 0])
            ax.semilogx(freq, PhaseZ, '--')
            ax.set_ylabel('Phase [Degrees]')

    
        
    return 0
      
if __name__ == "__main__":

#    FileName = 'B5_Cor64_D1_Eup4_M12_01_CV.mpt'
    FileName = './TestFiles/B5_Cor64_D1_Eup4_M12_01_CV.mpt'
    
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
    
    
        
    myDat = mptData(Data)
    myDat.calcScanRate()
    
    plt.close('all')
    plt.plot(np.diff(myDat.time))
    print np.mean(np.diff(myDat.time))
    plt.figure()
    plt.plot(np.diff(myDat.Ewe))
    plt.figure()
    plt.plot(myDat.Ewe)
    plt.figure()
    plt.plot(np.abs(np.diff(myDat.Ewe)/np.diff(myDat.time)))
    
    
    print myDat.sr0

mptData.calcPotentialWindow    
    #getCyclesData(myDat, 'CSC')
    #
    #
    #data = {'I': myDat.I, 'Ewe': myDat.Ewe, 'cyclenumber': myDat.cyclenumber}
    #df = pd.DataFrame(data)  
    #dfCycles = df.groupby('cyclenumber')  
    #ScanRate = getScanRate(myDat)
    #    
        
