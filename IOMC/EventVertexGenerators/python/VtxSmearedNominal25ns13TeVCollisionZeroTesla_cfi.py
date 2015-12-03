import FWCore.ParameterSet.Config as cms

from IOMC.EventVertexGenerators.VtxSmearedParameters_cfi import *
VtxSmeared = cms.EDProducer("BetafuncEvtVtxGenerator",
    Nominal25ns13TeVCollisionZeroTeslaVtxSmearingParameters,
    VtxSmearedCommon
)

