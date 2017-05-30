from CRABClient.UserUtilities import config
config = config()

config.General.requestName  = 'BS_systematics_sumptUP_trksDOWN'
#config.General.workArea     = 'Fill_5106'
config.General.workArea     = 'Fill_5441'

config.JobType.pluginName   = 'Analysis'
config.JobType.psetName     = 'analyze_d0_phi_cfg.py' #'BeamFit_LumiBased_NewAlignWorkflow.py'
config.JobType.outputFiles  = ['BS_systematics_sumptUP_trksDOWN.txt'] #['BeamFit_LumiBased_NewAlignWorkflow_alcareco.txt']

#config.Data.inputDataset      = '/ZeroBias/Run2016G-TkAlMinBias-PromptReco-v1/ALCARECO'
#config.Data.inputDataset      = '/JetHT/Run2016E-22Feb2017-v1/AOD'
config.Data.inputDataset      = '/JetHT/Run2016H-22Feb2017-v1/AOD'

config.Data.lumiMask        = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/DCSOnly/json_DCSONLY.txt' #'json_DCSONLY.txt'
#config.Data.runRange        = '277094-277112' #Fill 5106
config.Data.runRange        = '283863-283865' #Fill 5441
config.Data.useParent       = False
config.Data.inputDBS        = 'global'
config.Data.splitting       = 'LumiBased'
config.Data.unitsPerJob     = 30
config.Data.outLFNDirBase   = '/store/user/fbrivio/BeamSpot' #'/store/group/phys_tracking/beamspot/13TeV'

config.Site.storageSite = 'T3_IT_MIB' #'T2_CH_CERN'