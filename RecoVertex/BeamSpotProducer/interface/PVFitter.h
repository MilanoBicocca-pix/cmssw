#ifndef PVFitter_H
#define PVFitter_H

/**_________________________________________________________________
   class:   PVFitter.h
   package: RecoVertex/BeamSpotProducer
   


 author: Francisco Yumiceva, Fermilab (yumiceva@fnal.gov)
         Geng-Yuan Jeng, UC Riverside (Geng-Yuan.Jeng@cern.ch)
 

 ________________________________________________________________**/

#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Provenance/interface/Timestamp.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/TrackReco/interface/TrackBase.h"
#include "RecoVertex/BeamSpotProducer/interface/BSTrkParameters.h"
#include "RecoVertex/BeamSpotProducer/interface/BSFitter.h"

#include "RecoVertex/BeamSpotProducer/interface/BeamSpotTreeData.h"
#include "RecoVertex/BeamSpotProducer/interface/BeamSpotFitPVData.h"

#include "DataFormats/VertexReco/interface/VertexFwd.h"


// ROOT
#include "TFile.h"
#include "TTree.h"
#include "TH2F.h"

#include <fstream>

namespace edm {class ConsumesCollector;}

namespace reco 
{
  class Vertex;
}

class PVFitter 
{
 public:
 
  typedef                std::vector<BeamSpotFitPVData>   PVData_TD_   ;
  typedef std::map< int, std::vector<BeamSpotFitPVData> > i_PVData_TD_ ;
  typedef                reco::BeamSpot                   BS_TD_       ;
  typedef std::map<int,  BS_TD_ >  	   	          BS_i_TD_     ;
  typedef std::map<int,  int>             	   	  mii_TD_      ;
  
  	     PVFitter	   	  (void 				   ) {  				 }
  	     PVFitter	   	  (const edm::ParameterSet	&  iConfig,				    
  	     		   	  	 edm::ConsumesCollector && iColl   );
  	     PVFitter	   	  (const edm::ParameterSet	&  iConfig, 
  	     		   	  	 edm::ConsumesCollector &  iColl   );
  virtual   ~PVFitter      	  (void 				   );

  void       initialize    	  (const edm::ParameterSet	& iConfig, 
             			  	 edm::ConsumesCollector & iColl    );
  void       readEvent     	  (const edm::Event		& iEvent   );
  void       setTree	   	  (	 TTree  		* tree     );
  
  double     getWidthX     	  (void 				   ) { return fwidthX;  		 }
  double     getWidthY     	  (void 				   ) { return fwidthY;  		 }
  double     getWidthZ     	  (void 				   ) { return fwidthZ;  		 }
  double     getWidthXerr  	  (void 				   ) { return fwidthXerr;		 }
  double     getWidthYerr  	  (void 				   ) { return fwidthYerr;		 }
  double     getWidthZerr  	  (void 				   ) { return fwidthZerr;		 }
  //ssc 			  									    
  PVData_TD_ getpvStore     	  (void 				   ) { return pvStore_; 		 }
 				  									    
  void       FitPerBunchCrossing  (void 				   ) { fFitPerBunchCrossing = true;	 }
  bool       runBXFitter	  (void 				   );
  bool       runFitter   	  (void 				   );
  void       resetLSRange	  (void 				   ) { fbeginLumiOfFit=fendLumiOfFit=-1; }
  void       resetRefTime	  (void 				   ) { freftime[0] = freftime[1] = 0;	 }
  //ssc
   void      setRefTime           (std::time_t t0,
                                   std::time_t t1			   ) {
  				  					       freftime[0] = t0;
  				  					       freftime[1] = t1;
  				  					     }
   void      setFitLSRange        (int ls0,
                                   int ls1				   ) {
  				  					       fbeginLumiOfFit = ls0; 
  				  					       fendLumiOfFit   = ls1;	
  				  					     }  		      

  void       dumpTxtFile          (void 				   );
  void       resetAll             (void 				   ) {
  				  					       dynamicQualityCut_ = 1.e30  ;
  				  					       resetLSRange   ()	   ;
  				  					       resetRefTime   ()	   ;
  				  					       pvStore_.clear ()	   ;
  				  					       bxMap_.clear   ()	   ;
  				  					       hPVx->Reset    ()	   ;
  				  					       hPVy->Reset    ()	   ;
  				  					       fbeamspot = reco::BeamSpot();
  				  					       fbspotMap.clear()           ;
  				  					     };
  BS_TD_     getBeamSpot          (void 				   ) { return fbeamspot 	  ;	 }
  BS_i_TD_   getBeamSpotMap       (void 				   ) { return fbspotMap 	  ;	 }
  bool       IsFitPerBunchCrossing(void                                    ) { return fFitPerBunchCrossing;      }
  int      * getFitLSRange        (void                                    ) {
  									       int *tmp = new int[2]     ;
  									       tmp[0]   = fbeginLumiOfFit;
  									       tmp[1]   = fendLumiOfFit  ;
  									       return tmp;
  									     }
  //ssc
  time_t   * getRefTime           (void                                    ) {
 									      time_t *tmptime = new time_t[2];
 									      tmptime[0]      = freftime[0]  ;
 									      tmptime[1]      = freftime[1]  ;
 									      return tmptime;
 									     }

  //ssc
  void       resizepvStore        (unsigned int rmSize                     ){
                                                                             pvStore_.erase(pvStore_.begin(), 
									                    pvStore_.begin()+rmSize);
                                                                            }

 
  /// reduce size of primary vertex cache by increasing quality limit
  void       compressStore        (void                                    );
  /// vertex quality measure
  double     pvQuality            (const reco::Vertex      & pv            ) const;
  /// vertex quality measure
  double     pvQuality            (const BeamSpotFitPVData & pv            ) const;
  int        getNPVs              (void                                    ) { return pvStore_.size();          }
  
  const mii_TD_ & getNPVsperBX    (void                                    ) {
  									       npvsmap_.clear();
  									       for ( std::map<int,std::vector<BeamSpotFitPVData> >::const_iterator   pvStore = bxMap_.begin();                                  
                                                                                                                                                     pvStore!= bxMap_.end(); 
																		   ++pvStore) 
                                                                               {
  									     	 //std::cout << "bx " << pvStore->first << " NPVs = " << (pvStore->second).size() << std::endl;
  									     	 npvsmap_[ pvStore->first ] = (pvStore->second).size();

  									       }
  									       return npvsmap_;
  									     }
 //--------------------------------------------------------------------------
 private:

  typedef edm::EDGetTokenT<reco::VertexCollection> 	  VC_TD_       ;

  mii_TD_         npvsmap_ 	      ;
  BS_TD_          fbeamspot	      ;
  BS_i_TD_        fbspotMap	      ;
  bool            fFitPerBunchCrossing;

  std::ofstream   fasciiFile;

  bool  	  debug_      	      ;
  bool  	  do3DFit_    	      ;
  VC_TD_          vertexToken_	      ;
  // bool         writeTxt_   	      ;
  std::string     outputTxt_  	      ;

  unsigned int    maxNrVertices_      ;
  unsigned int    minNrVertices_      ;
  double          minVtxNdf_          ;
  double          maxVtxNormChi2_     ;
  unsigned int    minVtxTracks_       ;
  double          minVtxWgt_          ;
  double          maxVtxR_            ;
  double          maxVtxZ_            ;
  double          errorScale_         ;
  double          sigmaCut_           ;
  
  //  int    	  frun       	      ;
  //  int    	  flumi      	      ;
  std::time_t	  freftime[2]	      ;

  TH2F  	* hPVx		      ;
  TH2F  	* hPVy		      ;

  TTree         * ftree_              ;
  //bool 	  saveNtuple_ 	      ;
  //bool 	  saveBeamFit_	      ;
  //std::string   outputfilename_     ;
  //TFile	* file_ 	      ;
  //TTree	* ftree_	      ;

  //beam  	  fit results         ;
  //TTree 	* ftreeFit_	      ;
  //  int 	  frunFit  	      ;
  int 		  fbeginLumiOfFit     ;
  int 		  fendLumiOfFit       ;
  //  char 	  fbeginTimeOfFit[32] ;
  //  char 	  fendTimeOfFit[32]   ;
  double	  fwidthX   	      ;
  double	  fwidthY   	      ;
  double	  fwidthZ   	      ;
  double	  fwidthXerr	      ;
  double	  fwidthYerr	      ;
  double	  fwidthZerr	      ;
  
  /*  double      fx	    	      ;
  double 	  fy	    	      ;
  double 	  fz	    	      ;
  double 	  fsigmaZ   	      ;
  double 	  fdxdz     	      ;
  double 	  fdydz     	      ;
  double 	  fxErr     	      ;
  double 	  fyErr     	      ;
  double 	  fzErr     	      ;
  double 	  fsigmaZErr	      ;
  double 	  fdxdzErr  	      ;
  double 	  fdydzErr  	      ;
  */

  PVData_TD_          pvStore_            ; //< cache for PV data
  i_PVData_TD_        bxMap_              ; // store PV data as a function of bunch crossings
  double              dynamicQualityCut_  ; //< quality cut for vertices (dynamic adjustment)
  std::vector<double> pvQualities_        ; //< working space for PV store adjustement
  BeamSpotTreeData    theBeamSpotTreeData_;
};

#endif
