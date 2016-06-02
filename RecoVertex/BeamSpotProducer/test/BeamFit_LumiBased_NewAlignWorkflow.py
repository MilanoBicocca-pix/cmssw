import FWCore.ParameterSet.Config as cms

process = cms.Process("BSworkflow")

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
#       "/store/data/Run2015A/ZeroBias/RECO/PromptReco-v1/000/248/038/00000/5C3E92F8-6614-E511-BF18-02163E0143EC.root",
      "/store/data/Run2015D/ZeroBias/RECO/PromptReco-v4/000/258/159/00000/0007AF4D-B36B-E511-8407-02163E012385.root",
    )
)

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport  = cms.untracked.PSet(
    reportEvery = cms.untracked.int32(10000),
)
process.MessageLogger.debugModules = ['BeamSpotAnalyzer']

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1) 
)

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

process.load("RecoVertex.BeamSpotProducer.BeamSpot_cfi")
process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff")
process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")
# process.GlobalTag.globaltag = '74X_dataRun2_Candidate_2015_10_06_09_25_21'
# process.GlobalTag.globaltag = '74X_dataRun2_Candidate_2015_11_18_10_38_33'
process.GlobalTag.globaltag = '74X_dataRun2_EOY_Candidate_v0' # 2015 EOY 0T
process.GlobalTag.toGet = cms.VPSet(
    cms.PSet(record = cms.string("TrackerAlignmentRcd"),
             tag = cms.string("TrackerAlignment_v14_0T_offline"),
             connect = cms.untracked.string("frontier://FrontierPrep/CMS_CONDITIONS")
            )
)



## Track refit
process.load("RecoTracker.TrackProducer.TrackRefitters_cff")

# remove the following lines if you run on RECO files
# process.TrackRefitter.src = 'ALCARECOTkAlMinBias'
# process.TrackRefitter.NavigationSchool = ''


# 
process.load("RecoTracker.MeasurementDet.MeasurementTrackerEventProducer_cfi")
process.MeasurementTrackerEvent.inactivePixelDetectorLabels = cms.VInputTag()
process.MeasurementTrackerEvent.inactiveStripDetectorLabels = cms.VInputTag() 


## PV refit
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")

from RecoVertex.PrimaryVertexProducer.OfflinePrimaryVertices_cfi import offlinePrimaryVertices 
process.offlinePrimaryVerticesFromRefittedTrks                                             = offlinePrimaryVertices.clone()
process.offlinePrimaryVerticesFromRefittedTrks.TrackLabel                                  = cms.InputTag("TrackRefitter") 
process.offlinePrimaryVerticesFromRefittedTrks.vertexCollections.maxDistanceToBeam         = 1
process.offlinePrimaryVerticesFromRefittedTrks.TkFilterParameters.maxNormalizedChi2        = 20
process.offlinePrimaryVerticesFromRefittedTrks.TkFilterParameters.minSiliconLayersWithHits = 5
process.offlinePrimaryVerticesFromRefittedTrks.TkFilterParameters.maxD0Significance        = 5.0 
process.offlinePrimaryVerticesFromRefittedTrks.TkFilterParameters.minPixelLayersWithHits   = 2   


                     
## BeamSpot fit
process.load("RecoVertex.BeamSpotProducer.d0_phi_analyzer_cff")

process.d0_phi_analyzer.BeamFitter.WriteAscii                = True
process.d0_phi_analyzer.BeamFitter.AsciiFileName             = 'BeamFit_LumiBased_NewAlignWorkflow_alcareco.txt'
process.d0_phi_analyzer.BeamFitter.AppendRunToFileName       = False
process.d0_phi_analyzer.BeamFitter.InputBeamWidth            = -1
process.d0_phi_analyzer.BeamFitter.MaximumImpactParameter    = 1.0
process.d0_phi_analyzer.BeamFitter.MaximumNormChi2           = 10
process.d0_phi_analyzer.BeamFitter.MinimumInputTracks        = 50
process.d0_phi_analyzer.BeamFitter.MinimumPixelLayers        = -1
process.d0_phi_analyzer.BeamFitter.MinimumPt                 = 1.0
process.d0_phi_analyzer.BeamFitter.MinimumTotalLayers        = 6
process.d0_phi_analyzer.BeamFitter.OutputFileName            = 'BeamFit_LumiBased_Workflow_alcareco.root' 
process.d0_phi_analyzer.BeamFitter.TrackAlgorithm            = cms.untracked.vstring()
process.d0_phi_analyzer.BeamFitter.TrackCollection           = 'TrackRefitter'
process.d0_phi_analyzer.BeamFitter.SaveFitResults            = False
process.d0_phi_analyzer.BeamFitter.SaveNtuple                = False
process.d0_phi_analyzer.BeamFitter.SavePVVertices            = False
   
process.d0_phi_analyzer.PVFitter.Apply3DFit                  = True
process.d0_phi_analyzer.PVFitter.minNrVerticesForFit         = 10 
process.d0_phi_analyzer.PVFitter.nSigmaCut                   = 50.0
process.d0_phi_analyzer.PVFitter.VertexCollection            = 'offlinePrimaryVerticesFromRefittedTrks' 
   
process.d0_phi_analyzer.BSAnalyzerParameters.fitEveryNLumi   = 1
process.d0_phi_analyzer.BSAnalyzerParameters.resetEveryNLumi = 1


process.p = cms.Path(
    process.offlineBeamSpot                        + 
    process.MeasurementTrackerEvent                + # RIC 23/11/15, needed to fix missing product "Looking for type: MeasurementTrackerEvent"
    process.TrackRefitter                          + 
    process.offlinePrimaryVerticesFromRefittedTrks +
    process.d0_phi_analyzer
)
