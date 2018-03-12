#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 12:32:14 2018

@author: aguimera
"""

from Mpyt.MpytDataClass import MpytDataBase
import os, glob
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
import sys

FileFind = 'TestFiles/*2-60*CV*.mpt'
    
Meas = {}
for f in glob.glob(FileFind):
    filein = f.split('/')[-1]
    fparts = filein.split('.')[0].split('-')
    
    ElectName = fparts[0] + '-' + fparts[1] + '-' + fparts[2].split('_')[0]
    print filein, ElectName
    Mdat = MpytDataBase(FileName=f)
    Mdat.Name = ElectName
    if ElectName in Meas:
        Meas[ElectName].append(Mdat)
    else:
        Meas[ElectName] = [Mdat, ]
    
#%%
plt.close('all')

fig, Axcv = plt.subplots()    
for Ename, data in Meas.iteritems():
    for dat in data:
        if dat.GetCap() is None:
            continue
        print dat.GetCap(), dat.GetSR()        
        Ve, Ie = dat.GetCV()
        Lab = dat.Name
        Axcv.plot(Ve, Ie)
plt.legend()
    

       
#fig, Axcv = plt.subplots()    
#for Ename, data in Meas.iteritems():
#    for dat in data:
#        if dat.GetCap() is None:
#            continue
#        print dat.GetCap(), dat.GetSR()
#        VE = np.array([])
#        IE = np.array([])
#        if len(dat.CVcycles)>1:
#            Ssize = np.min([CV['Ewe'].shape[0] for CV in dat.CVcycles[1:]])
#            for CV in dat.CVcycles[1:]:            
#                Ve = CV['Ewe']
#                Ie = CV['I']
#                Axcv.plot(Ve, Ie, 'k--', alpha=0.1)
#                VE = np.vstack((VE, Ve[:Ssize])) if VE.size else Ve[:Ssize]
#                IE = np.vstack((IE, Ie[:Ssize])) if IE.size else Ie[:Ssize]
#
#            sr = dat.GetSR(units='V/s')
#            Lab = '{}-{}{}'.format(Ename, np.round(sr,2), str(sr.units).split(' ')[-1])            
#            Axcv.plot(VE.mean(axis=0), IE.mean(axis=0), label=Lab)            
#        else:
#            sr = dat.GetSR(units='V/s')
#            Lab = '{} {} {}'.format(Ename, np.round(sr,2), str(sr.units).split(' ')[-1])
#            Axcv.plot(CV['Ewe'], CV['I'], label=Lab)
#plt.legend()
#    


##%%
#plt.close('all')
#       
#fig, Axcv = plt.subplots()    
#for Ename, data in Meas.iteritems():
#    for dat in data:
#        for CV in dat.CVcycles:
#            Lab = '{}-SR{}'.format(dat.Name, np.round(CV['SR'],1))
#            Axcv.plot(CV['Ewe'], CV['I'], label=Lab)
#
#plt.legend()
#
##%%
#
#fig, AxcpE = plt.subplots()
#AxcpI = plt.twinx(AxcpE)
#for Ename, data in Meas.iteritems():
#    for dat in data:
#        for CP in dat.CPcycles:
#            AxcpE.plot(CP['time'], CP['Ewe'])
#            AxcpI.plot(CP['time'], CP['I'],'k--', alpha=0.5)
#
#Fig, (Axm, Axp) = plt.subplots(2, 1, sharex=True)
#for Ename, data in Meas.iteritems():
#    for dat in data:
#        for IES in dat.PIEScycles:
#            Axm.loglog(IES['freq'], np.abs(IES['Ze']))
#            Axp.semilogx(IES['freq'], np.angle(IES['Ze'], deg=True))
