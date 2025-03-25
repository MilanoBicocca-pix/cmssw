#include "FWCore/Framework/interface/one/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/Exception.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include <iostream> 

class BunchCrossingFilter : public edm::one::EDFilter<> {
  public:
    explicit BunchCrossingFilter(const edm::ParameterSet&);
    ~BunchCrossingFilter() = default;
  private:
    virtual bool filter(edm::Event&, const edm::EventSetup&)  override;

    std::vector<unsigned int> const bcrossings_ ;
    bool                      const verbose_    ;
};

BunchCrossingFilter::BunchCrossingFilter(const edm::ParameterSet& pset):
  bcrossings_ (pset.getParameter<std::vector<unsigned int>> ("bunchcrossings")),
  verbose_    (pset.getUntrackedParameter<bool>             ("verbose")       ){
  if (verbose_){
    for (auto bc : bcrossings_){
      std::cout << "request bunch-crossing: " << bc << std::endl;
    }
  }
}

bool BunchCrossingFilter::filter(edm::Event& event, const edm::EventSetup& setup){
  const int bunch = event.bunchCrossing();
  bool verdict = std::find(bcrossings_.begin(), bcrossings_.end(), bunch) != bcrossings_.end();
  if (verbose_){
    std::cout << "Event bunch crossing number: " << bunch;
    if (verdict){
      std::cout << " (accepted)" << std::endl;
    } else {
      std::cout << " (rejected)" << std::endl;
    }
  }
  return verdict;
}

DEFINE_FWK_MODULE(BunchCrossingFilter);
