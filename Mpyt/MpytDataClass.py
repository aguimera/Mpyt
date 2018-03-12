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
import quantities as pq
from datetime import datetime


def TextFileReader(FileName):
    FileIn = open(FileName, 'r')

    State = 'Header'
    HeaderInfo = ''
    HeadL = None
    Date = None
    for nl, line in enumerate(FileIn):
        if State == 'Header':
            HeaderInfo = HeaderInfo + line
            if line.startswith('Acquisition started on'):
                line = line.replace('\r', '')
                line = line.replace('\n', '')
                Date = datetime.strptime(line.split(' : ')[-1],
                                         '%m/%d/%Y %H:%M:%S')
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
    Data['DateTime'] = Date
    Data['FileName'] = FileName
    return Data


def CalcScanRate(time, V, DevRem=0.25):
    SR = np.abs(np.diff(V)/np.diff(time))
    SR = SR[np.abs(SR - np.mean(SR)) < DevRem * np.std(SR)]
    return np.mean(SR)


class MpytDataBase(object):
    PropRemoveChars = ('-', '(', ')', '<', '>', ' ', '.', '|')
    UnitsReplace = (('-1', '**-1'), ('-2', '**-2'), ('\xb5', 'u'))
    SRDevRemoval = 0.25
    Area = 5e-6*pq.cm**2
    Name = None
    CVcycles = []
    PIEScycles = []
    CPcycles = []
    Cap = None
    SR = None

    def __init__(self, FileName, DataDict=None):
        if DataDict is None:
            DataDict = TextFileReader(FileName)

        Units = {}
        for k, v in DataDict.iteritems():
            k = k.split('/')
            prop = k[0]
            for char in self.PropRemoveChars:
                prop = prop.replace(char, '')
            if (len(k) > 1) and (prop != 'ox'):
                unit = k[1]
                for uor, urep in self.UnitsReplace:
                    unit = unit.replace(uor, urep)
                Units.update({prop: unit})
                vq = pq.Quantity(v, units=unit)
                self.__setattr__(prop, vq)
            else:
                self.__setattr__(prop, v)
        self.__setattr__('Units', Units)

        if len(self.time) == 0:
            print FileName, 'Warning empty file'
            return

        self.CalcCPcycles()
        self.CalcPIEScycles()
        self.CalcCVcycles()

#        try:
        self.CalcCV()
#        except:
#            print 'Error calclutating CV'

    def CalcCV(self):
        if len(self.CVcycles) == 0:
            return

        Cap = []
        SR = []
        for cv in self.CVcycles:
            Ie = cv['I']
            Ve = cv['Ewe']
            time = cv['time']

            # calc SR, PotWin, and CenterPotWin
            sr = CalcScanRate(time, Ve, DevRem=self.SRDevRemoval)
            PotWin = (np.min(Ve), np.max(Ve))
            CenterPotWin = PotWin[1] + PotWin[0]  # center of PW
            # TODO !!!! Could crash if have same sign
            cv['SR'] = sr
            cv['PotWin'] = PotWin
            cv['CenterPotWin'] = CenterPotWin

            # Calc Capacitance
            Ind1 = np.min(np.where(Ve < CenterPotWin)[0])
            inds = np.where(Ve[Ind1:] > CenterPotWin)[0]
            if len(inds) == 0:
                print 'Removed incompleted CV', cv['Cycle']
                self.CVcycles.remove(cv)
                continue
            Ind2 = np.min(inds)

            ICap = np.mean(np.abs(Ie[[Ind1, Ind2]]))
            cv['Cap'] = ICap/sr
            Cap.append(cv['Cap'])
            SR.append(sr)

            # Calc CSC
            Irange1 = np.min(np.abs(Ie[np.where(Ve < 0)[0]]))
            Irange2 = np.min(np.abs(Ie[np.where(Ve > 0)[0]]))
            Indcat = np.where(Ie <= Irange1)[0]
            Indan = np.where(Ie >= Irange2)[0]
            cv['Indcat'] = Indcat
            cv['Indan'] = Indan
            CSCcat0 = np.trapz(Ie[Indcat], Ve[Indcat])
            CSCan0 = np.trapz(Ie[Indan], Ve[Indan])
            cv['CSCcat0'] = CSCcat0
            cv['CSCan0'] = CSCan0
            cv['CSCcat'] = (CSCcat0 / sr).rescale('C')
            cv['CSCan'] = (CSCan0 / sr).rescale('C')

        if len(Cap) > 1:
            self.Cap = (np.mean(Cap[1:])*Cap[-1].units).rescale('mF')
            self.CapErr = self.Cap/np.std(Cap[1:])
            self.SR = np.mean(SR[1:])*SR[-1].units
        else:
            self.Cap = (np.mean(Cap)*Cap[-1].units).rescale('mF')
            self.SR = np.mean(SR)*SR[-1].units
            self.CapErr = None

    def CalcCVcycles(self):
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

    def CalcCPcycles(self, DTimeSplitter=1):
        if 'mode' not in self.__dict__.keys():
            self.CPcycles = []
            return
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

    def CalcPIEScycles(self, DTimeSplitter=100):
        if 'ReZ' not in self.__dict__.keys():
            self.PIEScycles = []
            return

        dt = np.diff(self.time)
        sepInds = np.where(dt > DTimeSplitter)[0]
        if len(sepInds) == 0:
            sepInds = (len(self.time), )
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

    def GetCap(self, units='mF/cm**2'):
        if self.Cap is None:
            return None
        return np.round((self.Cap/self.Area).rescale(units),2)
    
    def GetSR(self, units='V/s'):
        if self.SR is None:
            return None
        return np.round(self.SR.rescale(units),2)

    def GetCV(self, Mean=True, Vunits='V', Iunits='uA'):
        if len(self.CVcycles) == 0:
            return None
        
        VE = np.array([])
        IE = np.array([])
        if len(self.CVcycles) > 1:
            Ssize = np.min([CV['Ewe'].shape[0] for CV in self.CVcycles[1:]])
            for CV in self.CVcycles[1:]:            
                Ve = CV['Ewe']
                Ie = CV['I']
                VE = np.vstack((VE, Ve[:Ssize])) if VE.size else Ve[:Ssize]
                IE = np.vstack((IE, Ie[:Ssize])) if IE.size else Ie[:Ssize]
            Ver = VE.mean(axis=0) * Ve.units
            Ier = IE.mean(axis=0) * Ie.units
        else:
            Ver = CV['Ewe']
            Ier = CV['I']      
        return Ver.rescale(Vunits), Ier.rescale(Iunits)


if __name__ == "__main__":
    
    plt.close('all')

#    FileName = './TestFiles/B5_Cor64_D1_Eup4_M12_01_CV.mpt'
##    FileName = './TestFiles/B12_MEA1_57_13_B2_M14_Pulses_1M_8mCcm2_04_PEIS.mpt'
##    FileName = './TestFiles/B12_MEA1_57_13_B2_M14_Pulses_1M_8mCcm2_02_CP Fast.mpt'
##    FileName = './TestFiles/B12_MEA1_57_13_B2_M2_Pulses_05_CP Fast.mpt'
#       
#    MpytData = MpytDataBase(FileName=FileName)
#    
#    print MpytData.__dict__.keys()
    
#    fig, (Axm, Axp) = plt.subplots(2, 1, sharex=True)
#    for IES in MpytData.PIEScycles:
#        Axm.loglog(IES['freq'], np.abs(IES['Ze']))
#        Axp.semilogx(IES['freq'], np.angle(IES['Ze'], deg=True))
#
    
###############################################################################
### CSC debug plots
###############################################################################  
    FileName = './TestFiles/B5_Cor64_D1_Eup4_M12_01_CV.mpt'
    MpytData = MpytDataBase(FileName=FileName)

    fig, Axcv = plt.subplots()    
    for CV in MpytData.CVcycles:
        Axcv.plot(CV['Ewe'], CV['I'])
        inds = CV['Indcat']
        Axcv.plot(CV['Ewe'][inds], CV['I'][inds],'*')
        inds = CV['Indan']
        Axcv.plot(CV['Ewe'][inds], CV['I'][inds],'+k')
        
    print MpytData.Cap
    fig, AxV = plt.subplots()
    AxI = plt.twinx(AxV)
    plt.figure()
    AxV.plot(CV['Ewe'])
    AxI.plot(CV['I'])

    fig, AxcpE = plt.subplots()
    AxcpI = plt.twinx(AxcpE)
    for CP in MpytData.CPcycles:
        AxcpE.plot(CP['time'], CP['Ewe'])
        AxcpI.plot(CP['time'], CP['I'],'--', alpha=0.5)

###############################################################################
### SR call debug
###############################################################################    
    # SR debugging
    # direct option
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




