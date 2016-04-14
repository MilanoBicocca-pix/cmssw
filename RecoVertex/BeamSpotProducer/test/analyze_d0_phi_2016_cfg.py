import FWCore.ParameterSet.Config as cms

process = cms.Process("d0phi")

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.load("RecoVertex.BeamSpotProducer.d0_phi_analyzer_cff")

process.source = cms.Source("PoolSource",
                   fileNames = cms.untracked.vstring(
"root://xrootd.unl.edu//store/data/Commissioning2016/ZeroBias5/RECO/PromptReco-v1/000/269/207/00000/0874B96A-7601-E611-98B9-02163E014765.root",
"root://xrootd.unl.edu//store/data/Commissioning2016/ZeroBias5/RECO/PromptReco-v1/000/269/207/00000/28CFC56F-7601-E611-8244-02163E01228A.root",
"root://xrootd.unl.edu//store/data/Commissioning2016/ZeroBias5/RECO/PromptReco-v1/000/269/207/00000/38CD96AE-7601-E611-A333-02163E013886.root",
"root://xrootd.unl.edu//store/data/Commissioning2016/ZeroBias5/RECO/PromptReco-v1/000/269/207/00000/6067CE7D-7601-E611-B87C-02163E014799.root",
"root://xrootd.unl.edu//store/data/Commissioning2016/ZeroBias5/RECO/PromptReco-v1/000/269/207/00000/76FCD1B5-7601-E611-90E6-02163E0127C0.root",
"root://xrootd.unl.edu//store/data/Commissioning2016/ZeroBias5/RECO/PromptReco-v1/000/269/207/00000/881B61A4-7701-E611-A656-02163E011A87.root",
"root://xrootd.unl.edu//store/data/Commissioning2016/ZeroBias5/RECO/PromptReco-v1/000/269/207/00000/8AF14F42-7701-E611-82C4-02163E01287F.root",
"root://xrootd.unl.edu//store/data/Commissioning2016/ZeroBias5/RECO/PromptReco-v1/000/269/207/00000/9A1CEC7F-7601-E611-BA85-02163E012193.root",
"root://xrootd.unl.edu//store/data/Commissioning2016/ZeroBias5/RECO/PromptReco-v1/000/269/207/00000/A49F1EC4-7701-E611-9C1F-02163E011E2F.root",
"root://xrootd.unl.edu//store/data/Commissioning2016/ZeroBias5/RECO/PromptReco-v1/000/269/207/00000/B21DE734-7601-E611-A23D-02163E011D60.root",
"root://xrootd.unl.edu//store/data/Commissioning2016/ZeroBias5/RECO/PromptReco-v1/000/269/207/00000/B41AA2B4-7801-E611-9BE3-02163E0145FA.root",
"root://xrootd.unl.edu//store/data/Commissioning2016/ZeroBias5/RECO/PromptReco-v1/000/269/207/00000/C0361E44-7701-E611-801D-02163E011ADB.root",
"root://xrootd.unl.edu//store/data/Commissioning2016/ZeroBias5/RECO/PromptReco-v1/000/269/207/00000/D665B521-7701-E611-88F0-02163E0143E9.root",
"root://xrootd.unl.edu//store/data/Commissioning2016/ZeroBias5/RECO/PromptReco-v1/000/269/207/00000/E8898737-7701-E611-8748-02163E012A04.root",
        )
)

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

process.d0_phi_analyzer.BeamFitter.WriteAscii  	             = True
process.d0_phi_analyzer.BeamFitter.AsciiFileName  	         = 'result_BeamFit_test.txt'
process.d0_phi_analyzer.BeamFitter.AppendRunToFileName       = cms.untracked.bool(True)
process.d0_phi_analyzer.BeamFitter.Debug                     = cms.untracked.bool(True)
process.d0_phi_analyzer.BeamFitter.InputBeamWidth            = -1
process.d0_phi_analyzer.BeamFitter.MaximumImpactParameter    = 1.0 # diff from alca
process.d0_phi_analyzer.BeamFitter.MaximumNormChi2    	     = 10
process.d0_phi_analyzer.BeamFitter.MinimumInputTracks 	     = 50   # diff from alca
process.d0_phi_analyzer.BeamFitter.MinimumPt                 = 1.0
process.d0_phi_analyzer.BeamFitter.MinimumTotalLayers 	     = 6
process.d0_phi_analyzer.BeamFitter.MinimumPixelLayers 	     = -1


process.d0_phi_analyzer.BeamFitter.OutputFileName 	         = 'BeamFit_test.root' #AtVtx10000.root'
process.d0_phi_analyzer.BeamFitter.TrackAlgorithm            = cms.untracked.vstring()
#process.d0_phi_analyzer.BeamFitter.TrackQuality             = cms.untracked.vstring("highPurity")
process.d0_phi_analyzer.BeamFitter.SaveFitResults 	         = True
process.d0_phi_analyzer.BeamFitter.SaveNtuple     	         = True
process.d0_phi_analyzer.BeamFitter.SavePVVertices 	         = True

process.d0_phi_analyzer.BeamFitter.MinimumPixelLayers        = 0
process.d0_phi_analyzer.BeamFitter.MaximumZ                  = 60
process.d0_phi_analyzer.BeamFitter.FractionOfFittedTrks      = 0.9

process.d0_phi_analyzer.BeamFitter.BunchCrossings            = cms.untracked.vdouble()
process.d0_phi_analyzer.BeamFitter.FitOnlyd0Phi              = True

process.d0_phi_analyzer.PVFitter.Apply3DFit       	         = False
process.d0_phi_analyzer.PVFitter.minNrVerticesForFit         = 10
process.d0_phi_analyzer.PVFitter.nSigmaCut       	         = 50.0

#sara
# process.d0_phi_analyzer.BeamFitter.TrackCollection           = cms.untracked.InputTag('generalTracks')
# process.d0_phi_analyzer.BeamFitter.TrackCollection           = cms.untracked.InputTag('ALCARECOTkAlMinBias')


# fit as function of lumi sections
process.d0_phi_analyzer.BSAnalyzerParameters.fitEveryNLumi   = 1
process.d0_phi_analyzer.BSAnalyzerParameters.resetEveryNLumi = 1
