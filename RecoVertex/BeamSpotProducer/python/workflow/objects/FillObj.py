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
        
        # remove html tags
        self.pattern = re.compile('\<[^>]+\>')
 
    def readLine(self, line):
        '''
        '''
        toRemove = self.pattern.findall(line)

        for r in toRemove:
            line = line.replace(r, '')
              
        elements = line.split('\t')
             
        self.Fill            = int  (elements[0])
        self.CreateTime      = elements[1]
        self.DurationStable  = elements[2]
        self.Bfield          = float(elements[3])
        self.PeakInstLumi    = float(elements[4])
        self.PeakPileup      = float(elements[5])
        self.PeakSpecLumi    = float(elements[6])
        self.DeliveredLumi   = float(elements[7])
        self.RecordedLumi    = float(elements[8])
        self.EffByLumi       = float(elements[9])
        self.EffByTime       = float(elements[10])
        self.BeginTime       = elements[11]
        try:
            self.toReady         = float(elements[12])
        except:
            self.toReady         = None
        self.EndTime         = elements[13]
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
        
        duration_hours   = int(re.findall(r'\d+', self.DurationStable)[0])
        duration_minutes = int(re.findall(r'\d+', self.DurationStable)[1])
        
        td = datetime.timedelta(hours = duration_hours, 
                                minutes = duration_minutes)
        
        self.DurationStable = td 
        
        for el in ['EndTime', 'BeginTime', 'CreateTime']:

            element = getattr(self, el)
            
            year  = int(element.split()[0].split('.')[0])
            month = int(element.split()[0].split('.')[1])
            day   = int(element.split()[0].split('.')[2])

            hour   = int(element.split()[1].split(':')[0])
            minute = int(element.split()[1].split(':')[1])
            second = int(element.split()[1].split(':')[2])
            
            dt = datetime.datetime(year, month, day, hour, minute, second)
            setattr(self, el, dt)

    def Print(self):
        '''
        Nicely formatting printing
        '''
        print ''
        for k, v in vars(self).items():
            print k, '=', v

if __name__ == '__main__':
    
    fname = 'fills.txt'
    myFills = {}

    with open(fname) as f:
        content = f.readlines()

    for c in content[1:]:
        myFill = Fill()
        myFill.readLine(c)
        myFills[myFill.Fill] = myFill

    
    Fills3p8T  = []
    Fills0T    = []
    Fills2p8T  = []
    FillsOther = []

    for k, v in myFills.items():
        if v.Bfield > 3.7:
            Fills3p8T.append(k)
        elif v.Bfield < 0.1:
            Fills0T.append(k)
        elif v.Bfield > 2.7 and v.Bfield < 2.9:
            Fills2p8T.append(k)
        else:
            FillsOther.append(k)

    Fills3p8T .sort()
    Fills0T   .sort()
    Fills2p8T .sort()
    FillsOther.sort()

    print '\n\nFills 3.8 T\n', Fills3p8T 
    print '\n\nFills   0 T\n', Fills0T   
    print '\n\nFills 2.8 T\n', Fills2p8T 
    print '\n\nOther Fills\n', FillsOther




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
