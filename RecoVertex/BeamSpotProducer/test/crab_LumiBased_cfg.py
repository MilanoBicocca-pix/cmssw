from CRABClient.UserUtilities import config

config = config()

config.General.transferOutputs = True

# 2015A
# config.General.requestName     = '2015A_23nov15_GT_74X_dataRun2_Candidate_2015_11_18_10_38_33_v2'
# config.General.workArea        = 'crab_nov15_rereco_2015A_v2'
# config.Data.inputDataset       = '/ZeroBias/Run2015A-PromptReco-v1/RECO'

# 2015B
# config.General.requestName     = '2015B_23nov15_GT_74X_dataRun2_Candidate_2015_11_18_10_38_33_v2'
# config.General.workArea        = 'crab_nov15_rereco_2015B_v2'
# config.Data.inputDataset       = '/ZeroBias/Run2015B-PromptReco-v1/RECO'

# 2015C
# config.General.requestName     = '2015C_23nov15_GT_74X_dataRun2_Candidate_2015_11_18_10_38_33_v2'
# config.General.workArea        = 'crab_nov15_rereco_2015C_v2'
# config.Data.inputDataset       = '/ZeroBias/Run2015C-PromptReco-v1/RECO'

# 2015Dv3
# config.General.requestName     = '2015D_v3_23nov15_GT_74X_dataRun2_Candidate_2015_11_18_10_38_33_v2'
# config.General.workArea        = 'crab_nov15_rereco_2015D_v3_v2'
# config.Data.inputDataset       = '/ZeroBias/Run2015D-PromptReco-v3/RECO'

# 2015Dv4
# config.General.requestName     = '2015D_v4_23nov15_GT_74X_dataRun2_Candidate_2015_11_18_10_38_33_v2'
# config.General.workArea        = 'crab_nov15_rereco_2015D_v4_v2'
# config.Data.inputDataset       = '/ZeroBias/Run2015D-PromptReco-v4/RECO'

# 2015E
config.General.requestName     = '2015E_23nov15_GT_74X_dataRun2_Candidate_2015_11_18_10_38_33_v2'
config.General.workArea        = 'crab_nov15_rereco_2015E_v2'
config.Data.inputDataset       = '/ZeroBias/Run2015E-PromptReco-v1/RECO'


config.JobType.psetName        = 'BeamFit_LumiBased_NewAlignWorkflow.py'
config.JobType.pluginName      = 'Analysis'
config.JobType.outputFiles     = ['BeamFit_LumiBased_NewAlignWorkflow_alcareco.txt']

config.Data.unitsPerJob        = 10
config.Data.splitting          = 'LumiBased'

# JSON files:
# /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/
config.Data.lumiMask           = 'json_DCSONLY.txt'
# config.Data.runRange           = '246908-247644'
config.Data.publication        = False
config.Data.outLFNDirBase      = '/store/group/phys_tracking/beamspot/'

config.Site.storageSite        = 'T2_CH_CERN'
