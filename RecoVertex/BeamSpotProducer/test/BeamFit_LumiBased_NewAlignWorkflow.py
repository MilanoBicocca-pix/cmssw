import FWCore.ParameterSet.Config as cms

process = cms.Process("BSworkflow")

process.source = cms.Source("PoolSource",
    #fileNames = cms.untracked.vstring(
      #"/store/express/Run2015A/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/246/959/00000/14174DF2-490A-E511-9862-02163E0143E9.root",
	  # Fill 5106 2016E
	  #"/store/data/Run2016E/JetHT/AOD/22Feb2017-v1/130001/FEDB164F-B4FA-E611-8735-0CC47A4D7632.root",
    #)
    fileNames = cms.untracked.vstring('root://cms-xrd-global.cern.ch//store/data/Run2016E/JetHT/AOD/22Feb2017-v1/110000/023753BD-18FB-E611-859D-0025905A609A.root')
)

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport  = cms.untracked.PSet(
    reportEvery = cms.untracked.int32(100),
)
process.MessageLogger.debugModules = ['BeamSpotAnalyzer']

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1000)
)

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

process.load("RecoVertex.BeamSpotProducer.BeamSpot_cfi")
process.load("Configuration.StandardSequences.MagneticField_cff") 
process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff") 
# this GT is for the Express, to be consistent with the file above
# in general this GT should be for the ReReco
process.GlobalTag.globaltag = '80X_dataRun2_2016LegacyRepro_Candidate_v5'

## Track refit
process.load("RecoTracker.TrackProducer.TrackRefitters_cff")

# remove the following lines if you run on RECO files
#process.TrackRefitter.src = 'ALCARECOTkAlMinBias'
process.TrackRefitter.NavigationSchool = ''


## PV refit
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")

from RecoVertex.PrimaryVertexProducer.OfflinePrimaryVertices_cfi import offlinePrimaryVertices 
process.offlinePrimaryVerticesFromRefittedTrks  = offlinePrimaryVertices.clone()
process.offlinePrimaryVerticesFromRefittedTrks.TrackLabel                                       = cms.InputTag("generalTracks") #cms.InputTag("TrackRefitter")
process.offlinePrimaryVerticesFromRefittedTrks.vertexCollections.maxDistanceToBeam              = 1
process.offlinePrimaryVerticesFromRefittedTrks.TkFilterParameters.maxNormalizedChi2             = 20
process.offlinePrimaryVerticesFromRefittedTrks.TkFilterParameters.minSiliconLayersWithHits      = 5
process.offlinePrimaryVerticesFromRefittedTrks.TkFilterParameters.maxD0Significance             = 5.0 
process.offlinePrimaryVerticesFromRefittedTrks.TkFilterParameters.minPixelLayersWithHits        = 2   


                     
## BeamSpot fit
process.load("RecoVertex.BeamSpotProducer.d0_phi_analyzer_cff")

process.d0_phi_analyzer.BeamFitter.WriteAscii                = True
process.d0_phi_analyzer.BeamFitter.AsciiFileName             = 'test_systematics_FirstPV.txt' #'BeamFit_LumiBased_NewAlignWorkflow_alcareco.txt'
process.d0_phi_analyzer.BeamFitter.AppendRunToFileName       = False
process.d0_phi_analyzer.BeamFitter.InputBeamWidth            = -1
process.d0_phi_analyzer.BeamFitter.MaximumImpactParameter    = 1.0
process.d0_phi_analyzer.BeamFitter.MaximumNormChi2           = 10
process.d0_phi_analyzer.BeamFitter.MinimumInputTracks        = 50
process.d0_phi_analyzer.BeamFitter.MinimumPixelLayers        = -1
process.d0_phi_analyzer.BeamFitter.MinimumPt                 = 1.0
process.d0_phi_analyzer.BeamFitter.MinimumTotalLayers        = 6
process.d0_phi_analyzer.BeamFitter.OutputFileName            = 'test_systematics.root' #'BeamFit_LumiBased_Workflow_alcareco.root'
process.d0_phi_analyzer.BeamFitter.TrackAlgorithm            = cms.untracked.vstring()
process.d0_phi_analyzer.BeamFitter.TrackCollection           = 'generalTracks' #'TrackRefitter'
process.d0_phi_analyzer.BeamFitter.SaveFitResults            = False
process.d0_phi_analyzer.BeamFitter.SaveNtuple                = False
process.d0_phi_analyzer.BeamFitter.SavePVVertices            = False
   
process.d0_phi_analyzer.PVFitter.Apply3DFit                  = True
process.d0_phi_analyzer.PVFitter.minNrVerticesForFit         = 10 
process.d0_phi_analyzer.PVFitter.nSigmaCut                   = 50.0
process.d0_phi_analyzer.PVFitter.VertexCollection            = 'offlinePrimaryVerticesFromRefittedTrks'
#process.d0_phi_analyzer.PVFitter.useOnlyFirstPV              = True
#process.d0_phi_analyzer.PVFitter.minSumPt                    = 50.0
#process.d0_phi_analyzer.PVFitter.minVertexNTracks            = 30

process.d0_phi_analyzer.BSAnalyzerParameters.fitEveryNLumi   = 1
process.d0_phi_analyzer.BSAnalyzerParameters.resetEveryNLumi = 1


process.p = cms.Path(process.offlineBeamSpot                        + 
                     #process.TrackRefitter                          +
                     process.offlinePrimaryVerticesFromRefittedTrks +
                     process.d0_phi_analyzer)
