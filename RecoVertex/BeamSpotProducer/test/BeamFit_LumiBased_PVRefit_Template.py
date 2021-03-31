import FWCore.ParameterSet.Config as cms

process = cms.Process("BSworkflow")

from filelist_template import file_list
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
      file_list
    ),
    skipBadFiles = cms.untracked.bool(True),
    lumisToProcess = cms.untracked.VLuminosityBlockRange('thelumirange')
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
process.load("Configuration.StandardSequences.MagneticField_cff") 
process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff") 
# this GT should be customized with the one used in the ReReco
# that you are analyzing
process.GlobalTag.globaltag = '106X_dataRun2_v20'  # VdM 2017
#process.GlobalTag.globaltag = '106X_dataRun2_v28' # VdM 2018

## PV refit
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
from RecoVertex.PrimaryVertexProducer.OfflinePrimaryVertices_cfi import offlinePrimaryVertices 
process.offlinePrimaryVerticesFromRefittedTrks  = offlinePrimaryVertices.clone()
process.offlinePrimaryVerticesFromRefittedTrks.TrackLabel                                  = cms.InputTag("generalTracks") # generalTracks or ALCARECOTkAlMinBias
process.offlinePrimaryVerticesFromRefittedTrks.vertexCollections.maxDistanceToBeam         = 1
process.offlinePrimaryVerticesFromRefittedTrks.TkFilterParameters.maxNormalizedChi2        = 20
process.offlinePrimaryVerticesFromRefittedTrks.TkFilterParameters.minSiliconLayersWithHits = 5
process.offlinePrimaryVerticesFromRefittedTrks.TkFilterParameters.maxD0Significance        = 5.0 
process.offlinePrimaryVerticesFromRefittedTrks.TkFilterParameters.minPixelLayersWithHits   = 2   

# Vertexing a' la' 80X
process.offlinePrimaryVerticesFromRefittedTrks.TkClusParameters.d0CutOff                           = cms.double(3.)
process.offlinePrimaryVerticesFromRefittedTrks.TkClusParameters.TkDAClusParameters.dzCutOff        = cms.double(4.0)
process.offlinePrimaryVerticesFromRefittedTrks.TkClusParameters.TkDAClusParameters.vertexSize      = cms.double(0.01)
process.offlinePrimaryVerticesFromRefittedTrks.TkClusParameters.TkDAClusParameters.uniquetrkweight = cms.double(0.9)
process.offlinePrimaryVerticesFromRefittedTrks.TkClusParameters.TkDAClusParameters.Tpurge          = cms.double(2.4)
process.offlinePrimaryVerticesFromRefittedTrks.TkClusParameters.TkDAClusParameters.Tstop           = cms.double(1.0)
process.offlinePrimaryVerticesFromRefittedTrks.TkClusParameters.TkDAClusParameters.zmerge          = cms.double(0.02)
process.offlinePrimaryVerticesFromRefittedTrks.TkFilterParameters.maxEta                           = 10.0
process.offlinePrimaryVerticesFromRefittedTrks.vertexCollections[0].chi2cutoff                     = 3.0
process.offlinePrimaryVerticesFromRefittedTrks.vertexCollections[1].chi2cutoff                     = 3.0


## BeamSpot fit
process.load("RecoVertex.BeamSpotProducer.d0_phi_analyzer_cff")

process.d0_phi_analyzer.BeamFitter.WriteAscii                = True
process.d0_phi_analyzer.BeamFitter.AsciiFileName             = 'BeamFit_LumiBased_alcareco_template.txt'
process.d0_phi_analyzer.BeamFitter.AppendRunToFileName       = True
process.d0_phi_analyzer.BeamFitter.InputBeamWidth            = -1
process.d0_phi_analyzer.BeamFitter.MaximumImpactParameter    = 1.0
process.d0_phi_analyzer.BeamFitter.MaximumNormChi2           = 10
process.d0_phi_analyzer.BeamFitter.MinimumInputTracks        = 50
process.d0_phi_analyzer.BeamFitter.MinimumPixelLayers        = -1
process.d0_phi_analyzer.BeamFitter.MinimumPt                 = 1.0
process.d0_phi_analyzer.BeamFitter.MinimumTotalLayers        = 6
process.d0_phi_analyzer.BeamFitter.OutputFileName            = 'BeamFit_LumiBased_Workflow_alcareco.root' 
process.d0_phi_analyzer.BeamFitter.TrackAlgorithm            = cms.untracked.vstring()
process.d0_phi_analyzer.BeamFitter.TrackCollection           = 'generalTracks' # generalTracks or ALCARECOTkAlMinBias
process.d0_phi_analyzer.BeamFitter.SaveFitResults            = False
process.d0_phi_analyzer.BeamFitter.SaveNtuple                = False
process.d0_phi_analyzer.BeamFitter.SavePVVertices            = False
process.d0_phi_analyzer.BeamFitter.timerange                 = cms.untracked.vdouble(min_time_t,max_time_t)
process.d0_phi_analyzer.BeamFitter.selectBx                  = cms.untracked.vint32(theBx)
   
process.d0_phi_analyzer.PVFitter.maxNrStoredVertices         = 200000   
process.d0_phi_analyzer.PVFitter.Apply3DFit                  = True
process.d0_phi_analyzer.PVFitter.minNrVerticesForFit         = 10 
process.d0_phi_analyzer.PVFitter.nSigmaCut                   = 50.0
process.d0_phi_analyzer.PVFitter.VertexCollection            = 'offlinePrimaryVerticesFromRefittedTrks'

process.d0_phi_analyzer.PVFitter.errorScale                  = 0.95 # VdM 2017
#process.d0_phi_analyzer.PVFitter.errorScale                 = 1.0  # VdM 2018

# Uncomment these parameters if you want to run the HP workflow
# process.d0_phi_analyzer.PVFitter.useOnlyFirstPV              = cms.untracked.bool(True)
# process.d0_phi_analyzer.PVFitter.minSumPt                    = cms.untracked.double(50.)
# process.d0_phi_analyzer.PVFitter.minVertexNTracks            = cms.untracked.uint32(30)
   
process.d0_phi_analyzer.BSAnalyzerParameters.fitEveryNLumi   = -1
process.d0_phi_analyzer.BSAnalyzerParameters.resetEveryNLumi = -1

process.options.numberOfThreads = cms.untracked.uint32(4)
process.options.numberOfStreams = cms.untracked.uint32(4)

process.p = cms.Path(process.offlinePrimaryVerticesFromRefittedTrks +
                     process.d0_phi_analyzer)
