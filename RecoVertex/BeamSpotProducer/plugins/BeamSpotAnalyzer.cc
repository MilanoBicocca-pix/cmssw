/**_________________________________________________________________
   class:   BeamSpotAnalyzer.cc
   package: RecoVertex/BeamSpotProducer



 author: Francisco Yumiceva, Fermilab (yumiceva@fnal.gov)
         Geng-Yuan Jeng, UC Riverside (Geng-Yuan.Jeng@cern.ch)


________________________________________________________________**/


// C++ standard
#include <string>
// CMS
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "RecoVertex/BeamSpotProducer/interface/BeamSpotAnalyzer.h"
#include "RecoVertex/BeamSpotProducer/interface/BSFitter.h"
#include "RecoVertex/BeamSpotProducer/interface/helpers.h"

#include "TMath.h"
//==============================================================================
BeamSpotAnalyzer::BeamSpotAnalyzer(const edm::ParameterSet& iConfig)
{
  edm::LogInfo("RecoVertex/BeamSpotAnalyzer") 
  	  << ACCyan << ACBold 
	  << "Initializing Beam Spot producer "
	  << ACPlain 
	  << "\n";
  _HERE_() ;
  
  // get parameter
  edm::ParameterSet _ps = iConfig.getParameter<edm::ParameterSet>("BSAnalyzerParameters");
  write2DB_       	= _ps.getParameter<bool>		 ("WriteToDB"	      	);
  runallfitters_  	= _ps.getParameter<bool>		 ("RunAllFitters"     	);
  runbeamwidthfit_      = _ps.getParameter<bool>		 ("RunBeamWidthFit"   	);
  fitNLumi_       	= _ps.getUntrackedParameter<int>	 ("fitEveryNLumi"  ,-1	);
  resetFitNLumi_  	= _ps.getUntrackedParameter<int>	 ("resetEveryNLumi",-1	);

  theBeamFitter = new BeamFitter(iConfig, consumesCollector());
  theBeamFitter->resetTrkVector();
  theBeamFitter->resetLSRange  ();
  theBeamFitter->resetCutFlow  ();
  theBeamFitter->resetRefTime  ();
  theBeamFitter->resetPVFitter ();

  ftotalevents       = countLumi_ = previousLumi_      = previousRun_    =  0;
  ftmprun0           = ftmprun    = beginLumiOfBSFit_  = endLumiOfBSFit_ = -1;
  Org_resetFitNLumi_ = resetFitNLumi_;
}

//==============================================================================
BeamSpotAnalyzer::~BeamSpotAnalyzer()
{
  delete theBeamFitter;
}

//==============================================================================
void BeamSpotAnalyzer::analyze(const edm::Event      & iEvent, 
                               const edm::EventSetup & iSetup)
{
  ftotalevents++;
  theBeamFitter->readEvent(iEvent);
  ftmprun = iEvent.id().run();
}

//==============================================================================
void BeamSpotAnalyzer::beginJob()
{
  _HERE_() ;
}

//==============================================================================
void BeamSpotAnalyzer::beginLuminosityBlock(const edm::LuminosityBlock & lumiSeg,
					    const edm::EventSetup      & context) 
{
  _HERE_() ;
  const edm::TimeValue_t fbegintimestamp = lumiSeg.beginTime().value();
  const std::time_t	 ftmptime	 = fbegintimestamp >> 32;

  if ( countLumi_ == 0 || (resetFitNLumi_ > 0 && countLumi_%resetFitNLumi_ == 0) ) 
  {
      ftmprun0          = lumiSeg.run();
      ftmprun           = ftmprun0;
      beginLumiOfBSFit_ = lumiSeg.luminosityBlock();
      refBStime[0]      = ftmptime;
  }

  countLumi_++;
  //std::cout << "Lumi # " << countLumi_ << std::endl;
  if ( ftmprun == previousRun_ ) 
  {
    if ( (previousLumi_ + 1) != int(lumiSeg.luminosityBlock()) )
      edm::LogWarning("BeamSpotAnalyzer") << "LUMI SECTIONS ARE NOT SORTED!";
  }
}

//==============================================================================
void BeamSpotAnalyzer::endLuminosityBlock(const edm::LuminosityBlock & lumiSeg,
					  const edm::EventSetup      & iSetup) 
{
  _HERE_() ;
  //LogDebug("BeamSpotAnalyzer") <<
  ss_.str("") ;
  ss_ << "For lumis "
      << beginLumiOfBSFit_ 
      << " - " 
      << endLumiOfBSFit_ 
      << _SP_ 
      << "number of selected tracks = " 
      << theBeamFitter->getNTracks() 
      << _SP_ 
      << "number of selected PVs = " 
      << theBeamFitter->getNPVs() ;
  _MSG_(ss_.str()) ;

  //std::cout << "number of selected PVs per bx: " << std::endl;
  //theBeamFitter->getNPVsperBX();

  const edm::TimeValue_t fendtimestamp = lumiSeg.endTime().value();
  const std::time_t	 fendtime      = fendtimestamp >> 32;
  refBStime[1]  		       = fendtime;

  endLumiOfBSFit_ = lumiSeg.luminosityBlock();
  previousLumi_   = endLumiOfBSFit_;

  if (fitNLumi_ == -1 && resetFitNLumi_       == -1 ) return;

  if (fitNLumi_ >   0 && countLumi_%fitNLumi_ !=  0 ) return;

  theBeamFitter->setFitLSRange(beginLumiOfBSFit_,endLumiOfBSFit_);
  theBeamFitter->setRefTime   (refBStime[0]	,refBStime[1]	);
  theBeamFitter->setRun       (ftmprun0 			);

  std::pair<int,int> LSRange = theBeamFitter->getFitLSRange();

  reco::BeamSpot bs ;
  if (theBeamFitter->runPVandTrkFitter())
  {
    bs = theBeamFitter->getBeamSpot();
    ss_.str(""); 
    ss_ << ACCyan 
  	<< ACBold
        << "[BeamFitter] fit succeeded." 
        << ACPlain 
	<< _SP_
        << ACRed 
  	<< ACBold 
        << "------ RESULTS OF DEFAULT FIT -------" 
        << ACPlain 
        << "For runs: " 
	<< _SP_
      	<< ftmprun0 
      	<< " - " 
      	<< ftmprun 
      	<< _SP_  
      	<< "for lumi blocks : " 
      	<< LSRange.first 
      	<< " - " 
      	<< LSRange.second 
      	<< _SP_ 
      	<< "lumi counter # " 
      	<< countLumi_ ;
    _MSG_(ss_.str()) ;
  }
  else 
  { // Fill in empty beam spot if beamfit fails
    bs.setType(reco::BeamSpot::Fake);
    ss_.str(""); 
    ss_ << ACRed 
  	<< ACBold 
        << "[BeamFitter] fit failed"  
        << ACPlain 
	<< _SP_ 
        << "Empty Beam spot fit" ;
        << "For runs: " 
	<< _SP_
      	<< ftmprun0 
      	<< " - " 
      	<< ftmprun 
      	<< _SP_  
      	<< "for lumi blocks : " 
      	<< LSRange.first 
      	<< " - " 
      	<< LSRange.second 
      	<< _SP_ 
      	<< "lumi counter # " 
      	<< countLumi_ ;
    _MSG_(ss_.str()) ;
    //accumulate more events
    // dissable this for the moment
    //resetFitNLumi_ += 1;
    //std::cout << "reset fitNLumi " << resetFitNLumi_ << std::endl;
  }

  if (resetFitNLumi_ > 0 && countLumi_%resetFitNLumi_ == 0) 
  {
    std::vector<BSTrkParameters> theBSvector = theBeamFitter->getBSvector();
    ss_.str(""); 
    ss_ << "Total number of tracks accumulated = " 
        << theBSvector.size() 
	<< _SP_ 
        << "Reset track collection for beam fit";
    _MSG_(ss_.str()) ;
    theBeamFitter->resetTrkVector();
    theBeamFitter->resetLSRange();
    theBeamFitter->resetCutFlow();
    theBeamFitter->resetRefTime();
    theBeamFitter->resetPVFitter();
    countLumi_=0;
    // reset counter to orginal
    resetFitNLumi_ = Org_resetFitNLumi_;
  }
}

//==============================================================================
void BeamSpotAnalyzer::endJob() 
{
  _HERE_() ;
  ss_.str(""); 
  ss_ << "--------------------------------------------------"
      << _SP_
      << "Total number of events processed: " 
      << ftotalevents
      << _SP_
      << "--------------------------------------------------" 
      << endl ; 
  _MSG_(ss_.str()) ;

  if ( fitNLumi_ == -1 && resetFitNLumi_ == -1 ) 
  {
    if(theBeamFitter->runPVandTrkFitter())
    {
      reco::BeamSpot beam_default = theBeamFitter->getBeamSpot();
      std::pair<int,int> LSRange  = theBeamFitter->getFitLSRange();

      ss_.str(""); 
      ss_ << "RESULTS OF DEFAULT FIT: "                                           
          << _SP_
      	  << " for runs 	 :  " 
	  << ftmprun0      
	  << " - " 
	  << ftmprun	  
          << _SP_
      	  << " for lumi blocks   :  " 
	  << LSRange.first 
	  << " - " 
	  << LSRange.second 
          << _SP_
      	  << " for lumi counter #:  " 
	  << countLumi_				  
          << _SP_
      	  << " Beam default	 :  " 
	  << beam_default ; 
      _MSG_(ss_.str()) ;

      if (write2DB_) 
      {
    	ss_.str(""); ss_ << "----------- Writing results to DB... -------------" ; _MSG_(ss_.str()) ;
    	theBeamFitter->write2DB();
      }

      if (runallfitters_) 
      {
    	theBeamFitter->runAllFitter();
      }
    }
    if ((runbeamwidthfit_))
    {
      theBeamFitter->runBeamWidthFitter();
      reco::BeamSpot beam_width = theBeamFitter->getBeamWidth();
      ss_.str(""); ss_ << " Beam beam width: " << beam_width ; _MSG_(ss_.str()) ;
    }
    else 
    {
     ss_.str(""); ss_ << "[BeamSpotAnalyzer] beamfit fails !!!" ; _MSG_(ss_.str()) ;
    }
  }

  ss_.str(""); ss_ << "[BeamSpotAnalyzer] Job done" ; _MSG_(ss_.str()) ;
}

//define this as a plug-in
DEFINE_FWK_MODULE(BeamSpotAnalyzer);
