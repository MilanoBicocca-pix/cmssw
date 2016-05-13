/**_________________________________________________________________
   class:   PVFitter.cc
   package: RecoVertex/BeamSpotProducer



   author: Francisco Yumiceva, Fermilab (yumiceva@fnal.gov)
           Geng-Yuan Jeng, UC Riverside (Geng-Yuan.Jeng@cern.ch)


________________________________________________________________**/

#include "RecoVertex/BeamSpotProducer/interface/PVFitter.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CondCore/DBOutputService/interface/PoolDBOutputService.h"
#include "CondFormats/BeamSpotObjects/interface/BeamSpotObjects.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/View.h"

#include "DataFormats/TrackCandidate/interface/TrackCandidate.h"
#include "DataFormats/TrackCandidate/interface/TrackCandidateCollection.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/TrackReco/interface/HitPattern.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include "RecoVertex/BeamSpotProducer/interface/FcnBeamSpotFitPV.h"
#include "FWCore/Utilities/interface/isFinite.h"

#include "TF1.h"
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#include "RecoVertex/BeamSpotProducer/interface/BeamSpotUtils.h"

#include <iostream>    // Dario
#include <iomanip>     // Dario
using namespace std ;  // Dario
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// ----------------------------------------------------------------------
// Useful function:
// ----------------------------------------------------------------------

// static char * formatTime(const std::time_t & t)  {
//   struct std::tm * ptm;
//   ptm = gmtime(&t);
//   static char ts[32];
//   strftime(ts,sizeof(ts),"%Y.%m.%d %H:%M:%S %Z",ptm);
//   return ts;
// }
PVFitter::PVFitter(const edm::ParameterSet& iConfig,
                   edm::ConsumesCollector &&iColl)
  : ftree_(0)
{
  initialize(iConfig, iColl);
}

PVFitter::PVFitter(const edm::ParameterSet& iConfig,
                   edm::ConsumesCollector &iColl)
    :ftree_(0)
{
  initialize(iConfig, iColl);
}

void PVFitter::initialize(const edm::ParameterSet& iConfig,
                          edm::ConsumesCollector &iColl)
{
  debug_             = iConfig.getParameter<edm::ParameterSet>("PVFitter").getUntrackedParameter<bool>("Debug");
  vertexToken_       = iColl.consumes<reco::VertexCollection>(
      iConfig.getParameter<edm::ParameterSet>("PVFitter")
      .getUntrackedParameter<edm::InputTag>("VertexCollection",
                                            edm::InputTag("offlinePrimaryVertices")));
  do3DFit_           = iConfig.getParameter<edm::ParameterSet>("PVFitter").getUntrackedParameter<bool>("Apply3DFit");
  //writeTxt_          = iConfig.getParameter<edm::ParameterSet>("PVFitter").getUntrackedParameter<bool>("WriteAscii");
  //outputTxt_         = iConfig.getParameter<edm::ParameterSet>("PVFitter").getUntrackedParameter<std::string>("AsciiFileName");

  maxNrVertices_     = iConfig.getParameter<edm::ParameterSet>("PVFitter").getUntrackedParameter<unsigned int>("maxNrStoredVertices");
  minNrVertices_     = iConfig.getParameter<edm::ParameterSet>("PVFitter").getUntrackedParameter<unsigned int>("minNrVerticesForFit");
  minVtxNdf_         = iConfig.getParameter<edm::ParameterSet>("PVFitter").getUntrackedParameter<double>("minVertexNdf");
  maxVtxNormChi2_    = iConfig.getParameter<edm::ParameterSet>("PVFitter").getUntrackedParameter<double>("maxVertexNormChi2");
  minVtxTracks_      = iConfig.getParameter<edm::ParameterSet>("PVFitter").getUntrackedParameter<unsigned int>("minVertexNTracks");
  minVtxWgt_         = iConfig.getParameter<edm::ParameterSet>("PVFitter").getUntrackedParameter<double>("minVertexMeanWeight");
  maxVtxR_           = iConfig.getParameter<edm::ParameterSet>("PVFitter").getUntrackedParameter<double>("maxVertexR");
  maxVtxZ_           = iConfig.getParameter<edm::ParameterSet>("PVFitter").getUntrackedParameter<double>("maxVertexZ");
  errorScale_        = iConfig.getParameter<edm::ParameterSet>("PVFitter").getUntrackedParameter<double>("errorScale");
  sigmaCut_          = iConfig.getParameter<edm::ParameterSet>("PVFitter").getUntrackedParameter<double>("nSigmaCut");
  fFitPerBunchCrossing=iConfig.getParameter<edm::ParameterSet>("PVFitter").getUntrackedParameter<bool>("FitPerBunchCrossing");

  // preset quality cut to "infinite"
  dynamicQualityCut_ = 1.e30;

  hPVx = new TH2F("hPVx","PVx vs PVz distribution",200,-maxVtxR_, maxVtxR_, 200, -maxVtxZ_, maxVtxZ_);
  hPVy = new TH2F("hPVy","PVy vs PVz distribution",200,-maxVtxR_, maxVtxR_, 200, -maxVtxZ_, maxVtxZ_);
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//   positionH_   .push_back(new TH1F("positionX","X of vertices" ,500, -1.  , 1.  )) ;
//   positionH_   .push_back(new TH1F("positionY","Y of vertices" ,500, -1.  , 1.  )) ;
//   positionH_   .push_back(new TH1F("positionZ","Z of vertices" ,500,-50.  ,50.  )) ;
//   errorH_      .push_back(new TH1F("errorX"   ,"X error"       ,500,  0.  ,  .1 )) ;
//   errorH_      .push_back(new TH1F("errorY"   ,"Y error"       ,500,  0.  ,  .1 )) ;
//   errorH_      .push_back(new TH1F("errorZ"   ,"Z error"       ,500,  0.  , 1.  )) ;
//   correlationH_.push_back(new TH1F("correlXY" ,"XY correlation",500,  0.  , 1.  )) ;
//   correlationH_.push_back(new TH1F("correlXZ" ,"XZ correlation",500,  0.  , 1.  )) ;
//   correlationH_.push_back(new TH1F("correlYZ" ,"YZ correlation",500,  0.  , 1.  )) ;
//   spacePosXY_  = 	  new TH2F("XvsY"     ,"X versus Y"    ,500,  0.02, 0.11
//                  	  				       ,500,  0.03, 0.15)  ;
//   spacePosXZ_  = 	  new TH2F("XvsZ"     ,"X versus Z"    ,500,  0.02, 0.11
//                  	  				       ,500,-12.0 ,12.0 )  ;
//   spacePosYZ_  = 	  new TH2F("YvsZ"     ,"Y versus Z"    ,500,  0.03, 0.15
//                  	  				       ,500,-12.0 ,12.0 )  ; 
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
}

PVFitter::~PVFitter() {
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  CO("Eccchecazzo!","") ;
//  TFile fout("temp.root","recreate") ;
//  positionH_   [0]->Write() ;
//  positionH_   [1]->Write() ;
//  positionH_   [2]->Write() ;
//  errorH_      [0]->Write() ;
//  errorH_      [1]->Write() ;
//  errorH_      [2]->Write() ;
//  correlationH_[0]->Write() ;
//  correlationH_[1]->Write() ;
//  correlationH_[2]->Write() ;
//  spacePosXY_	 ->Write() ;
//  spacePosXZ_	 ->Write() ;
//  spacePosYZ_ 	 ->Write() ;
//  fout.Close() ;
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
}


void PVFitter::readEvent(const edm::Event& iEvent)
{

//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  hPVx->Reset();
  hPVy->Reset();
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//   frun = iEvent.id().run();
//   const edm::TimeValue_t ftimestamp = iEvent.time().value();
//   const std::time_t ftmptime = ftimestamp >> 32;

//   if (fbeginLumiOfFit == -1) freftime[0] = freftime[1] = ftmptime;
//   if (freftime[0] == 0 || ftmptime < freftime[0]) freftime[0] = ftmptime;
//   const char* fbeginTime = formatTime(freftime[0]);
//   sprintf(fbeginTimeOfFit,"%s",fbeginTime);

//   if (freftime[1] == 0 || ftmptime > freftime[1]) freftime[1] = ftmptime;
//   const char* fendTime = formatTime(freftime[1]);
//   sprintf(fendTimeOfFit,"%s",fendTime);

//   flumi = iEvent.luminosityBlock();
//   frunFit = frun;

//   if (fbeginLumiOfFit == -1 || fbeginLumiOfFit > flumi) fbeginLumiOfFit = flumi;
//   if (fendLumiOfFit == -1 || fendLumiOfFit < flumi) fendLumiOfFit = flumi;
//   std::cout << "flumi = " <<flumi<<"; fbeginLumiOfFit = " << fbeginLumiOfFit <<"; fendLumiOfFit = "<<fendLumiOfFit<<std::endl;

  //------ Primary Vertices
  edm::Handle< reco::VertexCollection > PVCollection;
  bool hasPVs = false;
  //edm::View<reco::Vertex> vertices;
  //const reco::VertexCollection & vertices = 0;

  if ( iEvent.getByToken(vertexToken_, PVCollection ) ) {
      //pv = *PVCollection;
      //vertices = *PVCollection;
      hasPVs = true;
  }
  //------

  if ( hasPVs ) {

      for (reco::VertexCollection::const_iterator pv = PVCollection->begin(); pv != PVCollection->end(); ++pv ) {


           //for ( size_t ipv=0; ipv != pv.size(); ++ipv ) {

          //--- vertex selection
          if ( pv->isFake() || pv->tracksSize()==0 )  continue;
          if ( pv->ndof() < minVtxNdf_ || (pv->ndof()+3.)/pv->tracksSize()<2*minVtxWgt_ )  continue;
          //---

          hPVx->Fill( pv->x(), pv->z() );
          hPVy->Fill( pv->y(), pv->z() );

          //
          // 3D fit section
          //
          // apply additional quality cut
          if ( pvQuality(*pv)>dynamicQualityCut_ )  continue;
          // if store exceeds max. size: reduce size and apply new quality cut
          if ( pvStore_.size()>=maxNrVertices_ ) {
             compressStore();
             if ( pvQuality(*pv)>dynamicQualityCut_ )  continue;
          }
          //
          // copy PV to store
          //
	  int bx = iEvent.bunchCrossing();
          BeamSpotFitPVData pvData;
	  pvData.bunchCrossing = bx;
          pvData.position[0] = pv->x();
          pvData.position[1] = pv->y();
          pvData.position[2] = pv->z();
          pvData.posError[0] = pv->xError();
          pvData.posError[1] = pv->yError();
          pvData.posError[2] = pv->zError();
          pvData.posCorr[0] = pv->covariance(0,1)/pv->xError()/pv->yError();
          pvData.posCorr[1] = pv->covariance(0,2)/pv->xError()/pv->zError();
          pvData.posCorr[2] = pv->covariance(1,2)/pv->yError()/pv->zError();
          pvStore_.push_back(pvData);

	  if(ftree_ != 0){
	    theBeamSpotTreeData_.run(iEvent.id().run());
	    theBeamSpotTreeData_.lumi(iEvent.luminosityBlock());
	    theBeamSpotTreeData_.bunchCrossing(bx);
	    theBeamSpotTreeData_.pvData(pvData);
	    ftree_->Fill();
	  }

	  if (fFitPerBunchCrossing) bxMap_[bx].push_back(pvData);

      }

  }




}

void PVFitter::setTree(TTree* tree){
  ftree_ = tree;
  theBeamSpotTreeData_.branch(ftree_);
}

bool PVFitter::runBXFitter() {

  using namespace ROOT::Minuit2;
  edm::LogInfo("PVFitter") << " Number of bunch crossings: " << bxMap_.size() << std::endl;

  bool fit_ok = true;

  for ( std::map<int,std::vector<BeamSpotFitPVData> >::const_iterator pvStore = bxMap_.begin();
	pvStore!=bxMap_.end(); ++pvStore) {

    // first set null beam spot in case
    // fit fails
    fbspotMap[pvStore->first] = reco::BeamSpot();

    edm::LogInfo("PVFitter") << " Number of PVs collected for PVFitter: " << (pvStore->second).size() << " in bx: " << pvStore->first << std::endl;

    if ( (pvStore->second).size() <= minNrVertices_ ) {
        edm::LogWarning("PVFitter") << " not enough PVs, continue" << std::endl;
	fit_ok = false;
      continue;
    }

    //bool fit_ok = false;
    edm::LogInfo("PVFitter") << "Calculating beam spot with PVs ..." << std::endl;

    //
    // LL function and fitter
    //
    FcnBeamSpotFitPV* fcn = new FcnBeamSpotFitPV(pvStore->second);
    //
    // fit parameters: positions, widths, x-y correlations, tilts in xz and yz
    //
    MnUserParameters upar;
    upar.Add("x"     , 0.   , 0.02  , -10., 10.);  // 0
    upar.Add("y"     , 0.   , 0.02  , -10., 10.);  // 1
    upar.Add("z"     , 0.   , 0.20  , -30., 30.);  // 2
    upar.Add("ex"    , 0.015, 0.01  , 0.  , 10.);  // 3
    upar.Add("corrxy", 0.   , 0.02  , -1. , 1. );  // 4
    upar.Add("ey"    , 0.015, 0.01  , 0.  , 10.);  // 5
    upar.Add("dxdz"  , 0.   , 0.0002, -0.1, 0.1);  // 6
    upar.Add("dydz"  , 0.   , 0.0002, -0.1, 0.1);  // 7
    upar.Add("ez"    , 1.   , 0.1   , 0.  , 30.);  // 8
    upar.Add("scale", errorScale_   , errorScale_/10.,
                      errorScale_/2., errorScale_*2.);      // 9
    MnMigrad migrad(*fcn, upar);

    //
    // first iteration without correlations
    //
    upar.Fix(4);
    upar.Fix(6);
    upar.Fix(7);
    upar.Fix(9);
    FunctionMinimum ierr = migrad(0,1.);
    if ( !ierr.IsValid() ) {
        edm::LogInfo("PVFitter") << "3D beam spot fit failed in 1st iteration" << std::endl;
	fit_ok = false;
      continue;
    }
    //
    // refit with harder selection on vertices
    //
    fcn->setLimits(upar.Value(0)-sigmaCut_*upar.Value(3),
		   upar.Value(0)+sigmaCut_*upar.Value(3),
		   upar.Value(1)-sigmaCut_*upar.Value(5),
		   upar.Value(1)+sigmaCut_*upar.Value(5),
		   upar.Value(2)-sigmaCut_*upar.Value(8),
		   upar.Value(2)+sigmaCut_*upar.Value(8));
    ierr = migrad(0,1.);
    if ( !ierr.IsValid() ) {
      edm::LogInfo("PVFitter") << "3D beam spot fit failed in 2nd iteration" << std::endl;
      fit_ok = false;
      continue;
    }
    //
    // refit with correlations
    //
    upar.Release(4);
    upar.Release(6);
    upar.Release(7);
    ierr = migrad(0,1.);
    if ( !ierr.IsValid() ) {
        edm::LogInfo("PVFitter") << "3D beam spot fit failed in 3rd iteration" << std::endl;
	fit_ok = false;
      continue;
    }
    // refit with floating scale factor
    //   minuitx.ReleaseParameter(9);
    //   minuitx.Minimize();

    //minuitx.PrintResults(0,0);

    fwidthX = upar.Value(3);
    fwidthY = upar.Value(5);
    fwidthZ = upar.Value(8);
    fwidthXerr = upar.Error(3);
    fwidthYerr = upar.Error(5);
    fwidthZerr = upar.Error(8);

    reco::BeamSpot::CovarianceMatrix matrix;
    // need to get the full cov matrix
    matrix(0,0) = pow( upar.Error(0), 2);
    matrix(1,1) = pow( upar.Error(1), 2);
    matrix(2,2) = pow( upar.Error(2), 2);
    matrix(3,3) = fwidthZerr * fwidthZerr;
    matrix(4,4) = pow( upar.Error(6), 2);
    matrix(5,5) = pow( upar.Error(7), 2);
    matrix(6,6) = fwidthXerr * fwidthXerr;

    fbeamspot = reco::BeamSpot( reco::BeamSpot::Point(upar.Value(0),
						      upar.Value(1),
						      upar.Value(2) ),
				fwidthZ,
				upar.Value(6), upar.Value(7),
				fwidthX,
				matrix );
    fbeamspot.setBeamWidthX( fwidthX );
    fbeamspot.setBeamWidthY( fwidthY );
    fbeamspot.setType( reco::BeamSpot::Tracker );

    fbspotMap[pvStore->first] = fbeamspot;
    edm::LogInfo("PVFitter") << "3D PV fit done for this bunch crossing."<<std::endl;
    //delete fcn;
    fit_ok = fit_ok & true;
  }

  return fit_ok;
}


bool PVFitter::runFitter() {

    using namespace ROOT::Minuit2;
    edm::LogInfo("PVFitter") << " Number of PVs collected for PVFitter: " << pvStore_.size() << std::endl;
    CO("pvStore_.size()",pvStore_.size() ) ;
    CO("minNrVertices_" ,minNrVertices_  ) ;
    if ( pvStore_.size() <= minNrVertices_ ) return false;

    //bool fit_ok = false;

    TH1F *h1PVx = (TH1F*) hPVx->ProjectionX("h1PVx", 0, -1, "e");
    TH1F *h1PVy = (TH1F*) hPVy->ProjectionX("h1PVy", 0, -1, "e");
    TH1F *h1PVz = (TH1F*) hPVx->ProjectionY("h1PVz", 0, -1, "e");

    //Use our own copy for thread safety
    TF1 gaus("localGaus","gaus");

    h1PVx->Fit(&gaus,"QLM0");
    h1PVy->Fit(&gaus,"QLM0");
    h1PVz->Fit(&gaus,"QLM0");

    TF1 *gausx  = h1PVx->GetFunction("localGaus");
    TF1 *gausy  = h1PVy->GetFunction("localGaus");
    TF1 *gausz  = h1PVz->GetFunction("localGaus");

    fwidthX     = gausx->GetParameter(2); // First estimate of beam width X size
    fwidthY     = gausy->GetParameter(2); // First estimate of beam width Y size
    fwidthZ     = gausz->GetParameter(2); // First estimate of beam width Z size
    fwidthXerr  = gausx->GetParError (2);
    fwidthYerr  = gausy->GetParError (2);
    fwidthZerr  = gausz->GetParError (2);
    
    double estXpos = gausx->GetParameter(1); // First estimate of X beamspot position
    double estYpos = gausy->GetParameter(1); // First estimate of Y beamspot position 
    double estZpos = gausz->GetParameter(1); // First estimate of Z beamspot position
    double estXerr = gausx->GetParError (1); // First estimate of X beamspot position error
    double estYerr = gausy->GetParError (1); // First estimate of Y beamspot position error
    double estZerr = gausz->GetParError (1); // First estimate of Z beamspot position error
    double estXWid = gausx->GetParameter(2); // First estimate of beam width X size 
    double estYWid = gausy->GetParameter(2); // First estimate of beam width Y size 
    double estZWid = gausz->GetParameter(2); // First estimate of beam width Z size 
    double estXWer = gausx->GetParError (2); // First estimate of beam width X size error 
    double estYWer = gausy->GetParError (2); // First estimate of beam width Y size error
    double estZWer = gausz->GetParError (2); // First estimate of beam width Z size error

    if ( ! do3DFit_ ) {

      reco::BeamSpot::CovarianceMatrix matrix;
      matrix(2,2) = gausz->GetParError(1) * gausz->GetParError(1);
      matrix(3,3) = fwidthZerr * fwidthZerr;
      matrix(6,6) = fwidthXerr * fwidthXerr;

      fbeamspot = reco::BeamSpot( reco::BeamSpot::Point(gausx->GetParameter(1),
                                                        gausy->GetParameter(1),
                                                        gausz->GetParameter(1) ),
                                  fwidthZ,
                                  0., 0.,
                                  fwidthX,
                                  matrix );
      fbeamspot.setBeamWidthX( fwidthX );
      fbeamspot.setBeamWidthY( fwidthY );
      fbeamspot.setType(reco::BeamSpot::Tracker);

    }
    else { // do 3D fit
      //
      // LL function and fitter
      //
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//      CO("++++++++++++++++++++++++++++++++++++++++++++++++++++++","") ;
//       double meanPosX = 0, meanPosY = 0, meanPosZ = 0;
//       double meanErrX = 0, meanErrY = 0, meanErrZ = 0;
//       for(std::vector<BeamSpotFitPVData>::iterator it=pvStore_.begin(); it!=pvStore_.end(); ++it)
//       {
//        positionH_   [0]->Fill((*it).position[0]) ; meanPosX += (*it).position[0] ;
//        positionH_   [1]->Fill((*it).position[1]) ; meanPosY += (*it).position[1] ;
//        positionH_   [2]->Fill((*it).position[2]) ; meanPosZ += (*it).position[2] ;
//        errorH_      [0]->Fill((*it).posError[0]) ; meanErrX += (*it).posError[0] ;
//        errorH_      [1]->Fill((*it).posError[1]) ; meanErrY += (*it).posError[1] ;
//        errorH_      [2]->Fill((*it).posError[2]) ; meanErrZ += (*it).posError[2] ;
//        correlationH_[0]->Fill((*it).posCorr [0]) ;
//        correlationH_[1]->Fill((*it).posCorr [1]) ;
//        correlationH_[2]->Fill((*it).posCorr [2]) ;
//        spacePosXY_     ->Fill((*it).position[0],(*it).position[1]) ;  
//        spacePosXZ_     ->Fill((*it).position[0],(*it).position[2]) ;  
//        spacePosYZ_     ->Fill((*it).position[1],(*it).position[2]) ;  
//       }
//       meanPosX /= (double)pvStore_.size() ;
//       meanPosY /= (double)pvStore_.size() ;
//       meanPosZ /= (double)pvStore_.size() ;
//       meanErrX /= (double)pvStore_.size() ;
//       meanErrY /= (double)pvStore_.size() ;
//       meanErrZ /= (double)pvStore_.size() ;
//       CO("estXpos",estXpos) ; 
//       CO("estYpos",estYpos) ; 
//       CO("estZpos",estZpos) ;  
//       CO("estXerr",estXerr) ;  
//       CO("estYerr",estYerr) ;  
//       CO("estZerr",estZerr) ;  
//       CO("estXWid",estXWid) ;  
//       CO("estYWid",estYWid) ;  
//       CO("estZWid",estZWid) ;  
//       CO("estXWer",estXWer) ;  
//       CO("estYWer",estYWer) ;  
//       CO("estZWer",estZWer) ;  
//      CO("++++++++++++++++++++++++++++++++++++++++++++++++++++++","") ;
      maxTries_  = 1000 ; 
      tolerance_ = 1    ;
      MnStrategy strategy(2) ;
      fixRelMap_.clear() ;
      errorScale_ = 1.0 ;
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
      FcnBeamSpotFitPV* fcn = new FcnBeamSpotFitPV(pvStore_);
      //
      // fit parameters: positions, widths, x-y correlations, tilts in xz and yz
      //
      debug_ = true ; // debugging
      MnUserParameters upar;
      upar.Add("x"     , estXpos    , estXerr	     , -2. 	     , 2.	     ); // 0
      upar.Add("y"     , estYpos    , estYerr	     , -2. 	     , 2.	     ); // 1
      upar.Add("z"     , estZpos    , estZerr	     , -5. 	     , 5.	     ); // 2
      upar.Add("ex"    , estXWid    , estXWer        ,  0.	     , 0.1	     ); // 3
      upar.Add("corrxy", 0.25       , 0.5  	     ,  0.	     , 1.	     ); // 4
      upar.Add("ey"    , estYWid    , estYWer        ,  0.	     , 0.1	     ); // 5
      upar.Add("dxdz"  , 0.001      , 0.0002	     , -0.1 	     , 0.1 	     ); // 6
      upar.Add("dydz"  , 0.001      , 0.0002	     , -0.1 	     , 0.1 	     ); // 7
      upar.Add("ez"    , estZWid    , estZWer        , 0.   	     , 20	     ); // 8
      upar.Add("scale" , errorScale_, errorScale_/10.,-errorScale_*2., errorScale_*2.); // 9  
      MnMigrad migrad(*fcn, upar);

      int iteration = 1 ;
      // Free position, fix the rest
      fixRelMap_.insert(pair<string,int>("Fix",0)) ;
      fixRelMap_.insert(pair<string,int>("Fix",1)) ;
      fixRelMap_.insert(pair<string,int>("Fix",2)) ;
      fixRelMap_.insert(pair<string,int>("Fix",3)) ;
      fixRelMap_.insert(pair<string,int>("Rel",4)) ;
      fixRelMap_.insert(pair<string,int>("Fix",5)) ;
      fixRelMap_.insert(pair<string,int>("Rel",6)) ;
      fixRelMap_.insert(pair<string,int>("Rel",7)) ;
      fixRelMap_.insert(pair<string,int>("Fix",8)) ;
      fixRelMap_.insert(pair<string,int>("Fix",9)) ;
      if( ! guideTheFit(migrad,iteration++)) return false ;

      // Free position and width, fix the rest
      fixRelMap_.insert(pair<string,int>("Rel",0)) ;
      fixRelMap_.insert(pair<string,int>("Rel",1)) ;
      fixRelMap_.insert(pair<string,int>("Rel",2)) ;
      fixRelMap_.insert(pair<string,int>("Fix",3)) ;
      fixRelMap_.insert(pair<string,int>("Fix",4)) ;
      fixRelMap_.insert(pair<string,int>("Fix",5)) ;
      fixRelMap_.insert(pair<string,int>("Rel",6)) ;
      fixRelMap_.insert(pair<string,int>("Rel",7)) ;
      fixRelMap_.insert(pair<string,int>("Fix",8)) ;
      fixRelMap_.insert(pair<string,int>("Fix",9)) ;
      if( ! guideTheFit(migrad,iteration++)) return false ; 

      // Free width, slopes and correlation, fix the rest
      fixRelMap_.insert(pair<string,int>("Rel",0)) ;
      fixRelMap_.insert(pair<string,int>("Rel",1)) ;
      fixRelMap_.insert(pair<string,int>("Rel",2)) ;
      fixRelMap_.insert(pair<string,int>("Rel",3)) ;
      fixRelMap_.insert(pair<string,int>("Fix",4)) ;
      fixRelMap_.insert(pair<string,int>("Rel",5)) ;
      fixRelMap_.insert(pair<string,int>("Rel",6)) ;
      fixRelMap_.insert(pair<string,int>("Rel",7)) ;
      fixRelMap_.insert(pair<string,int>("Rel",8)) ;
      fixRelMap_.insert(pair<string,int>("Fix",9)) ;
      if( ! guideTheFit(migrad,iteration++)) return false ; 

      // Free width and slopes, fix the rest
//       fixRelMap_.insert(pair<string,int>("Fix",0)) ;
//       fixRelMap_.insert(pair<string,int>("Fix",1)) ;
//       fixRelMap_.insert(pair<string,int>("Fix",2)) ;
//       fixRelMap_.insert(pair<string,int>("Rel",3)) ;
//       fixRelMap_.insert(pair<string,int>("Fix",4)) ;
//       fixRelMap_.insert(pair<string,int>("Rel",5)) ;
//       fixRelMap_.insert(pair<string,int>("Rel",6)) ;
//       fixRelMap_.insert(pair<string,int>("Rel",7)) ;
//       fixRelMap_.insert(pair<string,int>("Rel",8)) ;
//       fixRelMap_.insert(pair<string,int>("Fix",9)) ;
//       if( ! guideTheFit(migrad,iteration++)) return false ; 
/*
      fixRelMap_.insert(pair<string,int>("Fix",6)) ;
      fixRelMap_.insert(pair<string,int>("Fix",7)) ;
      fixRelMap_.insert(pair<string,int>("Rel",4)) ;
      if( ! guideTheFit(migrad,4)) return false ; 
*/
      for(int par=0; par<8; ++par)
       fixRelMap_.insert(pair<string,int>("Rel",par)) ;
      if( ! guideTheFit(migrad,iteration++)) return false ; 
      
      fwidthX    = results_[3];
      fwidthY    = results_[5];
      fwidthZ    = results_[8];
      fwidthXerr = errors_ [3];
      fwidthYerr = errors_ [5];
      fwidthZerr = errors_ [8];

      // check errors on widths and sigmaZ for nan
      if ( edm::isNotFinite(fwidthXerr) || edm::isNotFinite(fwidthYerr) || edm::isNotFinite(fwidthZerr) ) {
          edm::LogWarning("PVFitter") << "3D beam spot fit returns nan in 3rd iteration" << std::endl;
          return false;
      }

      reco::BeamSpot::CovarianceMatrix matrix;
      // need to get the full cov matrix
      matrix(0,0) = pow( errors_[0], 2);
      matrix(1,1) = pow( errors_[1], 2);
      matrix(2,2) = pow( errors_[2], 2);
      matrix(3,3) = fwidthZerr * fwidthZerr;
      matrix(6,6) = fwidthXerr * fwidthXerr;

      fbeamspot = reco::BeamSpot( reco::BeamSpot::Point(results_[0],
                                                        results_[1],
                                                        results_[2]),
                                  fwidthZ,
                                  results_[6], results_[7],
                                  fwidthX,
                                  matrix );
      fbeamspot.setBeamWidthX( fwidthX );
      fbeamspot.setBeamWidthY( fwidthY );
      fbeamspot.setType(reco::BeamSpot::Tracker); 
    }

    return true; //FIXME: Need to add quality test for the fit results!
}

void PVFitter::dumpTxtFile(){
/*
  fasciiFile << "Runnumber " << frun << std::endl;
  fasciiFile << "BeginTimeOfFit " << fbeginTimeOfFit << std::endl;
  fasciiFile << "EndTimeOfFit " << fendTimeOfFit << std::endl;
  fasciiFile << "LumiRange " << fbeginLumiOfFit << " - " << fendLumiOfFit << std::endl;
  fasciiFile << "Type " << fbeamspot.type() << std::endl;
  fasciiFile << "X0 " << fbeamspot.x0() << std::endl;
  fasciiFile << "Y0 " << fbeamspot.y0() << std::endl;
  fasciiFile << "Z0 " << fbeamspot.z0() << std::endl;
  fasciiFile << "sigmaZ0 " << fbeamspot.sigmaZ() << std::endl;
  fasciiFile << "dxdz " << fbeamspot.dxdz() << std::endl;
  fasciiFile << "dydz " << fbeamspot.dydz() << std::endl;
  if (inputBeamWidth_ > 0 ) {
    fasciiFile << "BeamWidthX " << inputBeamWidth_ << std::endl;
    fasciiFile << "BeamWidthY " << inputBeamWidth_ << std::endl;
  } else {
    fasciiFile << "BeamWidthX " << fbeamspot.BeamWidthX() << std::endl;
    fasciiFile << "BeamWidthY " << fbeamspot.BeamWidthY() << std::endl;
  }

  for (int i = 0; i<6; ++i) {
    fasciiFile << "Cov("<<i<<",j) ";
    for (int j=0; j<7; ++j) {
      fasciiFile << fbeamspot.covariance(i,j) << " ";
    }
    fasciiFile << std::endl;
  }
  // beam width error
  if (inputBeamWidth_ > 0 ) {
    fasciiFile << "Cov(6,j) 0 0 0 0 0 0 " << "1e-4" << std::endl;
  } else {
    fasciiFile << "Cov(6,j) 0 0 0 0 0 0 " << fbeamspot.covariance(6,6) << std::endl;
  }
  fasciiFile << "EmittanceX " << fbeamspot.emittanceX() << std::endl;
  fasciiFile << "EmittanceY " << fbeamspot.emittanceY() << std::endl;
  fasciiFile << "BetaStar " << fbeamspot.betaStar() << std::endl;

*/
}


void
PVFitter::compressStore ()
{
  //
  // fill vertex qualities
  //
  pvQualities_.resize(pvStore_.size());
  for ( unsigned int i=0; i<pvStore_.size(); ++i )  pvQualities_[i] = pvQuality(pvStore_[i]);
  sort(pvQualities_.begin(),pvQualities_.end());
  //
  // Set new quality cut to median. This cut will be used to reduce the
  // number of vertices in the store and also apply to all new vertices
  // until the next reset
  //
  dynamicQualityCut_ = pvQualities_[pvQualities_.size()/2];
  //
  // remove all vertices failing the cut from the store
  //   (to be moved to a more efficient memory management!)
  //
  unsigned int iwrite(0);
  for ( unsigned int i=0; i<pvStore_.size(); ++i ) {
    if ( pvQuality(pvStore_[i])>dynamicQualityCut_ )  continue;
    if ( i!=iwrite )  pvStore_[iwrite] = pvStore_[i];
    ++iwrite;
  }
  pvStore_.resize(iwrite);
  edm::LogInfo("PVFitter") << "Reduced primary vertex store size to "
                           << pvStore_.size() << " ; new dynamic quality cut = "
                           << dynamicQualityCut_ << std::endl;

}

double
PVFitter::pvQuality (const reco::Vertex& pv) const
{
  //
  // determinant of the transverse part of the PV covariance matrix
  //
  return
    pv.covariance(0,0)*pv.covariance(1,1)-
    pv.covariance(0,1)*pv.covariance(0,1);
}

double
PVFitter::pvQuality (const BeamSpotFitPVData& pv) const
{
  //
  // determinant of the transverse part of the PV covariance matrix
  //
  double ex = pv.posError[0];
  double ey = pv.posError[1];
  return ex*ex*ey*ey*(1-pv.posCorr[0]*pv.posCorr[0]);
}
  
  
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
bool PVFitter::guideTheFit(ROOT::Minuit2::MnMigrad& migrad, int num) 
{

 for(map<string,int>::iterator it =fixRelMap_.begin(); it!=fixRelMap_.end(); ++it)
 {
  if( it->first == "Fix" )
   migrad.Fix    (it->second); 
  else
   migrad.Release(it->second); 
  CO(it->first,it->second) ;
 }
 
 ROOT::Minuit2::FunctionMinimum ierr = migrad(maxTries_,tolerance_);
 results_ = ierr.UserParameters().Params() ;						  
 errors_  = ierr.UserParameters().Errors() ;
 
 fixRelMap_.clear() ;
 						  
 if( debug_ ) 
 {
  cout << "======== Iteration " << num << " =============" << endl ;
  cout << ierr << endl ;
 }
 
 if ( !ierr.IsValid() ) 
 {
     CO("3D beam spot fit failed in iteration",num) ;
     edm::LogWarning("PVFitter") << "3D beam spot fit failed in iteration " << num << std::endl;
     return false;
 }
 for(unsigned int i=0; i<results_.size(); ++i)
 {
  if( edm::isNotFinite(results_[i]) )
  {
     CO("3D beam spot fit succeed in iteration",num) ;
     CO("but parameter is nan",i) ;
     edm::LogWarning("PVFitter") << "3D beam spot fit succeed in iteration " << num 
                                 << " but parameter " << i << " is nan"
                                 << std::endl;
     return false;
  }
  if( edm::isNotFinite(errors_[i]) )
  {
     CO("3D beam spot fit succeed in iteration",num) ;
     CO("but parameter error is nan",i) ;
     edm::LogWarning("PVFitter") << "3D beam spot fit succeed in iteration " << num 
                                 << " but parameter error " << i << " is nan"
                                 << std::endl;
     return false;
  }
 }
 
 return true ;
}
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
