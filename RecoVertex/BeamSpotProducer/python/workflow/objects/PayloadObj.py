#!/usr/bin/python

import ROOT
from array import array
from RecoVertex.BeamSpotProducer.workflow.objects.BeamSpotObj import BeamSpot
from RecoVertex.BeamSpotProducer.workflow.objects.IOVObj import IOV

class Payload(object):
    '''
    Class meant to connect the BeamSpot fit results as saved in a typical
    Payload ASCII file, to actual BeamSpot objects, that are much 
    nicer to handle
    '''
    
    def __init__(self, files):
        '''
        '''
        # can pass a single or a list of txt files
        if not isinstance(files, (list, tuple)):
            files = [files]

        self._readFiles(files)
    
    def _readFiles(self, files):
        '''
        Reads the Payload files.
        '''
        lines = []
        
        for f in files:
            with open(f, 'r') as file:
                for line in file:
                    lines.append(line) 
        
        self.lines = lines
        
    def splitBySingleFit(self):
        '''
        Parses the ASCII files and slices them into a chunk for each fit.
        '''
        singleFits = []

        for i, line in enumerate(self.lines):
            line = line.rstrip()
            # strings and numbers hardcoded here strictly depend on 
            # the format of the Payload file 
            if 'LumiRange' in line:
                singleFits.append([self.lines[j].rstrip() \
                                   for j in range(i-3, i+20)])
        
        return singleFits    

    def fromTextToBS(self, iov = False):
        '''
        Return a dictionary of dictionaries, as the following:
        { Run : {Lumi Range: BeamSpot Fit Object} }
        
        Parses the files passed when the Payload is instantiated.
        '''
        
        singleFits = self.splitBySingleFit()
        
        beamspots = {}
        
        for item in singleFits:
            
            bs = BeamSpot()
            bs.Read(item)
            
            if iov:
                beamspots[bs.GetIOV()] = bs

            else:
                if bs.IOVfirst == bs.IOVlast:
                    lsrange = bs.IOVfirst
                else:
                    lsrange = '%d-%d' %(bs.IOVfirst, bs.IOVlast)
                
                try:   
                    beamspots[bs.Run][lsrange] = bs
                except:
                    toadd = { bs.Run : {lsrange : bs} }
                    beamspots.update( toadd )
                   
        return beamspots
    
    def getProcessedLumiSections(self):
        '''
        Returns a dictionary with the run numbers as keys and the full
        list of lumi sections processed (fully extended), like:
        { Run : [ LS1, LS2, LS10, ...]}
        '''
        
        beamspots = self.fromTextToBS()
        
        runsAndLumis = { run : [] for run in beamspots.keys() }
        
        for k, v in beamspots.items():
            
            for lumi_range in v.keys():
                try:
                    start = int( lumi_range.split('-')[0] )
                    end   = int( lumi_range.split('-')[1] ) + 1
                except:
                    start = lumi_range
                    end   = start +1
                runsAndLumis[k].extend( range(start, end) )
            
            # sort LS nicely
            runsAndLumis[k] = sorted(runsAndLumis[k])

        return runsAndLumis

    def plot(self, variable, iRun, fRun, iLS = -1, fLS = 1e6, savePdf = False):
        '''
        Plot a BS parameter as a function of LS.
        Allows multiple LS bins.
        Can run over different runs or over a single run different LS
        '''
        afterFirst = lambda x : (x.RunFirst >= iRun and x.LumiFirst >= iLS)
        beforeLast = lambda x : (x.RunLast  <= fRun and x.LumiLast  <= fLS)
        
        # get the list of BS objects
        myBS = {k:v for k, v in self.fromTextToBS(iov = True).items()
                if afterFirst(k) and beforeLast(k)}

        runs = list(set(v.Run for v in myBS.values()))
        
        x  = []
        y  = []
        xe = []
        ye = []
        
        totBins = 0
        binLabels = {}
        
        for run in sorted(runs):

            nowBS = {k:v for k, v in myBS.items() if v.Run == run}
            nBins = len(nowBS)
            totBins += nBins
            binLabels[totBins] = str(run)
            
            semiSum  = lambda k : 0.5 * (k.LumiLast + k.LumiFirst) * (k.LumiLast != k.LumiFirst)
            semiDiff = lambda k : 0.5 * (k.LumiLast - k.LumiFirst + 1 )

            x .extend([semiSum(k) + totBins         for k in nowBS.keys()  ])
            y .extend([getattr(v, variable)         for v in nowBS.values()])
            xe.extend([semiDiff(k)                  for k in nowBS.keys()  ])
            ye.extend([getattr(v, variable + 'err') for v in nowBS.values()])
                
        ax = array('f', x)
        ay = array('f', y)
        
        axe = array('f', xe)
        aye = array('f', ye)
        
        tge = ROOT.TGraphErrors(totBins, ax, ay, axe, aye)        
        
        print '\n\n=='
        for index, label in binLabels.items():
            binIndex = tge.GetXaxis().FindBin(index)
            print index, '\t', binIndex, '\t', binIndex - index
            print tge.GetXaxis().GetBinLabel(index)
            tge.GetXaxis().SetBinLabel(2*index+1, label)

        import pdb ; pdb.set_trace()
        
        iRun = max(iRun, sorted(runs)[0])
        fRun = min(fRun, sorted(runs)[-1])
        
        tge.SetTitle('Run %d - %d'  %(iRun, fRun))
        tge.GetXaxis().SetTitle('Run')

        if iRun == fRun:
            iLS = max(iLS, min([v.IOVfirst for v in nowBS.values()]))
            fLS = min(fLS, max([v.IOVfirst for v in nowBS.values()]))
            tge.SetTitle('Run %d Lumi %d - %d'  %(iRun, iLS, fLS))
            tge.GetXaxis().SetTitle('Lumi Section')
            
        tge.GetYaxis().SetTitle('BeamSpot %s %s' 
                                %(variable, '[cm]'*(not 'dz' in variable)))
        tge.SetMarkerStyle(8)
        tge.GetYaxis().SetTitleOffset(1.5)
       
        c1 = ROOT.TCanvas('','',1000,700)
        ROOT.gPad.SetGridx()
        ROOT.gPad.SetGridy()
        tge.Draw('AP')
        if savePdf: 
            c1.SaveAs('BS_plot_%d_%d_%s.pdf' %(iRun, fRun, variable))


if __name__ == '__main__':

    #file = '/afs/cern.ch/user/m/manzoni/public/beamspot_validation/' \
    #       'BeamFit_LumiBased_NewAlignWorkflow_alcareco_Run247388.txt'


    file = '/afs/cern.ch/user/f/fiorendi/public/beamSpot/'\
           'beamspot_firstData_run247324_byLumi_all_lumi98_107.txt'
    file = '/afs/cern.ch/user/f/fiorendi/public/beamSpot/bs_weighted_results_246908.txt'
    file = '/afs/cern.ch/work/m/manzoni/beamspot/CMSSW_7_5_DEVEL_X_2015-06-10-1100/src/RecoVertex/BeamSpotProducer/python/workflow/utils/all_runs_16_june_2015_by_run_REMOVE_DUPLICATES.txt'
    myPL = Payload(file)
    
    #myPL = Payload('/afs/cern.ch/work/m/manzoni/beamspot/CMSSW_7_4_0_pre8/src/'\
    #               'RecoVertex/BeamSpotProducer/python/workflow/cfg/'          \
    #               'Runs2012B_FULL/Results/XRepFinal_1_195660_1.txt'           )
    
    #myPL = Payload('payload_test.txt')
    allLines = myPL.splitBySingleFit()
    
    allBs = myPL.fromTextToBS()

    allBs2 = myPL.fromTextToBS(iov = True)
    
    #allBs[195660][60].Dump('bs_dump_195660_LS60.txt', 'w+')
    #allBs[247324][98].Dump('bs_dump_247388_LS60.txt', 'w+')
    
    print myPL.getProcessedLumiSections()

    myPL.plot('X'         , 246908, 999999, savePdf = True)
    myPL.plot('Y'         , 246908, 999999, savePdf = True)
    myPL.plot('Z'         , 246908, 999999, savePdf = True)
    myPL.plot('sigmaZ'    , 246908, 999999, savePdf = True)
    myPL.plot('dxdz'      , 246908, 999999, savePdf = True)
    myPL.plot('dydz'      , 246908, 999999, savePdf = True)
    myPL.plot('beamWidthX', 246908, 999999, savePdf = True)
    myPL.plot('beamWidthY', 246908, 999999, savePdf = True)

#     myPL.plot('X'         , 246908, 246908, savePdf = True)
#     myPL.plot('Y'         , 246908, 246908, savePdf = True)
#     myPL.plot('Z'         , 246908, 246908, savePdf = True)
#     myPL.plot('sigmaZ'    , 246908, 246908, savePdf = True)
#     myPL.plot('dxdz'      , 246908, 246908, savePdf = True)
#     myPL.plot('dydz'      , 246908, 246908, savePdf = True)
#     myPL.plot('beamWidthX', 246908, 246908, savePdf = True)
#     myPL.plot('beamWidthY', 246908, 246908, savePdf = True)

#     myPL.plot('X'         , 246908, iLS = 90, fLS = 110, savePdf = True)
