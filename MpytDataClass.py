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


def CalcScanRate(time, V):
    SR = np.abs(np.diff(V)/np.diff(time))
    SR = SR[np.abs(SR - np.mean(SR)) < 0.25 * np.std(SR)]
    return np.mean(SR)


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

        self.GetCPcycles()
        self.GetPIEScycles()
        self.GetCVcycles()

        self.CalcCV()

    def CalcCV(self):
        if len(self.CVcycles) == 0:
            return

        Cap = []
        for cv in self.CVcycles:
            I = cv['I']
            V = cv['Ewe']
            time = cv['time']

            SR = CalcScanRate(time, V)       
            PotWin = (np.min(V), np.max(V))
            CenterPotWin = PotWin[1] + PotWin[0] #center of PW TODO !!!! Could crash if have same sign

            Ind1 = np.min(np.where(V < CenterPotWin)[0])            
            Ind2 = np.min(np.where(V[Ind1:] > CenterPotWin)[0])

#            print Ind1, Ind2
#            print CenterPotWin

            ICap = np.mean(np.abs(I[[Ind1, Ind2]]))            
            cv['Cap'] = ICap*SR
            Cap.append(cv['Cap'])
            
            cv['SR'] = SR
            cv['PotWin'] = PotWin
            cv['CenterPotWin'] = CenterPotWin             
        self.Cap = Cap
    
        
    def GetCVcycles(self):
        if 'ox' not in self.__dict__.keys():
            self.CVcycles = []
            return

        nCycles = set(self.cyclenumber)
        CVcycles = []
        for cy in nCycles:
            inds = np.where(self.cyclenumber == cy)
            Cycle = {'time': self.time[inds] - self.time[inds[0][0]],
                     'I': self.I[inds],
                     'Ewe': self.Ewe[inds],
                     'Cycle': cy}
            CVcycles.append(Cycle)

        self.CVcycles = CVcycles

    def GetCPcycles(self, DTimeSplitter=1):
        if self.mode[0] != 1:
            self.CPcycles = []
            return

        dt = np.diff(self.time)
        sepInds = np.where(dt > DTimeSplitter)[0]
        if len(sepInds) == 0:
            sepInds = (len(self.time), )
        CPcycles = []
        oldInd = -1
        for cy, sep in enumerate(sepInds):
            inds = range(oldInd+1, sep)
            time = self.time[inds]
            time = time - time[0]
            oldInd = sep
            Cycle = {'time': time,
                     'I': self.I[inds],
                     'Ewe': self.Ewe[inds],
                     'Cycle': cy}
            CPcycles.append(Cycle)

        self.CPcycles = CPcycles

    def GetPIEScycles(self, DTimeSplitter=100):
        if 'ReZ' not in self.__dict__.keys():
            self.PIEScycles = []
            return

        dt = np.diff(self.time)
        sepInds = np.where(dt > DTimeSplitter)[0]
        if len(sepInds) == 0:
            sepInds = (0, )
        PIEScycles = []
        oldInd = -1
        for cy, sep in enumerate(sepInds):
            inds = range(oldInd+1, sep)
            time = self.time[inds]
            time = time - time[0]
            oldInd = sep
            finds = np.where(self.freq[inds] > 0)[0]
            Cycle = {'time': time,
                     'Ze': (self.ReZ[inds][finds] - self.ImZ[inds][finds]*1j),
                     'freq': self.freq[inds][finds],
                     'Cycle': cy}
            PIEScycles.append(Cycle)

        self.PIEScycles = PIEScycles

if __name__ == "__main__":
    
    plt.close('all')

    FileName = './TestFiles/B5_Cor64_D1_Eup4_M12_01_CV.mpt'
#    FileName = './TestFiles/B12_MEA1_57_13_B2_M14_Pulses_1M_8mCcm2_04_PEIS.mpt'
#    FileName = './TestFiles/B12_MEA1_57_13_B2_M14_Pulses_1M_8mCcm2_02_CP Fast.mpt'
#    FileName = './TestFiles/B12_MEA1_57_13_B2_M2_Pulses_05_CP Fast.mpt'
       
    MpytData = MpytDataBase(FileName=FileName)
    
    print MpytData.__dict__.keys()
    
#    fig, (Axm, Axp) = plt.subplots(2, 1, sharex=True)
#    for IES in MpytData.PIEScycles:
#        Axm.loglog(IES['freq'], np.abs(IES['Ze']))
#        Axp.semilogx(IES['freq'], np.angle(IES['Ze'], deg=True))
#
    fig, Axcv = plt.subplots()    
    for CV in MpytData.CVcycles:
        Axcv.plot(CV['Ewe'], CV['I'])
    plt.figure()
    print MpytData.Cap
    

#    fig, AxcpE = plt.subplots()
#    AxcpI = plt.twinx(AxcpE)
#    for CP in MpytData.CPcycles:
#        AxcpE.plot(CP['time'], CP['Ewe'])
#        AxcpI.plot(CP['time'], CP['I'],'--', alpha=0.5)

###############################################################################
### SR call debug
###############################################################################    
    ## SR debugging
    ## direct option
#    FileName = './TestFiles/B5_Cor64_D1_Eup4_M12_01_CV.mpt'
#    MpytData = MpytDataBase(FileName=FileName)
#    fig, Ax1 = plt.subplots()
#    fig, Ax2 = plt.subplots()
#    for CV in MpytData.CVcycles:       
#        SR = np.abs(np.diff(CV['Ewe'])/np.diff(CV['time']))
#        Ax1.plot(CV['time'][1:],SR,'*')
#        Ax1.plot(CV['time'][1:],np.mean(SR)*np.ones(len(SR)))
#        
#        Ax2.boxplot(SR, positions=(CV['Cycle'],))
#    plt.xlim(0, CV['Cycle'])
#
#    ## SR debugging
#    ## Outlier removing
#    fig, Ax1 = plt.subplots()
#    fig, Ax2 = plt.subplots()
#    for CV in MpytData.CVcycles:       
#        SR = np.abs(np.diff(CV['Ewe'])/np.diff(CV['time']))
#        Ax1.plot(CV['time'][1:],SR,'*')
#        
#        SR = SR[np.abs(SR - np.mean(SR)) < 0.25 * np.std(SR)]
#        Ax1.plot(CV['time'],np.mean(SR)*np.ones(len(CV['time'])))
#        
#        Ax2.boxplot(SR, positions=(CV['Cycle'],))
#    plt.xlim(0, CV['Cycle'])




