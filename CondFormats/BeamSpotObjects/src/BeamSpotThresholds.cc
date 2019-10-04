#include "CondFormats/BeamSpotObjects/interface/BeamSpotThresholds.h"

#include <iostream>

void BeamSpotThresholds::print(std::stringstream& ss) const {
  ss << "-----------------------------------------------------\n"
     << "              Beam Spot Thresholds\n\n"
     << " Minimum pT               = " << GetSumPtCut() << "\n"
     << " Minimum number of tracks = " << GetNTrksCut() << "\n"
     << " Using only the first PV  = " << GetUseFirstPVOnly() << "\n"
     << " Max LS merged in one IOV = " << GetMaxLSinIOV() << "\n"
     << "-----------------------------------------------------\n\n";
}

std::ostream& operator<<(std::ostream& os, BeamSpotThresholds beam) {
  std::stringstream ss;
  beam.print(ss);
  os << ss.str();
  return os;
}
