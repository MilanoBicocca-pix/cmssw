#!/usr/bin/python

import os
import re
import datetime

class Fill():
    '''
    '''
    def __init__(self):
        '''
        '''
        
        beginOfTime = datetime.datetime.fromtimestamp(0)
        
        self.Fill            = -1               #
        self.CreateTime      = beginOfTime      #
        self.DurationStable  = 0                #
        self.Bfield          = -1.              #
        self.PeakInstLumi    = -1.              #
        self.PeakPileup      = -1.              #
        self.PeakSpecLumi    = -1.              #
        self.DeliveredLumi   = -1.              #
        self.RecordedLumi    = -1.              #
        self.EffByLumi       = -1.              #
        self.EffByTime       = -1.              #
        self.BeginTime       = beginOfTime      #
        self.toReady         = -1.              #
        self.EndTime         = beginOfTime      #
        self.Type            = ''               #
        self.Energy          = -1.              #
        self.IBeam1          = -1.              #
        self.IBeam2          = -1.              #
        self.nB1             = -1               #
        self.nB2             = -1               #
        self.nCol            = -1               #
        self.nTar            = -1.              #
        self.xIng            = -1.              #
        self.InjectionScheme = ''               #
        self.Runs            = []               #
        self.Comments        = ''               #
        
        # remove weird xls instructions
        self.pattern = re.compile('\<[^>]+\>')
 
    def readLine(self, line):
        '''
        '''
        toRemove = self.pattern.findall(line)

        for r in toRemove:
            line = line.replace(r, '')
              
        elements = line.split('\t')
             
        self.Fill            = int  (elements[0])
        self.CreateTime      = elements[1]          # to be implemented
        self.DurationStable  = elements[2]          # to be implemented
        self.Bfield          = float(elements[3])
        self.PeakInstLumi    = float(elements[4])
        self.PeakPileup      = float(elements[5])
        self.PeakSpecLumi    = float(elements[6])
        self.DeliveredLumi   = float(elements[7])
        self.RecordedLumi    = float(elements[8])
        self.EffByLumi       = float(elements[9])
        self.EffByTime       = float(elements[10])
        self.BeginTime       = elements[11]         # to be implemented
        try:
            self.toReady         = float(elements[12])
        except:
            self.toReady         = None
        self.EndTime         = elements[13]         # to be implemented
        self.Type            = str  (elements[14])
        self.Energy          = float(elements[15])
        self.IBeam1          = float(elements[16])
        self.IBeam2          = float(elements[17])
        self.nB1             = int  (elements[18])
        self.nB2             = int  (elements[19])
        self.nCol            = int  (elements[20])
        self.nTar            = float(elements[21])
        self.xIng            = float(elements[22])
        self.InjectionScheme = str  (elements[23])
        self.Runs            = [int(i) for i in elements[24].split()]
        self.Comments        = str  (elements[25])

    def Print(self):
        '''
        '''
        for k, v in vars(self):
            print k, '\t=\t', v

if __name__ == '__main__':
    
    fname = 'fills.txt'
    myFill = Fill()
    
    with open(fname) as f:
        content = f.readlines()
    
    for c in content[1:]:
        myFill.readLine(c)
        print myFill.Fill, ' : ', myFill.Runs






















  
 

# Fill            = 4681 
# CreateTime      = 2015.12.01 02:39:55 
# DurationStable  = 6 hr 11 min 
# Bfield          = 3.79998818359375
# PeakInstLumi    = 1856.113900 
# PeakPileup      = 0.003219 
# PeakSpecLumi    = 2.110736 
# DeliveredLumi   = 21.249954 
# RecordedLumi    = 18.627398 
# EffByLumi       = 87.659 
# EffByTime       = 98.021 
# BeginTime       = 2015.12.01 07:40:26 
# toReady         = 0.955 
# EndTime         = 2015.12.01 13:50:59 
# Type            = Ion - PB82 vs PB82
# Energy          = 6369 
# IBeam1          = 60.304612 
# IBeam2          = 59.525416 
# nB1             = 426 
# nB2             = 424 
# nCol            = 400 
# nTar            = 400.0 
# xIng(microrad)  = 145.0 
# InjectionScheme = 100_225ns_426Pb_424Pb_400_362_24_19inj 
# Runs            = 263005 263007 263022  
# Comments        =
#               #
