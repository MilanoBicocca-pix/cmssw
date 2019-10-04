#include "CondFormats/Serialization/interface/Test.h"

#include "CondFormats/BeamSpotObjects/src/headers.h"

int main() {
  testSerialization<BeamSpotObjects>();
  testSerialization<SimBeamSpotObjects>();
  testSerialization<BeamSpotThresholds>();

  return 0;
}
