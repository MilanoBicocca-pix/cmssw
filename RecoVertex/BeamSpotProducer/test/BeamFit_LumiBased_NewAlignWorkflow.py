import FWCore.ParameterSet.Config as cms

process = cms.Process("BSworkflow")

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
      "/store/express/Run2015A/StreamExpress/ALCARECO/TkAlMinBias-Express-v1/000/246/959/00000/14174DF2-490A-E511-9862-02163E0143E9.root",
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

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag as customiseGlobalTag
process.GlobalTag = customiseGlobalTag(process.GlobalTag, globaltag = 'GR_E_V48') # express
process.GlobalTag.connect   = 'frontier://FrontierProd/CMS_CONDITIONS'
process.GlobalTag.pfnPrefix = cms.untracked.string('frontier://FrontierProd/')
for pset in process.GlobalTag.toGet.value():
    pset.connect = pset.connect.value().replace('frontier://FrontierProd/', 'frontier://FrontierProd/')
# fix for multi-run processing
process.GlobalTag.RefreshEachRun = cms.untracked.bool( False )
process.GlobalTag.ReconnectEachRun = cms.untracked.bool( False )


## Track refit
process.load("RecoTracker.TrackProducer.TrackRefitters_cff")
process.load('RecoTracker.MeasurementDet.MeasurementTrackerEventProducer_cfi')

# remove the following lines if you run on RECO files
process.MeasurementTrackerEvent.stripClusterProducer = 'ALCARECOTkAlMinBias'
process.MeasurementTrackerEvent.pixelClusterProducer = 'ALCARECOTkAlMinBias'
process.MeasurementTrackerEvent.inactivePixelDetectorLabels = cms.VInputTag()
process.MeasurementTrackerEvent.inactiveStripDetectorLabels = cms.VInputTag() 
process.TrackRefitter.src = 'ALCARECOTkAlMinBias'


## PV refit
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")

from RecoVertex.PrimaryVertexProducer.OfflinePrimaryVertices_cfi import offlinePrimaryVertices 
process.offlinePrimaryVerticesFromRefittedTrks  = offlinePrimaryVertices.clone()
process.offlinePrimaryVerticesFromRefittedTrks.TrackLabel                                       = cms.InputTag("TrackRefitter") 
process.offlinePrimaryVerticesFromRefittedTrks.vertexCollections.maxDistanceToBeam              = 2
process.offlinePrimaryVerticesFromRefittedTrks.TkFilterParameters.maxNormalizedChi2             = 20
process.offlinePrimaryVerticesFromRefittedTrks.TkFilterParameters.minSiliconLayersWithHits      = 5
process.offlinePrimaryVerticesFromRefittedTrks.TkFilterParameters.maxD0Significance             = 5.0 # _sara: changed, was 100
process.offlinePrimaryVerticesFromRefittedTrks.TkFilterParameters.minPixelLayersWithHits        = 2   # _sara: changed, was 1


                     
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
process.d0_phi_analyzer.BeamFitter.SaveFitResults            = True
process.d0_phi_analyzer.BeamFitter.SaveNtuple                = True
process.d0_phi_analyzer.BeamFitter.SavePVVertices            = True
   
process.d0_phi_analyzer.PVFitter.Apply3DFit                  = True
process.d0_phi_analyzer.PVFitter.minNrVerticesForFit         = 10 
process.d0_phi_analyzer.PVFitter.nSigmaCut                   = 50.0
process.d0_phi_analyzer.PVFitter.VertexCollection            = 'offlinePrimaryVerticesFromRefittedTrks' 
   
process.d0_phi_analyzer.BSAnalyzerParameters.fitEveryNLumi   = 1
process.d0_phi_analyzer.BSAnalyzerParameters.resetEveryNLumi = 1


process.p = cms.Path(process.offlineBeamSpot                        + 
                     process.MeasurementTrackerEvent                + 
                     process.TrackRefitter                          + 
                     process.offlinePrimaryVerticesFromRefittedTrks +
                     process.d0_phi_analyzer)
