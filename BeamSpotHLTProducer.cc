/**_________________________________________________________________
   class:   BeamSpotHLTProducer.h
   package: RecoVertex/BeamSpotProducer



 author: Simone Gennai INFN MIB


________________________________________________________________**/

#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerEvmReadoutRecord.h"
#include "CondFormats/BeamSpotObjects/interface/BeamSpotObjects.h"
#include "CondFormats/DataRecord/interface/BeamSpotTransientObjectsRcd.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/ESGetToken.h"

class BeamSpotHLTProducer : public edm::stream::EDProducer<> {
public:
  /// constructor
  explicit BeamSpotHLTProducer(const edm::ParameterSet& iConf);

  /// produce a beam spot class
  void produce(edm::Event& iEvent, const edm::EventSetup& iSetup) override;

  ///Fill descriptor
  static void fillDescriptions(edm::ConfigurationDescriptions& iDesc);
private:
  const edm::ESGetToken<BeamSpotObjects, BeamSpotTransientObjectsRcd> beamTransientToken_;
};

using namespace edm;

BeamSpotHLTProducer::BeamSpotHLTProducer(const ParameterSet& iconf)
    : beamTransientToken_(esConsumes<BeamSpotObjects, BeamSpotTransientObjectsRcd>()){
  produces<reco::BeamSpot>();
}

void BeamSpotHLTProducer::fillDescriptions(edm::ConfigurationDescriptions& iDesc) {
  edm::ParameterSetDescription ps;
  iDesc.addWithDefaultLabel(ps);
}

void BeamSpotHLTProducer::produce(Event& iEvent, const EventSetup& iSetup) {
  // product is a reco::BeamSpot object
  auto result = std::make_unique<reco::BeamSpot>();
  reco::BeamSpot aSpot;

  auto const& spotDB = iSetup.getData(beamTransientToken_);

  // translate from BeamSpotObjects to reco::BeamSpot
  reco::BeamSpot::Point apoint(spotDB.GetX(), spotDB.GetY(), spotDB.GetZ());

  reco::BeamSpot::CovarianceMatrix matrix;
  for (int i = 0; i < 7; ++i) {
    for (int j = 0; j < 7; ++j) {
      matrix(i, j) = spotDB.GetCovariance(i, j);
    }
  }

  // this assume beam width same in x and y
  aSpot = reco::BeamSpot(
      apoint, spotDB.GetSigmaZ(), spotDB.Getdxdz(), spotDB.Getdydz(), spotDB.GetBeamWidthX(), matrix);
      aSpot.setBeamWidthY(spotDB.GetBeamWidthY());
      aSpot.setEmittanceX(spotDB.GetEmittanceX());
      aSpot.setEmittanceY(spotDB.GetEmittanceY());
      aSpot.setbetaStar(spotDB.GetBetaStar());
      //aSpot.setType(reco::BeamSpot::Tracker); //What do we want to do here?
      aSpot.setType(spotDB.GetBeamType()); //What do we want to do here?
  
  *result = aSpot;

  iEvent.put(std::move(result));
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(BeamSpotHLTProducer);
