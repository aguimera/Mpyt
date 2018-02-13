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


if __name__ == "__main__":

#    FileName = './TestFiles/B5_Cor64_D1_Eup4_M12_01_CV.mpt'
    FileName = './TestFiles/B12_MEA1_57_13_B2_M14_Pulses_1M_8mCcm2_04_PEIS.mpt'
#    FileName = 'B12_MEA1_57_13_B2_M14_Pulses_1M_8mCcm2_02_CP Fast.mpt'
    
    MpytData = MpytDataBase(FileName=FileName)
    
    
    
    
