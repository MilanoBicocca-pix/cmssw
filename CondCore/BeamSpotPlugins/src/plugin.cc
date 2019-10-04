#include "CondCore/ESSources/interface/registration_macros.h"
#include "CondFormats/DataRecord/interface/BeamSpotObjectsRcd.h"
#include "CondFormats/DataRecord/interface/SimBeamSpotObjectsRcd.h"
#include "CondFormats/DataRecord/interface/BeamSpotThresholdsRcd.h"
#include "CondFormats/BeamSpotObjects/interface/BeamSpotObjects.h"
#include "CondFormats/BeamSpotObjects/interface/SimBeamSpotObjects.h"
#include "CondFormats/BeamSpotObjects/interface/BeamSpotThresholds.h"

REGISTER_PLUGIN(BeamSpotObjectsRcd, BeamSpotObjects);
REGISTER_PLUGIN(SimBeamSpotObjectsRcd, SimBeamSpotObjects);
REGISTER_PLUGIN(BeamSpotThresholdsRcd, BeamSpotThresholds);
