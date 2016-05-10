from RecoVertex.BeamSpotProducer.workflow.objects.BeamSpotWorkflowCfgObj import BeamSpotWorkflowCfg

'''
Template cfg file to be passed to BeamSporWorkflow
'''

cfg = BeamSpotWorkflowCfg()

cfg.sourceDir             = 'test/Results/'
cfg.archiveDir            = 'test/Archive/'
cfg.workingDir            = 'test/Working/'
cfg.jsonFileName          = 'beamspot_payload_2012BONLY_merged_JSON_all.txt'
cfg.databaseTag           = 'BeamSpotObjects_2009_LumiBased_SigmaZ_v29_offline'
cfg.dataSet               = '/StreamExpress/Run2012B-TkAlMinBias-v1/ALCARECO'
cfg.fileIOVBase           = 'lumibase'
cfg.dbIOVBase             = 'lumiid'
cfg.dbsTolerance          = 200000
cfg.dbsTolerancePercent   = 5.
cfg.rrTolerance           = 200000
cfg.missingFilesTolerance = 200000
cfg.missingLumisTimeout   = 0
cfg.mailList              = 'manzoni@cern.ch'
cfg.payloadFileName       = 'PayloadFile.txt'
