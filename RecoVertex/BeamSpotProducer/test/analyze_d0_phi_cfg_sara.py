import FWCore.ParameterSet.Config as cms

process = cms.Process("d0phi")

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.load("RecoVertex.BeamSpotProducer.d0_phi_analyzer_cff")

# from fileList_StreamExpressPCL import * 
process.source = cms.Source("PoolSource",
                   fileNames = cms.untracked.vstring(
#                    streamExpressList_Old
                    "file:/afs/cern.ch/work/f/fiorendi/private/BeamSpot/CMSSW_7_4_0/src/skim_Tier0_PCLTest_SUPERBUNNIES_vocms047_StreamExpressv3_alcareco_lumi500-900.root",
#                   "file:/afs/cern.ch/work/f/fiorendi/private/BeamSpot/CMSSW_7_4_0/src/skim_StreamExpress2012D_lumi690-710_part1.root",
			        )
			     )

# process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange('207231:500-207231:900')
# process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange('207231:690-207231:710')

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
process.d0_phi_analyzer.BeamFitter.AsciiFileName  	         = 'BeamFit_207231_PCLReplay_Lumi500_900.txt'
process.d0_phi_analyzer.BeamFitter.Debug                     = True
process.d0_phi_analyzer.BeamFitter.InputBeamWidth            = -1
process.d0_phi_analyzer.BeamFitter.MaximumImpactParameter    = 1.0 # diff from alca
process.d0_phi_analyzer.BeamFitter.MaximumNormChi2    	     = 10
process.d0_phi_analyzer.BeamFitter.MinimumInputTracks 	     = 50   # diff from alca
process.d0_phi_analyzer.BeamFitter.MinimumPixelLayers 	     = -1
process.d0_phi_analyzer.BeamFitter.MinimumPt                 = 1.0
process.d0_phi_analyzer.BeamFitter.MinimumTotalLayers 	     = 6
process.d0_phi_analyzer.BeamFitter.OutputFileName 	         = 'run207231_PCLReplay_Lumi500_900_addCombinedResultsTree.root' #AtVtx10000.root'
process.d0_phi_analyzer.BeamFitter.TrackAlgorithm            = cms.untracked.vstring()
#process.d0_phi_analyzer.BeamFitter.TrackQuality             = cms.untracked.vstring("highPurity")
process.d0_phi_analyzer.BeamFitter.SaveFitResults 	         = True
process.d0_phi_analyzer.BeamFitter.SaveNtuple     	         = True
process.d0_phi_analyzer.BeamFitter.SavePVVertices 	         = True

process.d0_phi_analyzer.PVFitter.Apply3DFit       	         = True
process.d0_phi_analyzer.PVFitter.minNrVerticesForFit         = 10
process.d0_phi_analyzer.PVFitter.nSigmaCut       	         = 50.0

#sara
process.d0_phi_analyzer.BeamFitter.TrackCollection           = cms.untracked.InputTag('ALCARECOTkAlMinBias')


# fit as function of lumi sections
process.d0_phi_analyzer.BSAnalyzerParameters.fitEveryNLumi   = 1
process.d0_phi_analyzer.BSAnalyzerParameters.resetEveryNLumi = 1
