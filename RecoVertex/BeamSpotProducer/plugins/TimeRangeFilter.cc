#include "FWCore/Framework/interface/one/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/Exception.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include <iostream> 

class TimeRangeFilter : public edm::one::EDFilter<> {
  public:
    explicit TimeRangeFilter(const edm::ParameterSet&);
    ~TimeRangeFilter() = default;
  private:
    virtual bool filter(edm::Event&, const edm::EventSetup&)  override;

    std::vector<edm::ParameterSet>          const parameters_ ;
    bool                                    const verbose_    ;
    std::vector<std::pair<time_t, time_t>>        timeranges_ ;
};

TimeRangeFilter::TimeRangeFilter(const edm::ParameterSet& pset):
  parameters_ (pset.getParameter<std::vector<edm::ParameterSet>>("timeranges")),
  verbose_    (pset.getUntrackedParameter<bool>                 ("verbose")   ){
  for (auto par : parameters_){
    const time_t start  = static_cast<time_t>(par.getParameter<unsigned int>("start" ));
    const time_t end    = static_cast<time_t>(par.getParameter<unsigned int>("end"   ));
    timeranges_.push_back({start, end});
    if (start>end){
      throw cms::Exception("ConfigurationError") 
      << start << "," << end << " is not a valid timerange";
    }
    
    if (verbose_){
      std::cout << "request time range " << start << "," << end << std::endl;
    }
  }
}

bool TimeRangeFilter::filter(edm::Event& event, const edm::EventSetup& setup){
  const edm::TimeValue_t timestamp = event.time().value();
  const std::time_t time = timestamp >> 32;
  bool verdict = false;
  
  for (auto tr : timeranges_){
    verdict = verdict or (time>=tr.first and time<=tr.second);
  }

  if (verbose_){
    std::cout << "Event time stamp: " << time;
    if (verdict){
      std::cout << " (accepted)" << std::endl;
    } else {
      std::cout << " (rejected)" << std::endl;
    }
  }
  return verdict;
}

DEFINE_FWK_MODULE(TimeRangeFilter);
