#ifndef BeamSpotTreeData_H
#define BeamSpotTreeData_H

#include "RecoVertex/BeamSpotProducer/interface/BeamSpotFitPVData.h"
#include "RecoVertex/BeamSpotProducer/interface/helpers.h"
#include <sstream> 

class TTree;

class BeamSpotTreeData
{
 public:
                            BeamSpotTreeData(void                                   );
                           ~BeamSpotTreeData(                                       );
			   
  void  		    branch          (TTree		     * tree 	    );
  void  		    setBranchAddress(TTree		     * tree 	    );
  
  //Setters
  void  		    run 	    (unsigned int              run	    ) {run_	      = run;	      }
  void  		    lumi	    (unsigned int              lumi	    ) {lumi_	      = lumi;	      }
  void  		    bunchCrossing   (unsigned int              bunchCrossing) {bunchCrossing_ = bunchCrossing;}
  void  		    pvData	    (const BeamSpotFitPVData & pvData       ) {pvData_        = pvData;       }

  //Getters
  const unsigned int	  & getRun	    (void			    	    ) {return run_;		      }
  const unsigned int	  & getLumi	    (void			    	    ) {return lumi_;		      }
  const unsigned int	  & getBunchCrossing(void			    	    ) {return bunchCrossing_;	      }
  const BeamSpotFitPVData & getPvData	    (void			    	    ) {return pvData_;  	      }
  
 private:
  unsigned int      run_ 	  ;
  unsigned int      lumi_	  ;
  unsigned int      bunchCrossing_;
  BeamSpotFitPVData pvData_       ;
  std::stringstream ss_           ;
};

#endif
