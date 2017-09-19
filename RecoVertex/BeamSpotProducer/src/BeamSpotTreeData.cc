#include "RecoVertex/BeamSpotProducer/interface/BeamSpotTreeData.h"
#include <TTree.h>


BeamSpotTreeData::BeamSpotTreeData(){}
BeamSpotTreeData::~BeamSpotTreeData(){}


//--------------------------------------------------------------------------------------------------
void BeamSpotTreeData::branch(TTree* tree){
  tree->Branch("run"	      , &run_	       , "run/i");
  tree->Branch("lumi"	      , &lumi_	       , "lumi/i");
  tree->Branch("bunchCrossing", &bunchCrossing_, "bunchCrossing/i");
  //tree->Branch("ntracks_per_vtx", &ntracks_per_vtx_, "ntracks_per_vtx/i");
  //tree->Branch("sumpt_per_vtx", &sumpt_per_vtx_, "sumpt_per_vtx_/D");
  tree->Branch("pvData"	      , &pvData_       , "bunchCrossing:position[3]:posError[3]:posCorr[3]:ntrks_vtx:sumpt_vtx:nPV_vtx/F");
}

//--------------------------------------------------------------------------------------------------
void BeamSpotTreeData::setBranchAddress(TTree* tree){
  tree->SetBranchAddress("run"	        , &run_	         );
  tree->SetBranchAddress("lumi"	        , &lumi_	 );
  tree->SetBranchAddress("bunchCrossing", &bunchCrossing_);
  //tree->SetBranchAddress("ntracks_per_vtx", &ntracks_per_vtx_);
  //tree->SetBranchAddress("sumpt_per_vtx", &sumpt_per_vtx_);
  tree->SetBranchAddress("pvData"	, &pvData_       );
}
