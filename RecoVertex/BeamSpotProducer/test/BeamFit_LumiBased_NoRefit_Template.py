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
process.d0_phi_analyzer.BeamFitter.TrackCollection           = 'generalTracks'#'generalTracks'#ALCARECOTkAlMinBias
process.d0_phi_analyzer.BeamFitter.SaveFitResults            = False
process.d0_phi_analyzer.BeamFitter.SaveNtuple                = False
process.d0_phi_analyzer.BeamFitter.SavePVVertices            = False
process.d0_phi_analyzer.BeamFitter.timerange                 = cms.untracked.vdouble(min_time_t,max_time_t)
process.d0_phi_analyzer.BeamFitter.selectBx                  = theBx
'''
{{ <row>L1_ZeroBias_copy,  265, 1</row>}}
{{ <row>L1_ZeroBias_copy,  865, 1</row>}}
{{ <row>L1_ZeroBias_copy, 1780, 1</row>}}
{{ <row>L1_ZeroBias_copy, 2192, 1</row>}}
{{ <row>L1_ZeroBias_copy, 3380, 1</row>}}
'''
   
process.d0_phi_analyzer.PVFitter.maxNrStoredVertices         = 200000
   
process.d0_phi_analyzer.PVFitter.Apply3DFit                  = True
process.d0_phi_analyzer.PVFitter.minNrVerticesForFit         = 10 
process.d0_phi_analyzer.PVFitter.nSigmaCut                   = 50.0
process.d0_phi_analyzer.PVFitter.VertexCollection            = 'offlinePrimaryVertices' 

process.d0_phi_analyzer.PVFitter.errorScale                  = 0.9 
# process.d0_phi_analyzer.PVFitter.useOnlyFirstPV              = cms.untracked.bool(True)
# process.d0_phi_analyzer.PVFitter.minSumPt                    = cms.untracked.double(50.)
# process.d0_phi_analyzer.PVFitter.minVertexNTracks            = cms.untracked.uint32(30)
   
process.d0_phi_analyzer.BSAnalyzerParameters.fitEveryNLumi   = -1
process.d0_phi_analyzer.BSAnalyzerParameters.resetEveryNLumi = -1


process.p = cms.Path(process.d0_phi_analyzer)
