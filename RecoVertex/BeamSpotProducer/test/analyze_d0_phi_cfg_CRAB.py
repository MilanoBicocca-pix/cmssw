from CRABClient.UserUtilities import config
config = config()

config.General.requestName  = 'BS_LUT_run278366_sumptUP_trksDOWN'
#config.General.workArea     = 'Fill_5106'
#config.General.workArea     = 'Fill_5441_LUT'
config.General.workArea     = 'new_LUT'

config.JobType.pluginName   = 'Analysis'
config.JobType.psetName     = 'analyze_d0_phi_cfg.py' #'BeamFit_LumiBased_NewAlignWorkflow.py'
config.JobType.outputFiles  = ['BS_LUT_run278366_sumptUP_trksDOWN.txt'] #['BeamFit_LumiBased_NewAlignWorkflow_alcareco.txt']

config.JobType.inputFiles=['/afs/cern.ch/work/f/fbrivio/beamSpot/systematics/CMSSW_9_0_2_patch1/src/BeamSpotCalibration/errorScaleCal/test/PU_test/new_LUT/LUTs/LUT_X_PU_4bins.root']

#config.Data.inputDataset      = '/ZeroBias/Run2016G-TkAlMinBias-PromptReco-v1/ALCARECO'
#config.Data.inputDataset      = '/JetHT/Run2016E-22Feb2017-v1/AOD'
#config.Data.inputDataset      = '/JetHT/Run2016H-22Feb2017-v1/AOD'
#config.Data.inputDataset      = '/JetHT/Run2016G-22Feb2017-v1/AOD'
config.Data.inputDataset      = '/JetHT/Run2016F-22Feb2017-v1/AOD'

config.Data.lumiMask        = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/DCSOnly/json_DCSONLY.txt'
#config.Data.runRange        = '277094-277112' #Fill 5106
#config.Data.runRange        = '283865' #Fill 5441 - 283863-283865
#config.Data.runRange        = '278820' #Fill 5199
config.Data.runRange        = '278366' #Fill 5181
config.Data.useParent       = False
config.Data.publication     = False
config.Data.inputDBS        = 'global'
config.Data.splitting       = 'LumiBased'
config.Data.unitsPerJob     = 30
config.Data.outLFNDirBase   = '/store/group/phys_tracking/beamspot/13TeV' #'/store/user/fbrivio/BeamSpot' #

config.Site.storageSite = 'T2_CH_CERN' #'T3_IT_MIB' #