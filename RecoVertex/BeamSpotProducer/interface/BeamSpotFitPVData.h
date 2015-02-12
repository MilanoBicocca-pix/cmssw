#ifndef BeamSpotFitPVData_
#define BeamSpotFitPVData_
/** \class BeamSpotFitPVData
 *  Simple structure to hold vertex position and covariance.
 *  \author WA, 9/3/2010
 */

#include <TROOT.h>

struct BeamSpotFitPVData 
{
  Float_t bunchCrossing; // bunch crossing
  Float_t position[3]  ; //< x, y, z position
  Float_t posError[3]  ; //< x, y, z error
  Float_t posCorr[3]   ; //< xy, xz, yz correlations
};
#endif
