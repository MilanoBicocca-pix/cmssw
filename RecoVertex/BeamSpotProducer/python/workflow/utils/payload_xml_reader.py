#!/usr/bin/python

from math import sqrt
from subprocess import PIPE, Popen
from RecoVertex.BeamSpotProducer.workflow.objects.BeamSpotObj  import BeamSpot
from RecoVertex.BeamSpotProducer.workflow.objects.DBEntryObj   import DBEntry
from RecoVertex.BeamSpotProducer.workflow.objects.IOVObj       import IOV
from RecoVertex.BeamSpotProducer.workflow.objects.PayloadObj   import Payload
from RecoVertex.BeamSpotProducer.workflow.utils.condDbCommands import getListOfUploadedIOV
from RecoVertex.BeamSpotProducer.workflow.utils.condDbCommands import dumpXMLPayloadByHash


# databaseTag = 'BeamSpotObjects_PCL_byLumi_v0_prompt'
databaseTag = 'BeamSpotObjects_PCL_byRun_v0_prompt'
firstIOV    = 246908 #247321
lastIOV     = 999999 #247324
# plFile      = 'all_runs_16_june_2015_by_run.txt'#'dummy_bs.txt'
# plFile      = 'dummy_bs.txt'
# plFile      = 'all_iov_24_june_2015_by_lumi_from247079.txt'#'dummy_bs.txt'
plFile      = 'all_iov_24_june_2015_by_run.txt'#'dummy_bs.txt'

dbentries = getListOfUploadedIOV(databaseTag, firstIOV, lastIOV)

for i, entry in enumerate(dbentries):
    print 'entry %d/%d' %(i+1, len(dbentries))
    try:
        nextEntry = dbentries[i+1]
    except:
        nextEntry = DBEntry()
    
    try:
        myxml = dumpXMLPayloadByHash(entry.hash)
        mybs = BeamSpot()
        mybs.ReadXML(myxml)
    except:
        print 'corrupted'
        print vars(entry)
        print 'skipping'
        import pdb ; pdb.set_trace()
        continue
    
    myiov = IOV()
    myiov.RunFirst  = entry.run
    myiov.RunLast   = entry.run
    myiov.LumiFirst = entry.firstLumi
    myiov.LumiLast  = max(-1, nextEntry.firstLumi - 1)

    mybs.SetIOV(myiov)
        
    mybs.Dump(plFile, 'a')

# 
from RecoVertex.BeamSpotProducer.workflow.objects.PayloadObj   import Payload
# plFile      = 'all_iov_24_june_2015_by_lumi.txt'#'dummy_bs.txt'
plFile = 'all_runs_16_june_2015_by_run_REMOVE_DUPLICATES.txt'
mypl = Payload(plFile)

histos = []

histos.append(mypl.plot('X'         , 246908, 999999, savePdf = True, returnHisto = True))
histos.append(mypl.plot('Y'         , 246908, 999999, savePdf = True, returnHisto = True))
histos.append(mypl.plot('Z'         , 246908, 999999, savePdf = True, returnHisto = True))
histos.append(mypl.plot('sigmaZ'    , 246908, 999999, savePdf = True, returnHisto = True))
histos.append(mypl.plot('dxdz'      , 246908, 999999, savePdf = True, returnHisto = True))
histos.append(mypl.plot('dydz'      , 246908, 999999, savePdf = True, returnHisto = True))
histos.append(mypl.plot('beamWidthX', 246908, 999999, savePdf = True, returnHisto = True))
histos.append(mypl.plot('beamWidthY', 246908, 999999, savePdf = True, returnHisto = True))

import ROOT
rootfile = ROOT.TFile('all_plots_byrun_2.root','recreate')
rootfile.cd()
for histo in histos:
    #histo.Draw()
    histo.Write()

rootfile.Close()

