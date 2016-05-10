from RecoVertex.BeamSpotProducer.workflow.objects.PayloadObj  import Payload
from RecoVertex.BeamSpotProducer.workflow.utils.beamSpotMerge import cleanAndSort
from RecoVertex.BeamSpotProducer.workflow.utils.beamSpotMerge import splitByDrift
from RecoVertex.BeamSpotProducer.workflow.utils.beamSpotMerge import averageBeamSpot
from RecoVertex.BeamSpotProducer.workflow.utils.readJson      import readJson
from RecoVertex.BeamSpotProducer.workflow.utils.compareLists  import compareLists
from collections import OrderedDict

import os
import ROOT
from os.path import isfile, join

def getfiles(mypath, pattern):
    onlyfiles = ['/'.join([mypath, f]) for f in os.listdir(mypath) if isfile(join(mypath, f)) and pattern in f]
    return onlyfiles


# input parameters
initlumi  = 1  
endlumi   = 100000  


firstRun_2015A = 246865 
lastRun_2015A  = 250932
firstRun_2015B = 250985 
lastRun_2015B  = 253620 # split in B&C, however not in json, so no problem
firstRun_2015C = 253620 
lastRun_2015C  = 255621
firstRun_2015D = 256584
lastRun_2015D  = 258158


# copy result files from eos to local area
# for file in get_files('/store/group/phys_tracking/beamspot/ZeroBias/crab_Run2015D-v3_6Oct15_74X_dataRun2_Candidate_2015_10_06_09_25_21/151006_162657/0000','.txt'):
#   os.system('cmsStage ' + file + ' copy_of_crab_Run2015D_6Oct15_74X_dataRun2_Candidate_2015_10_06_09_25_21/')
# exit()

myPayload = Payload(
    getfiles('/afs/cern.ch/work/m/manzoni/public/eoyReReco_anyT/2015Dv3'      , 'BeamFit_LumiBased_NewAlignWorkflow_alcareco_') 
)

# # Plot fit results from txt file
# variables = [
#   'X'         ,
#   'Y'         ,
#   'Z'         ,
#   'sigmaZ'    ,
#   'dxdz'      ,
#   'dydz'      ,
#   'beamWidthX',
#   'beamWidthY'
# ]
# 
# histos_pre_merging  = []
# for var in variables:
#     h1 = myPayload.plot(var,  0, 999999, savePdf = True, returnHisto = True, dilated = 6, byFill = False)
#     histos_pre_merging.append(h1)
# 
# file_pre_merging.cd()
# for h1 in histos_pre_merging:
#     h1.Write()


# convert results into a dictionary  { Run : {Lumi Range: BeamSpot Fit Object} }
allBS            = myPayload.fromTextToBS() 
for irun,ivalues in allBS.items():
  allBS[irun] = cleanAndSort(allBS[irun])

# check if any run is missing
theJson   = "../../../Cert_13TeV_16Dec2015ReReco_Collisions15_25ns_JSON_v2.txt"
# theJson   = "../../../test/total_DCS_json_upTo256869.txt"

# # this returns a dictionary of runs and LS in the txt file, like {195660 : [1,2,3,...]}
runsLumisCrab = myPayload.getProcessedLumiSections() 
runsCrab      = runsLumisCrab.keys()

# # this returns a dictionary of runs and LS in the json file
# runsLumisJson = readJson(firstRun_2015C, lastRun_2015C, theJson, False)
# runsJson      = runsLumisJson.keys()

# filter for json file 
# runsCommon      = set(runsCrab) & set(runsJson)
# inCrabNotInJson = set(runsCrab) - set(runsJson)
# inJsonNotInCrab = set(runsJson) - set(runsCrab)
# print 'missing runs:'
# print inJsonNotInCrab

# for irun in runsCommon:
#   inJsonNotCrab, inCrabNotJson = compareLists(runsLumisCrab[irun], runsLumisJson[irun], 100, 'crab', 'json' )
#   if len(inJsonNotCrab) > 0:
#     print 'run ' + str(irun) 
#     for ls in inJsonNotCrab:
#       print str(ls) 

# remove LS not in json file 
#   for ls in inCrabNotJson:
#     del allBS[irun][ls]



# check drifts and create IOV
for irun,ivalues in allBS.items():
#   pairs = splitByDrift(allBS[irun], slopes = True, )                         #2015B 3.8T, 2015C 3.8T 2015D 3.8T
  pairs = splitByDrift(allBS[irun], slopes = False, )                          #2015B 0T, 2015C 0T 2015D 0T
#   pairs = splitByDrift(allBS[irun], slopes = False, relaxedCriteria = True ) #2015A
  for p in pairs:
    print p
    myrange = set(range(p[0], p[1] + 1)) & set(allBS[irun].keys())
    bs_list = [allBS[irun][i] for i in sorted(list(myrange))]
    aveBeamSpot = averageBeamSpot(bs_list)
    aveBeamSpot.Dump('2015D/bs_weighted_results_' + str(irun) + '_' + str(p[0]) +'_LumiIOV.txt', 'a+')
  # nb: the LumiIOV file is opened in "append mode"



# now evaluate average BS for the entire run
# pairs = [(initlumi, endlumi)]
# for p in pairs:
#     myrange = set(range(p[0], p[1] + 1)) & set(allBS[runNumber].keys())
#     bs_list = [allBS[runNumber][i] for i in sorted(list(myrange))]
#     aveBeamSpot = averageBeamSpot(bs_list)
#     aveBeamSpot.Dump('bs_weighted_results_' + str(runNumber) + '_AllRun.txt', 'w+')


