import FWCore.ParameterSet.Config as cms

process = cms.Process("d0phi")
# initialize MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.load("RecoVertex.BeamSpotProducer.d0_phi_analyzer_cff")

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(

#'root://cms-xrd-global.cern.ch//store/data/Run2016E/JetHT/AOD/22Feb2017-v1/110000/023753BD-18FB-E611-859D-0025905A609A.root'
# runs=  277094 - 277096 - 277127 (fill 5106 in runE)

#'root://cms-xrd-global.cern.ch//store/data/Run2016E/JetHT/AOD/22Feb2017-v1/130000/007C4941-E8FA-E611-B4F5-0CC47A4D76C0.root', # run 277127 (+277305)
#'root://cms-xrd-global.cern.ch//store/data/Run2016E/JetHT/AOD/22Feb2017-v1/130000/0034884F-E8FA-E611-8BB6-0025905B85D8.root', # runs 277096 - 277112

#'root://cmsxrootd.fnal.gov//store/data/Run2016G/JetHT/AOD/22Feb2017-v1/110001/8AF339B2-ABFC-E611-A57C-0CC47A4C8E2E.root', runG

# Fill 5441, runH , run = 283863
#'/store/data/Run2016H/JetHT/AOD/22Feb2017-v1/90000/8A4BC9C0-DCFD-E611-9AF8-FA163EC17E40.root',

# runG, run = 278820
'/store/data/Run2016G/JetHT/AOD/22Feb2017-v1/130000/243C2213-92F9-E611-B098-001E67E34034.root',
						  	  
  						             ),
									 #firstRun = cms.untracked.uint32(277127)
			   )

#process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange('124120:1-124120:59')

process.maxEvents = cms.untracked.PSet(
                                       input = cms.untracked.int32(-1) #1500
                                      )

process.options   = cms.untracked.PSet(
                                       wantSummary = cms.untracked.bool(False)
                                      )

# this is for filtering on L1 technical trigger bit
process.load('L1TriggerConfig.L1GtConfigProducers.L1GtTriggerMaskTechTrigConfig_cff')
process.load('HLTrigger/HLTfilters/hltLevel1GTSeed_cfi')

process.hltLevel1GTSeed.L1TechTriggerSeeding     = cms.bool(True)
process.hltLevel1GTSeed.L1SeedsLogicalExpression = cms.string('0 AND ( 40 OR 41 )')

#### remove beam scraping events
process.noScraping = cms.EDFilter(
                                  "FilterOutScraping",
    				  applyfilter = cms.untracked.bool(True) ,
    				  debugOn     = cms.untracked.bool(False), ## Or 'True' to get some per-event info
    				  numtrack    = cms.untracked.uint32(10) ,
    				  thresh      = cms.untracked.double(0.20)
                                 )

#process.p = cms.Path(process.hltLevel1GTSeed + process.d0_phi_analyzer)
process.p = cms.Path(process.d0_phi_analyzer)
process.MessageLogger.debugModules = ['BeamSpotAnalyzer']

#######################

process.MessageLogger.cerr.FwkReport.reportEvery = 1000

# run over STA muons
#process.d0_phi_analyzer.BeamFitter.TrackCollection = cms.untracked.InputTag('ALCARECOTkAlMinBias') #,'UpdatedAtVtx')
#process.d0_phi_analyzer.BeamFitter.IsMuonCollection = True

process.d0_phi_analyzer.BeamFitter.WriteAscii                = True
process.d0_phi_analyzer.BeamFitter.AsciiFileName             = 'BS_systematics_central.txt'
process.d0_phi_analyzer.BeamFitter.AppendRunToFileName       = True
process.d0_phi_analyzer.BeamFitter.InputBeamWidth            = -1
process.d0_phi_analyzer.BeamFitter.MaximumImpactParameter    = 1.0
process.d0_phi_analyzer.BeamFitter.MaximumNormChi2           = 10
process.d0_phi_analyzer.BeamFitter.MinimumInputTracks        = 2 #50
process.d0_phi_analyzer.BeamFitter.MinimumPixelLayers        = -1
process.d0_phi_analyzer.BeamFitter.MinimumTotalLayers 	     = 6
process.d0_phi_analyzer.BeamFitter.MinimumPt                 = 1.0
process.d0_phi_analyzer.BeamFitter.OutputFileName 	         = 'BS_systematics_central.root' #'relvalQCD.root'
process.d0_phi_analyzer.BeamFitter.TrackAlgorithm            = cms.untracked.vstring()
process.d0_phi_analyzer.BeamFitter.TrackCollection           = 'generalTracks'

process.d0_phi_analyzer.BeamFitter.SaveNtuple     	     = False
process.d0_phi_analyzer.BeamFitter.SavePVVertices 	     = True
process.d0_phi_analyzer.BeamFitter.SaveFitResults 	     = False

# defalt values: sumPt= 50.    - NTracks=20 (30 is the new one)
# median values: sumPt= 289.36 - NTracks=76.8
# new median val: sumPt=301.6  - NTracks=76.54
process.d0_phi_analyzer.PVFitter.Apply3DFit       	     = True
process.d0_phi_analyzer.PVFitter.useOnlyFirstPV              = True
process.d0_phi_analyzer.PVFitter.errorScale                  = 1.
process.d0_phi_analyzer.PVFitter.minSumPt                    = 50.0
process.d0_phi_analyzer.PVFitter.maxSumPt                    = 10000.0
process.d0_phi_analyzer.PVFitter.minVertexNTracks            = 30
process.d0_phi_analyzer.PVFitter.maxVertexNTracks            = 10000

# fit as function of lumi sections
process.d0_phi_analyzer.BSAnalyzerParameters.fitEveryNLumi   = 1 #2
process.d0_phi_analyzer.BSAnalyzerParameters.resetEveryNLumi = 1 #2
