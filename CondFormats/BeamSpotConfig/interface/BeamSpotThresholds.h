#ifndef CondFormats_BeamSpotConfig_BeamSpotThresholds_h
#define CondFormats_BeamSpotConfig_BeamSpotThresholds_h

#include "CondFormats/Serialization/interface/Serializable.h"
#include <vector>

class BeamSpotThresholds {
    public:
      struct Item {
       float m_sumPtCut;
       int   m_nTrksCut;
       int   m_maxLSinIOV;
       bool  m_useFirstVtx;
       COND_SERIALIZABLE;
      };

    std::vector<Item>  m_beamSpotConfigurables;



    COND_SERIALIZABLE;

};

#endif