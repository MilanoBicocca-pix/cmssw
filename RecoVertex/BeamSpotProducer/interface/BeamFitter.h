#ifndef BeamFitter_H
#define BeamFitter_H

/**_________________________________________________________________
   class:   BeamFitter.h
   package: RecoVertex/BeamSpotProducer

 author: Francisco Yumiceva, Fermilab (yumiceva@fnal.gov)
         Geng-Yuan Jeng, UC Riverside (Geng-Yuan.Jeng@cern.ch)
 ________________________________________________________________**/

#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/Provenance/interface/Timestamp.h"
#include "DataFormats/TrackReco/interface/TrackBase.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/TrackCandidate/interface/TrackCandidate.h"
#include "DataFormats/TrackCandidate/interface/TrackCandidateCollection.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "RecoVertex/BeamSpotProducer/interface/BSTrkParameters.h"
#include "RecoVertex/BeamSpotProducer/interface/BSFitter.h"
#include "RecoVertex/BeamSpotProducer/interface/PVFitter.h"

// ROOT
#include "TFile.h"
#include "TTree.h"
#include "TH1F.h"

#include <fstream>

namespace edm {class ConsumesCollector;}

class BeamFitter 
{
 public:

  typedef std::pair<time_t,time_t>      ptt_TD_   ;
  typedef std::map<int, reco::BeamSpot> iBS_TD_   ;
  typedef std::vector<BSTrkParameters>  vBSTP_TD_ ;
  typedef std::map<int,int>             mii_TD_   ;
  typedef std::pair<int,int>            pii_TD_   ;
  
  	   	  BeamFitter	     (void				      ) {					    }
  	   	  BeamFitter	     (const edm::ParameterSet	    & iConfig, 
	   	  			    edm::ConsumesCollector && iColl   );
  virtual ~	  BeamFitter	     (void				      );

  void     	  readEvent	     (const edm::Event  	    & iEvent  );

  bool     	  runFitter	     (void				      );
  bool     	  runBeamWidthFitter (void				      );
  bool     	  runPVandTrkFitter  (void				      );
  bool     	  runFitterNoTxt     (void				      );

  reco::BeamSpot  getBeamWidth       (void				      ) { return fbeamWidthFit; 		    }
  void  	  runAllFitter       (void				      );
  void  	  resetTrkVector     (void				      ) { fBSvector.clear();			    }
  void  	  resetTotTrk	     (void				      ) { ftotal_tracks   = 0;  		    }
  void  	  resetLSRange       (void				      ) { fbeginLumiOfFit = fendLumiOfFit = -1;     }
  void  	  resetRefTime       (void				      ) { freftime[0]	  = freftime[1]   =  0;     }
  void  	  setRefTime	     (time_t t0, 
                  		      time_t t1)				{
  		  								  freftime[0] = t0;
  		  								  freftime[1] = t1;
  		  								  // Make sure the string representation 
  		  								  // of the time is up-to-date
  		  								  updateBTime();
  		  								}
  ptt_TD_         getRefTime	     (void				      ) {
  		  								  return std::make_pair(
		  											freftime[0], 
		  											freftime[1]
		  										       );
  		  								}  

  void            resetPVFitter      (void				      ) { MyPVFitter->resetAll();		    }

  //---these are added to fasciliate BeamMonitor stuff for DIP
  std::size_t     getPVvectorSize    (void				      ) { return (MyPVFitter->getpvStore()).size(); }
  //sc
  void            resizeBSvector     (unsigned int nsize		      ) {
  		  								  fBSvector.erase(
		  										  fBSvector.begin(),
		  										  fBSvector.begin()+nsize
		  										 );
  		  								}
  //ssc
  void            resizePVvector     (unsigned int npvsize		      ) { 
   		  								  MyPVFitter->resizepvStore(npvsize);
   		  								}
 //ssc
  void            SetPVInfo	     (const std::vector<float> & v1_	      ) {
    		  								  ForDIPPV_.clear();
    		  								  ForDIPPV_.assign( v1_.begin(), v1_.end() );
    		  								}

//-----------------

  void  	  dumpTxtFile	     (std::string &, bool		      );
  void  	  dumpBWTxtFile      (std::string &);
  void  	  write2DB	     (void				      );
  reco::BeamSpot  getBeamSpot	     (void				      ) { return fbeamspot;			    }
  iBS_TD_         getBeamSpotMap     (void				      ) { return fbspotPVMap;			    }
  vBSTP_TD_       getBSvector	     (void				      ) { return fBSvector;			    }
  TH1F          * getCutFlow	     (void				      ) { return h1cutFlow;			    }
  void            subtractFromCutFlow(const TH1F  * toSubtract  	      ) {
  		  								  h1cutFlow->Add(toSubtract, -1.0);
  		  								  for (unsigned int i=0; 
		  								       i<sizeof(countPass)/sizeof(countPass[0]); 
		  								       i++)
		  								  {
  		  								    countPass[i] = h1cutFlow->GetBinContent(i+1);
  		  								  }
  		  								}
  void            resetCutFlow       (void				      ) {
  		  								  h1cutFlow->Reset();
  		  								  ftotal_tracks = 0;
  		  								  for (unsigned int i=0; 
		  								       i<sizeof(countPass)/sizeof(countPass[0]); 
		  								       i++)
		  								  {
  		  								    countPass[i] = 0;
		  								  }
  		  								}

  //ssc
  int             getRunNumber       (void				      ) { return frun;  			    }

  pii_TD_         getFitLSRange      (void				      ) {
  		  								  return std::make_pair(
		  											fbeginLumiOfFit, 
		  											fendLumiOfFit
		  										       );
  		  								}
  void            setFitLSRange      (int ls0,
                  		      int ls1				      ) {
  		  								  fbeginLumiOfFit = ls0;
  		  								  fendLumiOfFit   = ls1;
  		  								}
  void            setRun	     (int run				      ) { frun = run;				    }

  int             getNTracks	     (void				      ) { return fBSvector.size();		    }
  int             getNPVs	     (void				      ) { return MyPVFitter->getNPVs(); 	    }
  const mii_TD_ & getNPVsperBX       (void				      ) { return MyPVFitter->getNPVsperBX();        }

 private:

   typedef edm::EDGetTokenT<reco::TrackCollection>    	EDGTC_TD_ ;
   typedef edm::EDGetTokenT<edm::View<reco::Vertex> > 	EDGRV_TD_ ;
   typedef edm::EDGetTokenT<reco::BeamSpot>           	EDGBS_TD_ ;
   typedef std::vector<std::string>                   	vS_TD_    ;
   typedef std::vector<reco::TrackBase::TrackQuality> 	vTQ_TD_   ;
   typedef std::vector<reco::TrackBase::TrackAlgorithm> vTA_TD_   ;
   typedef std::vector<float>                           vf_TD_    ;
   
   // Update the fbeginTimeOfFit etc from the refTime
   void           updateBTime        (void                                    );

   vBSTP_TD_      fBSvector          ;
   reco::BeamSpot fbeamspot          ;
   reco::BeamSpot fbeamWidthFit      ;
   iBS_TD_        fbspotPVMap        ;
   //  BSFitter * fmyalgo            ;
   std::ofstream  fasciiFile         ;
   std::ofstream  fasciiDIP          ;

   bool 	  debug_;
   bool 	  appendRunTxt_      ;
   bool 	  writeTxt_          ;
   bool 	  writeDIPTxt_       ;
   bool 	  writeDIPBadFit_    ;
   bool 	  isMuon_	     ;
   bool 	  fitted_	     ;
   bool 	  ffilename_changed  ;
   EDGTC_TD_      tracksToken_       ;
   EDGRV_TD_      vertexToken_       ;
   EDGBS_TD_      beamSpotToken_     ; //offlineBeamSpot
   std::string    outputTxt_         ;
   std::string    outputDIPTxt_      ;
   double 	  trk_MinpT_ 	     ;
   double 	  trk_MaxZ_  	     ;
   double 	  trk_MaxEta_	     ;
   double 	  trk_MaxIP_ 	     ;
   double 	  trk_MaxNormChi2_   ;
   double 	  inputBeamWidth_    ;
   double 	  convergence_       ;
   int  	  trk_MinNTotLayers_ ;
   int  	  trk_MinNPixLayers_ ;
   int  	  ftotal_tracks      ;
   int  	  min_Ntrks_         ;
   vS_TD_ 	  trk_Algorithm_     ;
   vS_TD_ 	  trk_Quality_       ;
   vTQ_TD_        quality_           ;
   vTA_TD_        algorithm_         ;
   //ssc
   vf_TD_         ForDIPPV_          ; 
  

   // ntuple
   TH1F         * h1z                ;
   bool 	  saveNtuple_        ;
   bool 	  saveBeamFit_       ;
   bool 	  savePVVertices_    ;
   bool 	  fquality           ;
   bool 	  falgo              ;
   bool 	  fpvValid           ;
   std::string    outputfilename_    ;
   TFile	* file_              ;
   TTree	* ftree_             ;
   double 	  ftheta             ;
   double 	  fpt                ;
   double 	  feta               ;
   double 	  fnormchi2          ;
   double 	  fphi0              ;
   double 	  fd0                ;
   double 	  fd0bs              ;
   double 	  fsigmad0           ;
   double 	  fz0                ;
   double 	  fsigmaz0           ;
   double 	  fcov[7][7]         ;
   double 	  fvx                ;
   double 	  fvy                ;
   double 	  fpvx, fpvy, fpvz   ;
   int            fcharge            ;
   int  	  fnTotLayerMeas     ;
   int  	  fnPixelLayerMeas   ;
   int  	  fnStripLayerMeas   ;
   int  	  fnTIBLayerMeas     ;
   int  	  fnTIDLayerMeas     ;
   int  	  fnTOBLayerMeas     ;
   int  	  fnTECLayerMeas     ;
   int  	  fnPXBLayerMeas     ;
   int  	  fnPXFLayerMeas     ;
   int  	  frun               ;
   int  	  flumi              ;
   std::time_t    freftime[2]        ;

   //beam fit results
   TTree	* ftreeFit_          ;
   int  	  frunFit            ;
   int  	  fbeginLumiOfFit    ;
   int  	  fendLumiOfFit      ;
   int            countPass[9]       ;
   char 	  fbeginTimeOfFit[32];
   char 	  fendTimeOfFit[32]  ;
   double 	  fx                 ;
   double 	  fy                 ;
   double 	  fz                 ;
   double 	  fsigmaZ            ;
   double 	  fdxdz              ;
   double 	  fdydz              ;
   double 	  fxErr              ;
   double 	  fyErr              ;
   double 	  fzErr              ;
   double 	  fsigmaZErr         ;
   double 	  fdxdzErr           ;
   double 	  fdydzErr           ;
   double 	  fwidthX            ;
   double 	  fwidthY            ;
   double 	  fwidthXErr         ;
   double 	  fwidthYErr         ;

   TH1F         * h1ntrks            ;
   TH1F         * h1vz_event         ;
   TH1F         * h1cutFlow          ;

   PVFitter     * MyPVFitter         ;
   TTree        * fPVTree_           ;

};

#endif
