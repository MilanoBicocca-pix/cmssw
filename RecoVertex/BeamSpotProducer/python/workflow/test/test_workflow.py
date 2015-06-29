from RecoVertex.BeamSpotProducer.workflow.objects.PayloadObj  import Payload
from RecoVertex.BeamSpotProducer.workflow.utils.beamSpotMerge import cleanAndSort
from RecoVertex.BeamSpotProducer.workflow.utils.beamSpotMerge import splitByDrift
from RecoVertex.BeamSpotProducer.workflow.utils.beamSpotMerge import averageBeamSpot
from RecoVertex.BeamSpotProducer.workflow.utils.readJson      import readJson
from RecoVertex.BeamSpotProducer.workflow.utils.compareLists  import compareLists
from collections import OrderedDict
import os

# input parameters
runNumber = 247324
initlumi  = 1  
endlumi   = 100  
myPayload = Payload("../../../test/files_firstData/run247324/beamspot_firstData_run247324_byLumi_zb1_Run247324.txt")
theJson   = "../../../test/json_DCSONLY.txt"

# Plot fit results from txt file
variables = [
  'X'         ,
  'Y'         ,
  'Z'         ,
  'sigmaZ'    ,
  'dxdz'      ,
  'dydz'      ,
  'beamWidthX',
  'beamWidthY'
]

for ivar in variables: 
  myPayload.plot(ivar , runNumber, runNumber, savePdf = True)

allBS            = myPayload.fromTextToBS() 
allBS[runNumber] = cleanAndSort(allBS[runNumber])


# this returns a dictionary of runs and LS in the txt file, like {195660 : [1,2,3,...]}
runsLumisCrab = myPayload.getProcessedLumiSections() 

# this returns a dictionary of runs and LS in the json file
runsLumisJson = readJson(runNumber, theJson, False)


# filter for json file
inJsonNotCrab, inCrabNotJson = compareLists(runsLumisCrab[runNumber], runsLumisJson[runNumber], 100, 'crab', 'json' )
for ls in inCrabNotJson:
  del allBS[runNumber][ls]

# check drifts and create IOV
pairs = splitByDrift(allBS[runNumber])
print pairs

for p in pairs:
    myrange = set(range(p[0], p[1] + 1)) & set(allBS[runNumber].keys())
    bs_list = [allBS[runNumber][i] for i in sorted(list(myrange))]
    aveBeamSpot = averageBeamSpot(bs_list)
    aveBeamSpot.Dump('bs_weighted_results_' + str(runNumber) + '_LumiIOV.txt', 'a+')
    # nb: the LumiIOV file is opened in "append mode"

# now evaluate average BS for the entire run
pairs = [(initlumi, endlumi)]
for p in pairs:
    myrange = set(range(p[0], p[1] + 1)) & set(allBS[runNumber].keys())
    bs_list = [allBS[runNumber][i] for i in sorted(list(myrange))]
    aveBeamSpot = averageBeamSpot(bs_list)
    aveBeamSpot.Dump('bs_weighted_results_' + str(runNumber) + '_AllRun.txt', 'w+')
  







