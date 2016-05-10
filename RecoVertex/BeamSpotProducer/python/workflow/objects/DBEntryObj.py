#!/usr/bin/python

from datetime import datetime

class DBEntry(object):
    '''
    condDB entry object
    '''
    def __init__(self, *args, **kwargs):
        self.Reset()
        if args:
            self.Read(args[0])
        if 'line' in kwargs.keys():
            self.Read(kwargs['line'])
                
    def Read(self, line):

        elements = line.split()
        
        try:
            # RM obviously it changed
            # this works with CMSSW_7_5_DEVEL_X_2015-06-10-1100
        
            mydt = datetime(
                int(elements[4].split('-')[0]),
                int(elements[4].split('-')[1]),
                int(elements[4].split('-')[2]),
                int(elements[5].split(':')[0]),
                int(elements[5].split(':')[1]),
                int(elements[5].split(':')[2])
            )

            self.run        = int(elements[0])
            self.firstLumi  = int(elements[2])
            self.rawSince   = int(elements[3].replace('(','').replace(')',''))
            self.insertTime = mydt
            self.hash       = elements[6]
            self.type       = elements[7]

        except:
        
            mydt = datetime(
                int(elements[1].split('-')[0]),
                int(elements[1].split('-')[1]),
                int(elements[1].split('-')[2]),
                int(elements[2].split(':')[0]),
                int(elements[2].split(':')[1]),
                int(elements[2].split(':')[2])
            )

            self.run        = int(elements[0])
            self.insertTime = mydt
            self.hash       = elements[3]
            self.type       = elements[4]

    def Reset(self):
        self.run        = -1
        self.firstLumi  = -1
        self.rawSince   = -1
        self.insertTime = -1
        self.hash       = None
        self.type       = None
                

if __name__ == '__main__':
    # byLumi
    #line = '246908 Lumi    96  2015-06-04 14:34:12  c2bf9bdfefd920f5c31ae77e4299df5f6e042b5e  BeamSpotObjects'
    line = '248038 :    73 (1065315098165321)  2015-06-15 04:04:20  904be868beff578ebf7372f343f62431c7e5184f  BeamSpotObjects'
    # byRun
    line = '247914  2015-06-13  10:46:38  3f5387a9753863bbceef933372581332413b18d1  BeamSpotObjects'
    #line = 'paisjdouhas doiha woh 3f5387a9753863bbceef933372581332413b18d1  BeamSpotObjects'
    myDBEntry = DBEntry(line)
    myDBEntry = DBEntry(line = line)
    print vars(myDBEntry)

