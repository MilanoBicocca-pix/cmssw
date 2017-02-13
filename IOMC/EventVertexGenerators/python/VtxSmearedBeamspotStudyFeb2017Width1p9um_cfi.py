import FWCore.ParameterSet.Config as cms

from IOMC.EventVertexGenerators.VtxSmearedParameters_cfi import *
VtxSmeared = cms.EDProducer("BetafuncEvtVtxGenerator",
    BeamspotStudyFeb2017Width1p9umVtxSmearingParameters,
    VtxSmearedCommon
)
