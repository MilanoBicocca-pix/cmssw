/**_________________________________________________________________
   class:   PVFitter.cc
   package: RecoVertex/BeamSpotProducer

   author: Francisco Yumiceva, Fermilab (yumiceva@fnal.gov)
           Geng-Yuan Jeng, UC Riverside (Geng-Yuan.Jeng@cern.ch)
________________________________________________________________**/

#include "CondCore/DBOutputService/interface/PoolDBOutputService.h"
#include "CondFormats/BeamSpotObjects/interface/BeamSpotObjects.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/TrackCandidate/interface/TrackCandidate.h"
#include "DataFormats/TrackCandidate/interface/TrackCandidateCollection.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/TrackReco/interface/HitPattern.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "RecoVertex/BeamSpotProducer/interface/FcnBeamSpotFitPV.h"
#include "RecoVertex/BeamSpotProducer/interface/PVFitter.h"

//#define _OLDMINUIT_ 1

#include "RecoVertex/BeamSpotProducer/interface/helpers.h"

#ifdef _OLDMINUIT_
  #include "TFitterMinuit.h" 
#else
  #include "FWCore/Utilities/interface/isFinite.h"
  #include "Minuit2/FunctionMinimum.h"
  #include "Minuit2/MnMigrad.h"
  #include "Minuit2/MnPrint.h"
#endif

#include "Minuit2/FCNBase.h"

#include "TF1.h"

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
//==============================================================================
PVFitter::PVFitter(const edm::ParameterSet       & iConfig,
                         edm::ConsumesCollector && iColl )
  : ftree_(0)
{
  _HERE_() ;
  initialize(iConfig, iColl);
}

//==============================================================================
PVFitter::PVFitter(const edm::ParameterSet      & iConfig,
                         edm::ConsumesCollector & iColl )
    :ftree_(0)
{
  _HERE_() ;
  initialize(iConfig, iColl);
}

//==============================================================================
void PVFitter::initialize(const edm::ParameterSet      & iConfig,
                                edm::ConsumesCollector & iColl)
{
  _HERE_() ;
  edm::ParameterSet _ps = iConfig.getParameter<edm::ParameterSet>("PVFitter") ;

  debug_               = _ps.getUntrackedParameter<bool>("Debug");
  vertexToken_         = iColl.consumes<reco::VertexCollection>( 
                        					_ps.getUntrackedParameter<edm::InputTag>("VertexCollection",
                        										 edm::InputTag("offlinePrimaryVertices")
		        										)
                        				       );
  do3DFit_             = _ps.getUntrackedParameter<bool>	("Apply3DFit"	      );
  //writeTxt_          = _ps.getUntrackedParameter<bool>	("WriteAscii"	      );
  //outputTxt_         = _ps.getUntrackedParameter<std::string> ("AsciiFileName"      );
  maxNrVertices_       = _ps.getUntrackedParameter<unsigned int>("maxNrStoredVertices");
  minNrVertices_       = _ps.getUntrackedParameter<unsigned int>("minNrVerticesForFit");
  minVtxNdf_           = _ps.getUntrackedParameter<double>	("minVertexNdf"       );
  maxVtxNormChi2_      = _ps.getUntrackedParameter<double>	("maxVertexNormChi2"  );
  minVtxTracks_        = _ps.getUntrackedParameter<unsigned int>("minVertexNTracks"   );
  minVtxWgt_           = _ps.getUntrackedParameter<double>	("minVertexMeanWeight");
  maxVtxR_             = _ps.getUntrackedParameter<double>	("maxVertexR"	      );
  maxVtxZ_             = _ps.getUntrackedParameter<double>	("maxVertexZ"	      );
  errorScale_          = _ps.getUntrackedParameter<double>	("errorScale"	      );
  sigmaCut_            = _ps.getUntrackedParameter<double>	("nSigmaCut"	      );
  fFitPerBunchCrossing = _ps.getUntrackedParameter<bool>        ("FitPerBunchCrossing");

  // preset quality cut to "infinite"
  dynamicQualityCut_ = 1.e30;

  hPVx = new TH2F("hPVx","PVx vs PVz distribution",200,-maxVtxR_, maxVtxR_, 200, -maxVtxZ_, maxVtxZ_);
  hPVy = new TH2F("hPVy","PVy vs PVz distribution",200,-maxVtxR_, maxVtxR_, 200, -maxVtxZ_, maxVtxZ_);
}

//==============================================================================
PVFitter::~PVFitter() 
{
  _HERE_() ;
}

//==============================================================================
void PVFitter::readEvent(const edm::Event& iEvent)
{

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

  if ( iEvent.getByToken(vertexToken_, PVCollection ) ) 
  {
    //pv = *PVCollection;
    //vertices = *PVCollection;
    hasPVs = true;
  }
  //------

  if ( hasPVs ) 
  {
    for (reco::VertexCollection::const_iterator pv  = PVCollection->begin(); 
                                                pv != PVCollection->end(); 
					      ++pv ) 
    {
       //for ( size_t ipv=0; ipv != pv.size(); ++ipv ) {

      //--- vertex selection
      if ( pv->isFake() || pv->tracksSize()==0 )                                       continue;
      if ( pv->ndof() < minVtxNdf_ || (pv->ndof()+3.)/pv->tracksSize()<2*minVtxWgt_ )  continue;
      //---
      hPVx->Fill( pv->x(), pv->z() );
      hPVy->Fill( pv->y(), pv->z() );
      //
      // 3D fit section
      //
      // apply additional quality cut
      if ( pvQuality(*pv)>dynamicQualityCut_ )                                         continue;
      // if store exceeds max. size: reduce size and apply new quality cut
      if ( pvStore_.size()>=maxNrVertices_ ) 
      {
        compressStore();
        if ( pvQuality(*pv)>dynamicQualityCut_ )                                       continue;
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
      pvData.posCorr[0]  = pv->covariance(0,1)/pv->xError()/pv->yError();
      pvData.posCorr[1]  = pv->covariance(0,2)/pv->xError()/pv->zError();
      pvData.posCorr[2]  = pv->covariance(1,2)/pv->yError()/pv->zError();
      pvStore_.push_back(pvData);

      if(ftree_ != 0)
      {
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

//==============================================================================
void PVFitter::setTree(TTree* tree)
{
  ftree_ = tree;
  theBeamSpotTreeData_.branch(ftree_);
}

//==============================================================================
bool PVFitter::runBXFitter() 
{

  using namespace ROOT::Minuit2;

  edm::LogInfo("PVFitter") << " Number of bunch crossings: " 
                           << bxMap_.size() 
			   << std::endl;

  bool fit_ok = true;

  for ( std::map<int,std::vector<BeamSpotFitPVData> >::const_iterator pvStore  = bxMap_.begin();
	                                                              pvStore != bxMap_.end(); 
								    ++pvStore) 
  {
    // first set null beam spot in case
    // fit fails
    fbspotMap[pvStore->first] = reco::BeamSpot();

    edm::LogInfo("PVFitter") << " Number of PVs collected for PVFitter: " 
                             << (pvStore->second).size() 
			     << " in bx: " 
			     << pvStore->first 
			     << std::endl;

    if( (pvStore->second).size() <= minNrVertices_ ) 
    {
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
#ifdef _OLDMINUIT_
    TFitterMinuit minuitx;
    minuitx.SetMinuitFCN(fcn);
    //
    // fit parameters: positions, widths, x-y correlations, tilts in xz and yz
    //
    minuitx.SetParameter(0,"x",0.,0.02,-10.,10.);
    minuitx.SetParameter(1,"y",0.,0.02,-10.,10.);
    minuitx.SetParameter(2,"z",0.,0.20,-30.,30.);
    minuitx.SetParameter(3,"ex",0.015,0.01,0.,10.);
    minuitx.SetParameter(4,"corrxy",0.,0.02,-1.,1.);
    minuitx.SetParameter(5,"ey",0.015,0.01,0.,10.);
    minuitx.SetParameter(6,"dxdz",0.,0.0002,-0.1,0.1);
    minuitx.SetParameter(7,"dydz",0.,0.0002,-0.1,0.1);
    minuitx.SetParameter(8,"ez",1.,0.1,0.,30.);
    minuitx.SetParameter(9,"scale",errorScale_,errorScale_/10.,errorScale_/2.,errorScale_*2.);
    //
    // first iteration without correlations
    //
    int ierr(0);
    minuitx.FixParameter(4);
    minuitx.FixParameter(6);
    minuitx.FixParameter(7);
    minuitx.FixParameter(9);
    minuitx.SetMaxIterations(100);
    //       minuitx.SetPrintLevel(3);
    minuitx.SetPrintLevel(0);
    minuitx.CreateMinimizer();
    ierr = minuitx.Minimize();
    if ( ierr ) 
    {
	edm::LogInfo("PVFitter") << "3D beam spot fit failed in 1st iteration" << std::endl;
    fit_ok = false;
      continue;
    }
    //
    // refit with harder selection on vertices
    //
    fcn->setLimits(minuitx.GetParameter(0)-sigmaCut_*minuitx.GetParameter(3),
	   minuitx.GetParameter(0)+sigmaCut_*minuitx.GetParameter(3),
	   minuitx.GetParameter(1)-sigmaCut_*minuitx.GetParameter(5),
	   minuitx.GetParameter(1)+sigmaCut_*minuitx.GetParameter(5),
	   minuitx.GetParameter(2)-sigmaCut_*minuitx.GetParameter(8),
	   minuitx.GetParameter(2)+sigmaCut_*minuitx.GetParameter(8));
    ierr = minuitx.Minimize();
    if ( ierr ) 
    {
      edm::LogInfo("PVFitter") << "3D beam spot fit failed in 2nd iteration" << std::endl;
      fit_ok = false;
      continue;
    }
    //
    // refit with correlations
    //
    minuitx.ReleaseParameter(4);
    minuitx.ReleaseParameter(6);
    minuitx.ReleaseParameter(7);

    ierr = minuitx.Minimize();
    if ( ierr ) 
    {
	edm::LogInfo("PVFitter") << "3D beam spot fit failed in 3rd iteration" << std::endl;
    fit_ok = false;
      continue;
    }
    // refit with floating scale factor
    //   minuitx.ReleaseParameter(9);
    //   minuitx.Minimize();

    //minuitx.PrintResults(0,0);

    fwidthX = minuitx.GetParameter(3);
    fwidthY = minuitx.GetParameter(5);
    fwidthZ = minuitx.GetParameter(8);
    fwidthXerr = minuitx.GetParError(3);
    fwidthYerr = minuitx.GetParError(5);
    fwidthZerr = minuitx.GetParError(8);

    reco::BeamSpot::CovarianceMatrix matrix;
    // need to get the full cov matrix
    matrix(0,0) = pow( minuitx.GetParError(0), 2);
    matrix(1,1) = pow( minuitx.GetParError(1), 2);
    matrix(2,2) = pow( minuitx.GetParError(2), 2);
    matrix(3,3) = fwidthZerr * fwidthZerr;
    matrix(4,4) = pow( minuitx.GetParError(6), 2);
    matrix(5,5) = pow( minuitx.GetParError(7), 2);
    matrix(6,6) = fwidthXerr * fwidthXerr;

    fbeamspot = reco::BeamSpot( reco::BeamSpot::Point(minuitx.GetParameter(0),
			      minuitx.GetParameter(1),
			      minuitx.GetParameter(2) ),
		fwidthZ,
		minuitx.GetParameter(6), minuitx.GetParameter(7),
		fwidthX,
		matrix );
    fbeamspot.setBeamWidthX( fwidthX );
    fbeamspot.setBeamWidthY( fwidthY );
    fbeamspot.setType( reco::BeamSpot::Tracker );

    fbspotMap[pvStore->first] = fbeamspot;
#else
    //
    // fit parameters: positions, widths, x-y correlations, tilts in xz and yz
    //
    MnUserParameters upar;
    upar.Add("x"     , 0.   	  , 0.02  	   , -10.	  , 10. 	  ); // 0
    upar.Add("y"     , 0.   	  , 0.02  	   , -10.	  , 10. 	  ); // 1
    upar.Add("z"     , 0.   	  , 0.20  	   , -30.	  , 30. 	  ); // 2
    upar.Add("ex"    , 0.015	  , 0.01  	   , 0.  	  , 10. 	  ); // 3
    upar.Add("corrxy", 0.   	  , 0.02  	   , -1. 	  ,  1. 	  ); // 4
    upar.Add("ey"    , 0.015	  , 0.01  	   , 0.  	  , 10. 	  ); // 5
    upar.Add("dxdz"  , 0.   	  , 0.0002	   , -0.1	  ,  0.1	  ); // 6
    upar.Add("dydz"  , 0.   	  , 0.0002	   , -0.1	  ,  0.1	  ); // 7
    upar.Add("ez"    , 1.   	  , 0.1   	   , 0.  	  , 30. 	  ); // 8
    upar.Add("scale" , errorScale_, errorScale_/10.,errorScale_/2., errorScale_*2.); // 9
    MnMigrad migrad(*fcn, upar);

    //
    // first iteration without correlations
    //
    upar.Fix(4);
    upar.Fix(6);
    upar.Fix(7);
    upar.Fix(9);
    FunctionMinimum ierr = migrad();
    if ( !ierr.IsValid() ) 
    {
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
    ierr = migrad();
    if ( !ierr.IsValid() ) 
    {
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
    ierr = migrad();
    if ( !ierr.IsValid() ) 
    {
      edm::LogInfo("PVFitter") << "3D beam spot fit failed in 3rd iteration" << std::endl;
      fit_ok = false;
      continue;
    }
    // refit with floating scale factor
    //   minuitx.ReleaseParameter(9);
    //   minuitx.Minimize();

    //minuitx.PrintResults(0,0);

    fwidthX    = upar.Value(3);
    fwidthY    = upar.Value(5);
    fwidthZ    = upar.Value(8);
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
				upar.Value(6), 
				upar.Value(7),
				fwidthX,
				matrix );
    fbeamspot.setBeamWidthX( fwidthX );
    fbeamspot.setBeamWidthY( fwidthY );
    fbeamspot.setType( reco::BeamSpot::Tracker );

    fbspotMap[pvStore->first] = fbeamspot;
#endif
    edm::LogInfo("PVFitter") << "3D PV fit done for this bunch crossing."<<std::endl;
    //delete fcn;
    fit_ok = fit_ok & true;
  }

  return fit_ok;
}


//==============================================================================
bool PVFitter::runFitter() 
{
  using namespace ROOT::Minuit2;
  edm::LogInfo("PVFitter") << " Number of PVs collected for PVFitter: " 
                           << pvStore_.size() 
			   << std::endl;

  if ( pvStore_.size() <= minNrVertices_ ) return false;

  //bool fit_ok = false;

  if ( ! do3DFit_ ) 
  {
    TH1F *h1PVx = (TH1F*) hPVx->ProjectionX("h1PVx", 0, -1, "e");
    TH1F *h1PVy = (TH1F*) hPVy->ProjectionX("h1PVy", 0, -1, "e");
    TH1F *h1PVz = (TH1F*) hPVx->ProjectionY("h1PVz", 0, -1, "e");

    //Use our own copy for thread safety
    TF1 gaus("localGaus","gaus");

    h1PVx->Fit(&gaus,"QLM0");
    h1PVy->Fit(&gaus,"QLM0");
    h1PVz->Fit(&gaus,"QLM0");

    TF1 *gausx = h1PVx->GetFunction("localGaus");
    TF1 *gausy = h1PVy->GetFunction("localGaus");
    TF1 *gausz = h1PVz->GetFunction("localGaus");

    fwidthX    = gausx->GetParameter(2);
    fwidthY    = gausy->GetParameter(2);
    fwidthZ    = gausz->GetParameter(2);
    fwidthXerr = gausx->GetParError(2);
    fwidthYerr = gausy->GetParError(2);
    fwidthZerr = gausz->GetParError(2);

    reco::BeamSpot::CovarianceMatrix matrix;
    matrix(2,2) = gausz->GetParError(1) * gausz->GetParError(1);
    matrix(3,3) = fwidthZerr * fwidthZerr;
    matrix(6,6) = fwidthXerr * fwidthXerr;

    fbeamspot = reco::BeamSpot( reco::BeamSpot::Point(gausx->GetParameter(1),
 						      gausy->GetParameter(1),
 						      gausz->GetParameter(1) ),
 				fwidthZ,
 				0., 
				0.,
 				fwidthX,
 				matrix );
    fbeamspot.setBeamWidthX( fwidthX );
    fbeamspot.setBeamWidthY( fwidthY );
    fbeamspot.setType(reco::BeamSpot::Tracker);

  }
  else 
  { // do 3D fit
    int strategy = 1 ;
    H::ss_.str(""); H::ss_ << "Strategy: " << strategy ; _WARNING_(H::ss_.str()) ;
#ifdef _OLDMINUIT_
      _MSG_("Old Minuit version") ;
      FcnBeamSpotFitPV* fcn = new FcnBeamSpotFitPV(pvStore_);
      TFitterMinuit minuitx;
      minuitx.SetMinuitFCN(fcn);
      //
      // fit parameters: positions, widths, x-y correlations, tilts in xz and yz
      //
      minuitx.SetParameter(0,"x"     ,0.   	 ,0.02		 ,-10.		,10.	       );
      minuitx.SetParameter(1,"y"     ,0.   	 ,0.02		 ,-10.		,10.	       );
      minuitx.SetParameter(2,"z"     ,0.   	 ,0.20		 ,-30.		,30.	       );
      minuitx.SetParameter(3,"ex"    ,0.015	 ,0.01		 ,0.0001	,10.	       );
      minuitx.SetParameter(4,"corrxy",0.   	 ,0.02		 ,-1.		,1. 	       );
      minuitx.SetParameter(5,"ey"    ,0.015	 ,0.01		 ,0.0001	,10.	       );
      minuitx.SetParameter(6,"dxdz"  ,0.   	 ,0.0002	 ,-0.1		,0.1	       );
      minuitx.SetParameter(7,"dydz"  ,0.   	 ,0.0002	 ,-0.1		,0.1	       );
      minuitx.SetParameter(8,"ez"    ,1.   	 ,0.1		 ,1.0   	,30.	       );
      minuitx.SetParameter(9,"scale" ,errorScale_,errorScale_/10.,errorScale_/2.,errorScale_*2.);
      //
      // first iteration without correlations
      //
      int ierr(0);
      minuitx.FixParameter    (       4);
      minuitx.FixParameter    (       6);
      minuitx.FixParameter    (       7);
      minuitx.FixParameter    (       9);
      minuitx.SetMaxIterations(     100);
      minuitx.SetPrintLevel   (       0);
      minuitx.CreateMinimizer (        );
      minuitx.SetStrategy     (strategy);
      ierr = minuitx.Minimize (        );
      if ( ierr ) 
      {
	  edm::LogWarning("PVFitter") << "3D beam spot fit failed in 1st iteration" << std::endl;
	  _WARNING_("3D beam spot fit failed in 1st iteration") ;
	  return false;
      }
      _RESULTS_("3D beam spot fit passed 1st iteration") ;
      //
      // refit with harder selection on vertices
      //
      fcn->setLimits(minuitx.GetParameter(0)-sigmaCut_*minuitx.GetParameter(3),
	     	     minuitx.GetParameter(0)+sigmaCut_*minuitx.GetParameter(3),
	     	     minuitx.GetParameter(1)-sigmaCut_*minuitx.GetParameter(5),
	     	     minuitx.GetParameter(1)+sigmaCut_*minuitx.GetParameter(5),
	     	     minuitx.GetParameter(2)-sigmaCut_*minuitx.GetParameter(8),
	     	     minuitx.GetParameter(2)+sigmaCut_*minuitx.GetParameter(8));
      ierr = minuitx.Minimize();
      if ( ierr ) 
      {
	  edm::LogWarning("PVFitter") << "3D beam spot fit failed in 2nd iteration" << std::endl;
	  _WARNING_("3D beam spot fit failed in 2nd iteration") ;
	  return false;
      }
      _RESULTS_("3D beam spot fit passed 2nd iteration") ;
      //
      // refit with correlations
      //
      minuitx.ReleaseParameter(4);
      minuitx.ReleaseParameter(6);
      minuitx.ReleaseParameter(7);
      ierr = minuitx.Minimize();
      if ( ierr ) 
      {
	  edm::LogWarning("PVFitter") << "3D beam spot fit failed in 3rd iteration" << std::endl;
	  _WARNING_("3D beam spot fit failed in 3rd iteration") ;
	  return false;
      }
      _RESULTS_("3D beam spot fit passed 3rd iteration") ;
      // refit with floating scale factor
      //   minuitx.ReleaseParameter(9);
      //   minuitx.Minimize();

      //minuitx.PrintResults(0,0);

      fwidthX 	 = minuitx.GetParameter(3);
      fwidthY 	 = minuitx.GetParameter(5);
      fwidthZ 	 = minuitx.GetParameter(8);
      fwidthXerr = minuitx.GetParError(3);
      fwidthYerr = minuitx.GetParError(5);
      fwidthZerr = minuitx.GetParError(8);

      // check errors on widths and sigmaZ for nan
      if ( std::isnan(fwidthXerr) || std::isnan(fwidthYerr) || std::isnan(fwidthZerr) ) 
      {
	  edm::LogWarning("PVFitter") << "3D beam spot fit returns nan in 3rd iteration" << std::endl;
	  return false;
      }

      reco::BeamSpot::CovarianceMatrix matrix;
      // need to get the full cov matrix
      matrix(0,0) = pow( minuitx.GetParError(0), 2);
      matrix(1,1) = pow( minuitx.GetParError(1), 2);
      matrix(2,2) = pow( minuitx.GetParError(2), 2);
      matrix(3,3) = fwidthZerr * fwidthZerr;
      matrix(6,6) = fwidthXerr * fwidthXerr;

      fbeamspot = reco::BeamSpot( reco::BeamSpot::Point(minuitx.GetParameter(0),
							minuitx.GetParameter(1),
							minuitx.GetParameter(2) ),
				  fwidthZ,
				  minuitx.GetParameter(6), minuitx.GetParameter(7),
				  fwidthX,
				  matrix );
      fbeamspot.setBeamWidthX( fwidthX );
      fbeamspot.setBeamWidthY( fwidthY );
      fbeamspot.setType(reco::BeamSpot::Tracker);
#else
      vector<double> results ;
      vector<double> errors  ;
      _MSG_("New Minuit version") ;
      //
      // LL function and fitter
      //
      FcnBeamSpotFitPV* fcn = new FcnBeamSpotFitPV(pvStore_);
      MnStrategy theStrategy(strategy) ;
      //
      // fit parameters: positions, widths, x-y correlations, tilts in xz and yz
      //
      MnUserParameters upar;
      upar.Add("x"     , 0.	    , 0.02	     , -10.	     , 10.	     ); // 0
      upar.Add("y"     , 0.	    , 0.02	     , -10.	     , 10.	     ); // 1
      upar.Add("z"     , 0.	    , 0.20	     , -30.	     , 30.	     ); // 2
      upar.Add("ex"    , 0.015      , 0.01	     ,   0.0001      , 10.	     ); // 3
      upar.Add("corrxy", 0.	    , 0.02	     ,  -1.	     ,  1.	     ); // 4
      upar.Add("ey"    , 0.015      , 0.01	     ,   0.0001      , 10.	     ); // 5
      upar.Add("dxdz"  , 0.	    , 0.0002	     ,  -0.1	     ,  0.1	     ); // 6
      upar.Add("dydz"  , 0.	    , 0.0002	     ,  -0.1	     ,  0.1	     ); // 7
      upar.Add("ez"    , 1.	    , 0.1	     ,   1.0	     , 30.	     ); // 8
      upar.Add("scale" , errorScale_, errorScale_/10., errorScale_/2., errorScale_*2.); // 9
      MnMigrad migrad(*fcn, upar, theStrategy);
      //
      // first iteration without correlations
      //
      migrad.Fix(4);
      migrad.Fix(6);
      migrad.Fix(7);
      migrad.Fix(9);
      
      FunctionMinimum ierr = migrad();
      if ( !ierr.IsValid() ) 
      {
        edm::LogWarning("PVFitter") << "3D beam spot fit failed in 1st iteration" << std::endl;
        _WARNING_("3D beam spot fit failed in 1st iteration") ;
//         H::ss_.str("") ; H::ss_ << "HasAccurateCovar	 " << ierr.HasAccurateCovar()	; _WARNING_(H::ss_.str()) ;
//         H::ss_.str("") ; H::ss_ << "HasCovariance	 " << ierr.HasCovariance()	; _WARNING_(H::ss_.str()) ;
//         H::ss_.str("") ; H::ss_ << "HasMadePosDefCovar   " << ierr.HasMadePosDefCovar() ; _WARNING_(H::ss_.str()) ;
//         H::ss_.str("") ; H::ss_ << "HasPosDefCovar	 " << ierr.HasPosDefCovar()	; _WARNING_(H::ss_.str()) ;
//         H::ss_.str("") ; H::ss_ << "HasReachedCallLimit  " << ierr.HasReachedCallLimit(); _WARNING_(H::ss_.str()) ;
//         H::ss_.str("") ; H::ss_ << "HasValidCovariance   " << ierr.HasValidCovariance() ; _WARNING_(H::ss_.str()) ;
//         H::ss_.str("") ; H::ss_ << "HasValidParameters   " << ierr.HasValidParameters() ; _WARNING_(H::ss_.str()) ;
//         H::ss_.str("") ; H::ss_ << "HesseFailed 	 " << ierr.HesseFailed()	; _WARNING_(H::ss_.str()) ;
//         H::ss_.str("") ; H::ss_ << "IsAboveMaxEdm	 " << ierr.IsAboveMaxEdm()	; _WARNING_(H::ss_.str()) ;
//         H::ss_.str("") ; H::ss_ << "ierr: "		   << endl << ierr << endl      ; _WARNING_(H::ss_.str()) ;
        return false;
      }
      _RESULTS_("3D beam spot fit passed 1st iteration") ;
      //								
      // refit with harder selection on vertices
      //
      fcn->setLimits(results[0]-sigmaCut_*results[3],
        	     results[0]+sigmaCut_*results[3],
        	     results[1]-sigmaCut_*results[5],
        	     results[1]+sigmaCut_*results[5],
        	     results[2]-sigmaCut_*results[8],
        	     results[2]+sigmaCut_*results[8]);
      cout << __LINE__ << "] new limits: "
           << setw(22) << setprecision(15) 
	   << results[0] << " +/- " << sigmaCut_ << " * " << results[3] << endl
	   << results[1] << " +/- " << sigmaCut_ << " * " << results[5] << endl
	   << results[2] << " +/- " << sigmaCut_ << " * " << results[8] << endl
	   << endl ;
      cout << __LINE__ << "] upar <-> results comparison: " << endl 
           << setw(22) << setprecision(15)  
	   << upar.Value(0) << " <-> " << results[0] << endl 
	   << upar.Value(1) << " <-> " << results[1] << endl 
	   << upar.Value(2) << " <-> " << results[2] << endl 
	   << upar.Value(3) << " <-> " << results[3] << endl 
	   << upar.Value(4) << " <-> " << results[4] << endl 
	   << upar.Value(5) << " <-> " << results[5] << endl 
	   << upar.Value(6) << " <-> " << results[6] << endl 
	   << upar.Value(7) << " <-> " << results[7] << endl 
	   << upar.Value(8) << " <-> " << results[8] << endl 
	   << upar.Value(9) << " <-> " << results[9] << endl 
	   << endl ;
      ierr = migrad();
      if ( !ierr.IsValid() ) 
      {
        edm::LogWarning("PVFitter") << "3D beam spot fit failed in 2nd iteration" << std::endl;
        _WARNING_("3D beam spot fit failed in 2nd iteration") ;
        return false;
      }
      _RESULTS_("3D beam spot fit passed 2nd iteration") ;
      //
      // refit with correlations
      //
      migrad.Release(4);
      migrad.Release(6);
      migrad.Release(7);

      ierr = migrad();
      if ( !ierr.IsValid() ) 
      {
        edm::LogWarning("PVFitter") << "3D beam spot fit failed in 3rd iteration" << std::endl;
        _WARNING_("3D beam spot fit failed in 3rd iteration") ;
        return false;
      }
      _RESULTS_("3D beam spot fit passed 3rd iteration") ;
      // refit with floating scale factor
      //   minuitx.ReleaseParameter(9);
      //   minuitx.Minimize();

      //minuitx.PrintResults(0,0);

      fwidthX	 = results[3];
      fwidthY	 = results[5];
      fwidthZ	 = results[8];
      fwidthXerr = errors [3];
      fwidthYerr = errors [5];
      fwidthZerr = errors [8];

      // check errors on widths and sigmaZ for nan
      if ( edm::isNotFinite(fwidthXerr) || edm::isNotFinite(fwidthYerr) || edm::isNotFinite(fwidthZerr) ) 
      {
        edm::LogWarning("PVFitter") << "3D beam spot fit returns nan in 3rd iteration" << std::endl;
        _WARNING_("3D beam spot fit returns nan in 3rd iteration") ;
        return false;
      }

      reco::BeamSpot::CovarianceMatrix matrix;
      // need to get the full cov matrix
      matrix(0,0) = pow( errors[0], 2);
      matrix(1,1) = pow( errors[1], 2);
      matrix(2,2) = pow( errors[2], 2);
      matrix(3,3) = fwidthZerr * fwidthZerr;
      matrix(6,6) = fwidthXerr * fwidthXerr;

      fbeamspot = reco::BeamSpot( reco::BeamSpot::Point(results[0],
        						results[1],
        						results[2] ),
        			  fwidthZ,
        			  results[6], 
        			  results[7],
        			  fwidthX,
        			  matrix );
      fbeamspot.setBeamWidthX( fwidthX );
      fbeamspot.setBeamWidthY( fwidthY );
      fbeamspot.setType(reco::BeamSpot::Tracker);
#endif
  }

  _MSG_("3D beam spot fit succeded") ;
  return true; //FIXME: Need to add quality test for the fit results!
}

//==============================================================================
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


//==============================================================================
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
  for ( unsigned int i=0; i<pvStore_.size(); ++i ) 
  {
    if ( pvQuality(pvStore_[i])>dynamicQualityCut_ )  continue;
    if ( i!=iwrite )  pvStore_[iwrite] = pvStore_[i];
    ++iwrite;
  }
  pvStore_.resize(iwrite);
  edm::LogInfo("PVFitter") << "Reduced primary vertex store size to "
                           << pvStore_.size() << " ; new dynamic quality cut = "
                           << dynamicQualityCut_ << std::endl;

}

//==============================================================================
double
PVFitter::pvQuality (const reco::Vertex& pv) const
{
  //
  // determinant of the transverse part of the PV covariance matrix
  //
  return pv.covariance(0,0)*pv.covariance(1,1)-
    	 pv.covariance(0,1)*pv.covariance(0,1);
    
}

//==============================================================================
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

