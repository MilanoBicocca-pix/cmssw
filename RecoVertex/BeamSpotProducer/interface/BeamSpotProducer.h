#ifndef BeamSpotProducer_BeamSpotProducer_h
#define BeamSpotProducer_BeamSpotProducer_h

/**_________________________________________________________________
   class:   BeamSpotProducer.h
   package: RecoVertex/BeamSpotProducer

 author: Francisco Yumiceva, Fermilab (yumiceva@fnal.gov)
________________________________________________________________**/

#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

class BeamSpotProducer: public edm::stream::EDProducer<> 
{
  public:
    typedef std::vector<edm::ParameterSet> Parameters;

    explicit      BeamSpotProducer(const edm::ParameterSet & iConf );
                 ~BeamSpotProducer(void                            );

    /// produce a beam spot class
    virtual void  produce         (      edm::Event        & iEvent, 
                                   const edm::EventSetup   & iSetup);

  private:
	
};

#endif
