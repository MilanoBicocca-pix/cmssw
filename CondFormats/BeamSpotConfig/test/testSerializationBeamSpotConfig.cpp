#include "CondFormats/Serialization/interface/Test.h"

#include "../src/headers.h"

int main()
{
  testSerialization<BeamSpotThresholds>();
  testSerialization<std::vector<BeamSpotThresholds>>();
  testSerialization<std::vector<BeamSpotThresholds::Item>>();
}