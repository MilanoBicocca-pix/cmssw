#!/usr/bin/python

# produce the BeamSpot for the run and LS considered in this analysis
# https://indico.cern.ch/event/390912/contribution/0/material/slides/1.pdf

from RecoVertex.BeamSpotProducer.workflow.objects.PayloadObj  import Payload
from RecoVertex.BeamSpotProducer.workflow.utils.beamSpotMerge import averageBeamSpot

pl_1 = Payload('/afs/cern.ch/user/f/fiorendi/public/beamSpot/run247324/beamspot_firstData_run247324_byLumi_Run247324.txt'    )
pl_2 = Payload('/afs/cern.ch/user/f/fiorendi/public/beamSpot/run247324/beamspot_firstData_run247324_byLumi_zb2_Run247324.txt')
pl_3 = Payload('/afs/cern.ch/user/f/fiorendi/public/beamSpot/run247324/beamspot_firstData_run247324_byLumi_zb3_Run247324.txt')
pl_4 = Payload('/afs/cern.ch/user/f/fiorendi/public/beamSpot/run247324/beamspot_firstData_run247324_byLumi_zb4_Run247324.txt')

allbs_1 = pl_1.fromTextToBS()[247324].values()[87:]
allbs_2 = pl_2.fromTextToBS()[247324].values()[87:]
allbs_3 = pl_3.fromTextToBS()[247324].values()[87:]
allbs_4 = pl_4.fromTextToBS()[247324].values()[87:]

allbs = allbs_1 + allbs_2 + allbs_3 + allbs_4

avebs = averageBeamSpot(allbs)

avebs.Dump('beamspot_firstData_run247324_byRun_Run247324_ZeroBias1to4.txt')
