#ifndef BeamSpotTreeData_H
#define BeamSpotTreeData_H

#include "RecoVertex/BeamSpotProducer/interface/BeamSpotFitPVData.h"

class TTree;


class BeamSpotTreeData{
 public:
  BeamSpotTreeData();
  ~BeamSpotTreeData();
  void branch(TTree* tree);
  void setBranchAddress(TTree* tree);
  
  //Setters
  void run          (unsigned int      run)          {run_=run;}
  void lumi         (unsigned int      lumi)         {lumi_=lumi;}
  void bunchCrossing(unsigned int      bunchCrossing){bunchCrossing_=bunchCrossing;}
  void pvData       (const BeamSpotFitPVData &pvData)       {pvData_=pvData;}
  //void ntracks_per_vtx (unsigned int   ntracks_per_vtx) {ntracks_per_vtx_=ntracks_per_vtx;}
  //void sumpt_per_vtx (double sumpt_per_vtx) {sumpt_per_vtx_=sumpt_per_vtx;}

  //Getters
  const unsigned int&      getRun          (void)  {return run_;}
  const unsigned int&      getLumi         (void)  {return lumi_;}
  const unsigned int&      getBunchCrossing(void)  {return bunchCrossing_;}
  const BeamSpotFitPVData& getPvData       (void)  {return pvData_;}
  //const unsigned int&      getNtracks_per_vtx(void){return ntracks_per_vtx_;}
  //double&                  getSumpt_per_vtx(void)  {return sumpt_per_vtx_;}
  
 private:
  unsigned int      run_;
  unsigned int      lumi_;
  unsigned int      bunchCrossing_;
  //unsigned int      ntracks_per_vtx_;
  //double            sumpt_per_vtx_;
  BeamSpotFitPVData pvData_;
};

#endif
