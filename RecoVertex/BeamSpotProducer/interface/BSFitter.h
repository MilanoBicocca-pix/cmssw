#ifndef BeamSpotProducer_BSFitter_h
#define BeamSpotProducer_BSFitter_h

/**_________________________________________________________________
   class:   BSFitter.h
   package: RecoVertex/BeamSpotProducer
   


 author: Francisco Yumiceva, Fermilab (yumiceva@fnal.gov)


________________________________________________________________**/


// CMS
#include "RecoVertex/BeamSpotProducer/interface/BSpdfsFcn.h"
#include "RecoVertex/BeamSpotProducer/interface/BSTrkParameters.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"

// ROOT
#include "TMatrixD.h"
#include "TMath.h"
#include "Minuit2/VariableMetricMinimizer.h"
#include "TH1F.h"

// C++ standard
#include <vector>
#include <string>

class BSFitter 
{
  public:
    typedef std::vector <BSTrkParameters> BSTrk_TD_;
    typedef reco::BeamSpot::ResCovMatrix  RCM_TD_  ;

    	    	    BSFitter	     	 (void  					  );
     	    	    BSFitter	     	 (const std::vector< BSTrkParameters > & BSvector );

    virtual 	   ~BSFitter	     	 (void  					  );

    void    	    SetFitType       	 (std::string				 type	  ) { ffit_type     = type;  }
    void    	    SetFitVariable   	 (std::string				 name	  ) { ffit_variable = name;  }
    reco::BeamSpot  Fit 	     	 (void  					  );
    reco::BeamSpot  Fit 	     	 (double			       * inipar   );
    // Fit Z distribution with a gaussian
    reco::BeamSpot  Fit_z            	 (std::string				 type	  , 
                                     	  double			       * inipar   );
    reco::BeamSpot  Fit_z_chi2       	 (double			       * inipar   );
    reco::BeamSpot  Fit_z_likelihood 	 (double			       * inipar   );
   // Fit only d0-phi distribution with a chi2
    reco::BeamSpot  Fit_d0phi        	 (void  					  );
    void 	    SetMaximumZ      	 (double				 z	  ) { fMaxZ = z;	     }
    void 	    SetConvergence   	 (double				 val	  ) { fconvergence = val;    }
    void 	    SetMinimumNTrks  	 (int					 n	  ) { fminNtrks = n;	     }
    void 	    Setd0Cut_d0phi   	 (double				 d0cut    );
    void 	    SetChi2Cut_d0phi 	 (double				 chi2cut  );
    void 	    SetInputBeamWidth	 (double				 val	  ) { finputBeamWidth = val; }
    int             GetAcceptedTrks  	 (void  					  ) { return ftmprow;	     }
    void 	    d0phi_Init       	 (void  					  ) {
    					 						      ftmp.ResizeTo(4,1);
    					 						      ftmp.Zero()	;
    					 						      ftmprow = 0	;
    					 						      fnthite = 0	;
    					 						      goodfit = true	;
    					 						    }
    BSTrk_TD_       GetData          	 (void  					  ) { return fBSvector;      }
    reco::BeamSpot  Fit_ited0phi     	 (void  			                  );
    reco::BeamSpot  Fit_d_likelihood  	 (double 			       * inipar   );
    reco::BeamSpot  Fit_d_z_likelihood	 (double 			       * inipar, 
                                          double                               * error_par);
    reco::BeamSpot  Fit_dres_z_likelihood(double 			       * inipar   );
    double          scanPDF              (double                               * init_pars,
                                          int                                  & tracksFailed,
					  int                                    option   );
    double          GetMinimum           (void  					  ) { return ff_minimum;     }
    double          GetResPar0           (void  					  ) { return fresolution_c0; }
    double          GetResPar1           (void  					  ) { return fresolution_c1; }
    double          GetResPar0Err        (void  					  ) { return fres_c0_err;    }
    double          GetResPar1Err        (void  					  ) { return fres_c1_err;    }

    RCM_TD_         GetResMatrix         (void                                            ) { return fres_matrix;    }

    TH1F          * GetVzHisto           (void                                            ) { return h1z;            }
	
  private:

    ROOT::Minuit2::ModularFunctionMinimizer * theFitter      ;
  //BSzFcn                                  * theGausszFcn   ;
    BSpdfsFcn                               * thePDF         ;
    reco::BeamSpot::BeamType                  fbeamtype      ;
    static const int                          fdim = 7       ;
    double 				      fresolution_c0 ;
    double 				      fresolution_c1 ;
    double 				      fres_c0_err    ;
    double 				      fres_c1_err    ;
    double                                    ff_minimum     ;
    double 				      fd0cut  	     ;
    double 				      fchi2cut	     ;
    double 				      fMaxZ          ;
    double 				      fconvergence   ;
    double                                    finputBeamWidth;
    std::string 			      ffit_type      ;
    std::string 			      ffit_variable  ;
    std::string                               fpar_name[fdim];
    Double_t                                  fsqrt2pi       ;
    std::vector <BSTrkParameters> 	      fBSvector      ;
    std::vector <BSTrkParameters> 	      fBSvectorBW    ;
    reco::BeamSpot::ResCovMatrix              fres_matrix    ;
  //reco::BeamSpot                            fBSforCuts     ;
    TMatrixD 				      ftmp           ;
    bool     				      fapplyd0cut    ;
    bool     				      fapplychi2cut  ;
    bool     				      goodfit        ;
    int      				      ftmprow        ;
    int      				      fnthite        ;
    int      				      fminNtrks      ;
    TH1F     				    * h1z            ;
};

#endif

