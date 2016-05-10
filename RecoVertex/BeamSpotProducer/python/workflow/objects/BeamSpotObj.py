#!/usr/bin/python

import os
import datetime
from math import pow, sqrt
import xml.etree.ElementTree as et
from RecoVertex.BeamSpotProducer.workflow.objects.IOVObj import IOV

class BeamSpot(object):
    '''
    BeamSpot object
    '''
    def __init__(self):
        self.Reset()
        
    def Reset(self):
        self.Type          = -1
        self.X             =  0.
        self.Xerr          =  0.
        self.Y             =  0.
        self.Yerr          =  0.
        self.Z             =  0.
        self.Zerr          =  0.
        self.sigmaZ        =  0.
        self.sigmaZerr     =  0.
        self.dxdz          =  0.
        self.dxdzerr       =  0.
        self.dydz          =  0.
        self.dydzerr       =  0.
        self.beamWidthX    =  0.
        self.beamWidthXerr =  0.
        self.beamWidthY    =  0.
        self.beamWidthYerr =  0.
        self.EmittanceX    =  0.
        self.EmittanceY    =  0.
        self.betastar      =  0.
        self.IOVfirst      =  0
        self.IOVlast       =  0
        self.IOVBeginTime  =  0
        self.IOVEndTime    =  0
        self.Run           =  0
        self.XYerr         =  0. 
        self.YXerr         =  0.
        self.dxdzdydzerr   =  0.
        self.dydzdxdzerr   =  0.
    
    def SetIOV(self, iov):
        '''
        Set BeamSpot interval of validity
        from an IOV object.
        Works only if the IOV spans over just *one* run.
        This descends from the way the BeamSpot thing is conceived.
        '''
        if iov.RunFirst != iov.RunLast:
            raise ValueError('First Run must be equal to last Run.\nNow first:'\
                             '%d\t last:%d' %(iov.RunFirst, iov.RunLast))
            exit()
            
        self.IOVBeginTime = iov.since
        self.IOVEndTime   = iov.till
        self.Run          = iov.RunFirst
        self.IOVfirst     = iov.LumiFirst
        self.IOVlast      = iov.LumiLast
        
    def GetIOV(self):
        '''
        Returns the interval of validity of the BeamSpot object.
        '''
        bsIOV = IOV()
        bsIOV.since     = self.IOVBeginTime
        bsIOV.till      = self.IOVEndTime
        bsIOV.RunFirst  = self.Run
        bsIOV.RunLast   = self.Run
        bsIOV.LumiFirst = self.IOVfirst
        bsIOV.LumiLast  = self.IOVlast
        
        return bsIOV
        
    def ReadXML(self, xml):
        '''
        Set the BeamSpot attributes from reading a xml file  or string 
        as returned by the condDB command:
        conddb dump 6601ff1538198fad046c18af4fb48ce3053e4c7c --format xml
        
        NotaBene: IOV boundaries are not saved in the xml from the DB
                  therefore they remain set to dummy values
        '''
        # check whether xml is a file or a xml-like string
        if os.path.isfile(xml):
            filein = open(xml) 
            lines = [line for line in filein.readlines() if 'DOCTYPE' 
                     not in line and 'boost_serialization' not in line]
        else:
            lines = [line for line in xml.split('\n') if 'DOCTYPE' 
                     not in line and 'boost_serialization' not in line]

        xmlstring = ''.join(lines)
                
        # get ahold of the xml object        
        dbentry = et.fromstring(xmlstring)
        
        # connect index to human readable names
        d = { k.tag.replace('-','') : i for i, k in enumerate(dbentry)}

        self.Xerr          = sqrt( float( dbentry[ d['covariance'] ].findall('item')[0].findall('item')[0].text ) )
        self.Yerr          = sqrt( float( dbentry[ d['covariance'] ].findall('item')[1].findall('item')[1].text ) )
        self.Zerr          = sqrt( float( dbentry[ d['covariance'] ].findall('item')[2].findall('item')[2].text ) )
        self.sigmaZerr     = sqrt( float( dbentry[ d['covariance'] ].findall('item')[3].findall('item')[3].text ) )
        self.dxdzerr       = sqrt( float( dbentry[ d['covariance'] ].findall('item')[4].findall('item')[4].text ) )
        self.dydzerr       = sqrt( float( dbentry[ d['covariance'] ].findall('item')[5].findall('item')[5].text ) )
        self.beamWidthXerr = sqrt( float( dbentry[ d['covariance'] ].findall('item')[6].findall('item')[6].text ) )
        self.beamWidthYerr = self.beamWidthXerr 

        self.Type          = int  ( dbentry[ d['type'      ] ].text                    )
        self.X             = float( dbentry[ d['position'  ] ].findall('item')[0].text )
        self.Y             = float( dbentry[ d['position'  ] ].findall('item')[1].text )
        self.Z             = float( dbentry[ d['position'  ] ].findall('item')[2].text )
        self.sigmaZ        = float( dbentry[ d['sigmaZ'    ] ].text                    )
        self.dxdz          = float( dbentry[ d['dxdz'      ] ].text                    )
        self.dydz          = float( dbentry[ d['dydz'      ] ].text                    )
        self.beamWidthX    = float( dbentry[ d['beamwidthX'] ].text                    )
        self.beamWidthY    = float( dbentry[ d['beamwidthY'] ].text                    )
        self.EmittanceX    = float( dbentry[ d['emittanceX'] ].text                    )
        self.EmittanceY    = float( dbentry[ d['emittanceY'] ].text                    )
        self.betastar      = float( dbentry[ d['betaStar'  ] ].text                    )

    def Read(self, payload):
        '''
        Reads the Payload-like fragment (portion of text file, from Run 
        to BetaStar) and sets its attributes accordingly.
        
        E.g.:
        
        Runnumber 195660
        BeginTimeOfFit 2012.06.07 07:22:30 GMT 1339053750
        EndTimeOfFit 2012.06.07 07:22:52 GMT 1339053772
        LumiRange 60 - 60
        Type 2
        X0 0.0720989
        Y0 0.0627524
        Z0 -1.19547
        sigmaZ0 4.76234
        dxdz 3.7475e-05
        dydz -2.86578e-05
        BeamWidthX 0.0020988
        BeamWidthY 0.00201228
        Cov(0,j) 4.35559e-08 3.11886e-10 0 0 0 0 0
        Cov(1,j) 3.11886e-10 4.63974e-08 0 0 0 0 0
        Cov(2,j) 0 0 0.0948918 0 0 0 0
        Cov(3,j) 0 0 0 0.0474358 0 0 0
        Cov(4,j) 0 0 0 0 1.76222e-09 2.11043e-11 0
        Cov(5,j) 0 0 0 0 2.11043e-11 1.773e-09 0
        Cov(6,j) 0 0 0 0 0 0 7.89321e-08
        EmittanceX 0.0
        EmittanceY 0.0
        BetaStar 0.0
        '''
        self.Run           = int  ( payload[ 0].split()[1] )
        self.IOVBeginTime  = int  ( payload[ 1].split('GMT')[1] )
        self.IOVEndTime    = int  ( payload[ 2].split('GMT')[1] )
        self.IOVfirst      = int  ( payload[ 3].split()[1] )
        self.IOVlast       = int  ( payload[ 3].split()[3] )
        self.Type          = int  ( payload[ 4].split()[1] )

        self.X             = float( payload[ 5].split()[1] )
        self.Y             = float( payload[ 6].split()[1] )
        self.Z             = float( payload[ 7].split()[1] )

        self.sigmaZ        = float( payload[ 8].split()[1] )
        self.dxdz          = float( payload[ 9].split()[1] )
        self.dydz          = float( payload[10].split()[1] )

        self.beamWidthX    = float( payload[11].split()[1] )
        self.beamWidthY    = float( payload[12].split()[1] )
        
        # covariance matrix defined here
        # https://github.com/MilanoBicocca-pix/cmssw/blob/CMSSW_7_5_X_beamspot_workflow_riccardo/RecoVertex/BeamSpotProducer/src/PVFitter.cc#L306
        # diagonal terms 
        self.Xerr          = sqrt( float(payload[13].split()[1]) )
        self.Yerr          = sqrt( float(payload[14].split()[2]) )
        self.Zerr          = sqrt( float(payload[15].split()[3]) )
        self.sigmaZerr     = sqrt( float(payload[16].split()[4]) )
        self.dxdzerr       = sqrt( float(payload[17].split()[5]) )
        self.dydzerr       = sqrt( float(payload[18].split()[6]) )
        self.beamWidthXerr = sqrt( float(payload[19].split()[7]) )
        # self.beamWidthYerr = float( payload[16].split()[1] ) # not in cov matrix!
        # RIC: we should save it in the covariance matrix!
        #      workaround, for now
        self.beamWidthYerr = self.beamWidthXerr
        
        # off diagonal terms
        self.XYerr         = float( payload[13].split()[2] )
        self.YXerr         = float( payload[14].split()[1] )
        self.dxdzdydzerr   = float( payload[17].split()[6] )
        self.dydzdxdzerr   = float( payload[18].split()[5] )

        self.EmittanceX    = float( payload[20].split()[1] )
        self.EmittanceY    = float( payload[21].split()[1] )

        self.betastar      = float( payload[22].split()[1] )    

    def Dump(self, file, mode = 'a'):
        '''
        Dumps a Beam Spot objects into a Payload-like file.
        Default file open mode is append 'a', so that it can be serialised.
        '''
        
        f = open(file, mode)
        
        date_start = datetime.datetime.utcfromtimestamp(self.IOVBeginTime)
        date_end   = datetime.datetime.utcfromtimestamp(self.IOVEndTime  )
                
        str_date_start = '%d.%02d.%02d %02d:%02d:%02d' %( date_start.year   ,
                                                          date_start.month  ,
                                                          date_start.day    ,
                                                          date_start.hour   ,
                                                          date_start.minute ,
                                                          date_start.second )
        
        str_date_end   = '%d.%02d.%02d %02d:%02d:%02d' %( date_end.year   ,
                                                          date_end.month  ,
                                                          date_end.day    ,
                                                          date_end.hour   ,
                                                          date_end.minute ,
                                                          date_end.second )
        
        towrite = 'Runnumber {RUN}\n'                           \
                  'BeginTimeOfFit {DATESTART} GMT {TIMESTART}\n'\
                  'EndTimeOfFit {DATEEND} GMT {TIMEEND}\n'      \
                  'LumiRange {LUMISTART} - {LUMIEND}\n'         \
                  'Type {TYPE}\n'                               \
                  'X0 {X0}\n'                                   \
                  'Y0 {Y0}\n'                                   \
                  'Z0 {Z0}\n'                                   \
                  'sigmaZ0 {SZ0}\n'                             \
                  'dxdz {DXDZ}\n'                               \
                  'dydz {DYDZ}\n'                               \
                  'BeamWidthX {BWX}\n'                          \
                  'BeamWidthY {BWY}\n'                          \
                  'Cov(0,j) {M00} {M01} 0 0 0 0 0\n'            \
                  'Cov(1,j) {M10} {M11} 0 0 0 0 0\n'            \
                  'Cov(2,j) 0 0 {M22} 0 0 0 0\n'                \
                  'Cov(3,j) 0 0 0 {M33} 0 0 0\n'                \
                  'Cov(4,j) 0 0 0 0 {M44} {M45} 0\n'            \
                  'Cov(5,j) 0 0 0 0 {M54} {M55} 0\n'            \
                  'Cov(6,j) 0 0 0 0 0 0 {M66}\n'                \
                  'EmittanceX {EMX}\n'                          \
                  'EmittanceY {EMY}\n'                          \
                  'BetaStar {BSTAR}\n'                          \
                  ''.format(RUN       = str(self.Run          ),
                            DATESTART = str(str_date_start    ),
                            TIMESTART = str(self.IOVBeginTime ),
                            DATEEND   = str(str_date_end      ),
                            TIMEEND   = str(self.IOVEndTime   ),
                            LUMISTART = str(self.IOVfirst     ),
                            LUMIEND   = str(self.IOVlast      ),
                            TYPE      = str(self.Type         ),
                            X0        = str(self.X            ),
                            Y0        = str(self.Y            ),
                            Z0        = str(self.Z            ),
                            SZ0       = str(self.sigmaZ       ),
                            DXDZ      = str(self.dxdz         ),
                            DYDZ      = str(self.dydz         ),
                            BWX       = str(self.beamWidthX   ),
                            BWY       = str(self.beamWidthY   ),
                            # diagonal
                            M00       = str(pow(self.Xerr         , 2)),
                            M11       = str(pow(self.Yerr         , 2)),
                            M22       = str(pow(self.Zerr         , 2)),
                            M33       = str(pow(self.sigmaZerr    , 2)),
                            M44       = str(pow(self.dxdzerr      , 2)),
                            M55       = str(pow(self.dydzerr      , 2)),
                            M66       = str(pow(self.beamWidthXerr, 2)),
                            # off diagonal
                            M01       = str(self.XYerr        ),
                            M10       = str(self.YXerr        ),
                            M45       = str(self.dxdzdydzerr  ),
                            M54       = str(self.dydzdxdzerr  ),
                            EMX       = str(self.EmittanceX   ),
                            EMY       = str(self.EmittanceY   ),
                            BSTAR     = str(self.betastar     ),
                            )
        
        f.write(towrite)

    def Print(self):
        '''
        Nice printer.
        '''
        toWrite = 'X0         = {:3.6f} +/- {:3.4E} [cm]\n' \
                  'Y0         = {:3.6f} +/- {:3.4E} [cm]\n' \
                  'Z0         = {:3.6f} +/- {:3.4E} [cm]\n' \
                  'BeamWidthX = {:3.6f} +/- {:3.4E} [cm]\n' \
                  'BeamWidthY = {:3.6f} +/- {:3.4E} [cm]\n' \
                  'sigmaZ0    = {:3.6f} +/- {:3.4E} [cm]\n' \
                  'dxdz       = {:3.6E} +/- {:3.4E} [rad]\n'\
                  'dydz       = {:3.6E} +/- {:3.4E} [rad]'  \
                  .format(self.X         , self.Xerr         ,
                          self.Y         , self.Yerr         ,
                          self.Z         , self.Zerr         ,
                          self.beamWidthX, self.beamWidthXerr,
                          self.beamWidthY, self.beamWidthYerr,
                          self.sigmaZ    , self.sigmaZerr    ,
                          self.dxdz      , self.dxdzerr      ,
                          self.dydz      , self.dydzerr      )
        print toWrite

 
    
       
if __name__ == '__main__':
#     mybs = BeamSpot()
#     myself.Dump('bs_dump_dummy.txt', 'w+')

    mybs = BeamSpot()
    mybs.ReadXML('/afs/cern.ch/work/m/manzoni/beamspot/CMSSW_7_5_0_pre4/src/RecoVertex/BeamSpotProducer/python/workflow/utils/payload_hash.xml')
    mybs.Dump('bs_dump_from_xml.txt', 'w+')
    mybs.Print()
