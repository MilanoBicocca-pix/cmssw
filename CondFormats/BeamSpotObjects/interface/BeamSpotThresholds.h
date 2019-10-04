#ifndef CondFormats_BeamSpotObjects_BeamSpotThresholds_h
#define CondFormats_BeamSpotObjects_BeamSpotThresholds_h
/** \class BeamSpotThresholds
 *
 * Class to store the cuts applied to select the Primary Vertices
 * used in the BeamSpot fit (PVFitter module):
 *  - sumPtCut       : cut on the minimum pT of the PV
 *  - nTrksCut       : cut on the minumum number of tracks in the PV
 *  - useFirstPVOnly : whether or not to use only the first PV in the collection
 *  - maxLSinIOV     : maximum number of LS to be merged in a single IOV
 * 
 * This can be used to switch from "Legacy BeamSpot" (computed on ZeroBias until 2017)
 * to "HighPurity BeamSpot" (computed on StreamExpress as default starting from 2018).
 *
 * Legacy Beamspot values:
 *  - sumPtCut       : 0
 *  - nTrksCut       : 0
 *  - useFirstPVOnly : false
 *  - maxLSinIOV     : 60
 *
 * HighPurity Beamspot values:
 *  - sumPtCut       : 50
 *  - nTrksCut       : 30
 *  - useFirstPVOnly : true
 *  - maxLSinIOV     : 20
 *
 *
 *  \Authors: Francesco Brivio (INFN & UNIMIB), Sara Fiorendi (CERN)
 *
 */

#include "CondFormats/Serialization/interface/Serializable.h"

#include <sstream>
#include <cstring>

class BeamSpotThresholds {
public:
  // Default Constructor
  BeamSpotThresholds(): sumPtCut_(50.0), nTrksCut_(30), useFirstPVOnly_(true) {
    maxLSinIOV_ = 20;
  }

  virtual ~BeamSpotThresholds() {}

  /// Setters Methods
  /// set sumPtCut_, minumum pT of the Primary Vertex
  void SetSumPtCut(float val) { sumPtCut_ = val; }

  /// set nTrksCut_, minumum number of tracks in the Primary Vertex
  void SetNTrksCut(int val) { nTrksCut_ = val; }

  /// set maxLSinIOV_, max number of LS to be merged in an IOV
  void SetMaxLSinIOV(int val) { maxLSinIOV_ = val; }

  /// set useFirstPVOnly_, use only the first Primary Vertex of the collection
  void SetUseFirstPVOnly(bool val) { useFirstPVOnly_ = val; }


  /// Getters Methods
  /// get sumPtCut_, minumum pT of the Primary Vertex
  float GetSumPtCut() const { return sumPtCut_; }

  /// get nTrksCut_, minumum number of tracks in the Primary Vertex
  int GetNTrksCut() const { return nTrksCut_; }

  /// get maxLSinIOV_, max number of LS to be merged in an IOV
  int GetMaxLSinIOV() const { return maxLSinIOV_; }

  /// get useFirstPVOnly_, use only the first Primary Vertex of the collection
  bool GetUseFirstPVOnly() const { return useFirstPVOnly_; }


  /// Print Beam Spot thresholds
  void print(std::stringstream& ss) const;


private:
  float sumPtCut_;
  int   nTrksCut_;
  int   maxLSinIOV_;
  bool  useFirstPVOnly_;

  COND_SERIALIZABLE;
};

std::ostream& operator<<(std::ostream&, BeamSpotThresholds beam);

#endif
