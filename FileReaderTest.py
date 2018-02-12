#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 22:00:36 2018

@author: aguimera
"""

import numpy as np
import matplotlib.pyplot as plt


class mptData(object):
    PropRemoveChars = ('-', '(', ')', '<', '>', ' ', '.')

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


FileName = 'B5_Cor64_D1_Eup4_M12_01_CV.mpt'

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

plt.plot(myDat.Ewe, myDat.I)
