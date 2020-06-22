#ifndef DQM_BeamMonitor_AlcaBeamMonitor_h
#define DQM_BeamMonitor_AlcaBeamMonitor_h

/** \class AlcaBeamMonitor
 * *
 *  \author  Lorenzo Uplegger/FNAL
 *   
 */
// C++
#include <map>
#include <vector>
#include <string>
// CMS
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DQMServices/Core/interface/DQMStore.h"
#include "DataFormats/Provenance/interface/LuminosityBlockID.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include <DQMServices/Core/interface/DQMOneEDAnalyzer.h>

class BeamFitter;
class PVFitter;
namespace {
  struct Cache {
    Cache() : value(0) {}
    //Using mutable since we want to update the value.
    mutable std::atomic<unsigned int> value;
  };

}  //end anonymous namespace
class AlcaBeamMonitor : public DQMOneEDAnalyzer<edm::LuminosityBlockCache<Cache>> {
public:
  AlcaBeamMonitor(const edm::ParameterSet&);
  ~AlcaBeamMonitor() override;

protected:
  void bookHistograms(DQMStore::IBooker&, edm::Run const&, edm::EventSetup const&) override;
  void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) override;
  std::shared_ptr<Cache> globalBeginLuminosityBlock(const edm::LuminosityBlock& iLumi, const edm::EventSetup& iSetup) const override;
  void globalEndLuminosityBlock(const edm::LuminosityBlock& iLumi, const edm::EventSetup& iSetup) override;

private:
  //Typedefs
  //                BF,BS...
  typedef std::map<std::string, reco::BeamSpot> BeamSpotContainer;
  //                x,y,z,sigmax(y,z)... [run,lumi]          Histo name
  typedef std::map<std::string, std::map<std::string, std::map<std::string, MonitorElement*> > > HistosContainer;
  //                x,y,z,sigmax(y,z)... [run,lumi]          Histo name
  typedef std::map<std::string, std::map<std::string, std::map<std::string, int> > > PositionContainer;

  //Parameters
  edm::ParameterSet parameters_;
  std::string monitorName_;
  edm::EDGetTokenT<reco::VertexCollection> primaryVertexLabel_;
  edm::EDGetTokenT<reco::TrackCollection> trackLabel_;
  edm::EDGetTokenT<reco::BeamSpot> scalerLabel_;
  edm::InputTag beamSpotLabel_;

  //Service variables
  int numberOfValuesToSave_;
  BeamFitter* theBeamFitter_;
  PVFitter* thePVFitter_;

  // MonitorElements:
  MonitorElement* hD0Phi0_;
  MonitorElement* hDxyBS_;
  MonitorElement* theValuesContainer_;
  mutable bool testLumi = false;
  //Containers
  mutable BeamSpotContainer beamSpotsMap_;
  HistosContainer histosMap_;
  PositionContainer positionsMap_;
  std::vector<std::string> varNamesV_;                            //x,y,z,sigmax(y,z)
  std::multimap<std::string, std::string> histoByCategoryNames_;  //run, lumi
  mutable std::vector<reco::VertexCollection> vertices_;
};

#endif
