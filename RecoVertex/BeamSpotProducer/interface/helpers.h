#ifndef HELPERS_H
#define HELPERS_H

/*
 Author: D. Menasce
 INFN Milano-Bicocca
*/

#include <iostream>
#include <sstream>
#include <iomanip>
#include <string>

#include "RecoVertex/BeamSpotProducer/interface/ANSIColors.h"

using namespace std ;

#define _L_  40
#define _S_  setw(5) 
#define _SS_ _S_ << "       "
#define _SP_ _S_ << endl << _SS_
//#define _OLDMINUIT_ 1

namespace H
{
 void                set(bool a) ;
 bool                get(void)   ;
 static stringstream ss_         ;
}

#define _MSG_(text) 	{										          \
        	    	 if(H::get()) { string p = __PRETTY_FUNCTION__ ; p = p.substr(0,_L_) ; cout << ACGreen 	  \
        	    	 << ACBold   << _S_	  << __LINE__	 << "]"    << ACPlain << " ["		  	  \
		    	 << ACYellow << setw(_L_) << p  	 << "..."  << ACPlain << "] "		  	  \
		    	 << endl     << _SS_      << ""          << text			          	  \
        	    	 << endl ; }									  	  \
        	    	}      

#define _HERE_()        {										  	  \
        	         if(H::get()) { string p = __PRETTY_FUNCTION__ ; p = p.substr(0,_L_) ;  cout << ACGreen	  \
		         << ACBold   << _S_	  << __LINE__	 << "]"    << ACPlain << " ["		  	  \
		         << ACYellow << setw(_L_) << p  	 << "..."  << ACPlain << "] "		  	  \
        	         << endl ; }									  	  \
        	        }

#define _WARNING_(text) {                            	  					    	  	  \
        		 if(H::get()) { string p = __PRETTY_FUNCTION__ ; p = p.substr(0,_L_) ;  cout << ACGreen   \
        		 << ACBold   << _S_       << __LINE__    << "]"    << ACPlain << " ["             	  \
			 << ACYellow << setw(_L_) << p  	 << "..."	      << ACPlain  << "] " 	  \
			 << endl     << _SS_      << ACRed       << ACBold            << "WARNING: "  	          \
			 << ACCyan   << _SS_      << ""          << text              << ACPlain 	          \
			 << endl ; }									  	  \
        		}        

#ifdef _OLDMINUIT_

#define _RESULTS_(text) {                                                                                         \
      			 cout << __LINE__ << "] " << __PRETTY_FUNCTION__ << "] " << text << endl ;		  \
      			 minuitx.PrintResults(3,0) ;                      					  \
      			 cout << __LINE__ << "] " << __PRETTY_FUNCTION__ << "] " << "Results (Old)" << endl ;	  \
      			 for(int i=0; i<minuitx.GetNumberTotalParameters(); ++i)				  \
      			 {											  \
      			  cout << __LINE__ << "] "								  \
			       << setw(3)  << i << ": " 							  \
			       << setw(7)									  \
			       << minuitx.GetParName(i) 							  \
			       << " "										  \
			       << setw(22) << setprecision(14)  						  \
			       << minuitx.GetParameter(i) << " +/- " << minuitx.GetParError(i) << endl ;	  \
      			 }											  \
      			 cout << __LINE__ << "] " << __PRETTY_FUNCTION__ << "] " << "Covariance (Old)" << endl ;  \
                         for(int i=0; i<minuitx.GetNumberFreeParameters(); ++i)                                   \
      			 {											  \
      			  cout << __LINE__ << "] " ;	                                                          \
                          for(int j=0; j<minuitx.GetNumberFreeParameters(); ++j)                                  \
      			  {											  \
      			   cout << setw(22) << setprecision(14)  						  \
			        << minuitx.GetCovarianceMatrixElement(i, j)  ;	                                  \
      			  }											  \
                          cout << endl ;                                                                          \
      			 }											  \
                        }											  

#define _LIMITS_()      {                                                                                         \
      			 cout << __LINE__ << "] " << __PRETTY_FUNCTION__ << "] New limits (Old)" << endl ;	  \
                     	 cout << __LINE__ << "] " << minuitx.GetParameter(0) << "-" << sigmaCut_ << "*"           \
			                          << minuitx.GetParameter(3) << endl ;                            \
                     	 cout << __LINE__ << "] " << minuitx.GetParameter(0) << "+" << sigmaCut_ << "*"           \
			                          << minuitx.GetParameter(3) << endl ;                            \
                     	 cout << __LINE__ << "] " << minuitx.GetParameter(1) << "-" << sigmaCut_ << "*"           \
			                          << minuitx.GetParameter(5) << endl ;                            \
                     	 cout << __LINE__ << "] " << minuitx.GetParameter(1) << "+" << sigmaCut_ << "*"           \
			                          << minuitx.GetParameter(5) << endl ;                            \
                     	 cout << __LINE__ << "] " << minuitx.GetParameter(2) << "-" << sigmaCut_ << "*"           \
			                          << minuitx.GetParameter(8) << endl ;                            \
                     	 cout << __LINE__ << "] " << minuitx.GetParameter(2) << "+" << sigmaCut_ << "*"           \
			                          << minuitx.GetParameter(8) << endl ;                            \
                        }
#else

#define _RESULTS_(text) {                                                                                         \
      			 cout << __LINE__ << "] " << __PRETTY_FUNCTION__ << "] " << text << endl ;		  \
      			 cout << ierr << endl;                   						  \
      			 results = ierr.UserParameters().Params() ;                                               \
      			 errors  = ierr.UserParameters().Errors() ;						  \
      			 cout << __LINE__ << "] " << __PRETTY_FUNCTION__ << "] " << "Results (New)" << endl ;	  \
      			 for(unsigned int i=0; i<results.size(); ++i)						  \
      			 {											  \
      			   cout << setw(3)  << i << ": " 							  \
			 	<< setw(7)									  \
			 	<< ierr.UserParameters().GetName(i) 						  \
			 	<< " "  									  \
			 	<< setw(22) << setprecision(14) 						  \
			 	<< results[i] << " +/- " << errors[i] << endl ; 				  \
      			 }											  \
      			 cout << __LINE__ << "] " << __PRETTY_FUNCTION__ << "] " << "Covariance (New)" << endl ;  \
      			 unsigned int size = migrad.VariableParameters() ;					  \
      			 for(unsigned int i=0; i<size; ++i)							  \
      			 {											  \
      			  cout << __LINE__ << "] " ;	                                                          \
      			  for(unsigned int j=0; j<size; ++j)							  \
      			  {											  \
			   cout << setw(22) << setprecision(14)                                                   \
			        << ierr.UserCovariance()(i,j) << " " ;					          \
      			  }											  \
      			  cout << endl ;									  \
      			 }											  \
                        }

#define _LIMITS_()      {                                                                                         \
      			 cout << __LINE__ << "] " << __PRETTY_FUNCTION__ << "] New limits (New)" << endl ;	  \
                     	 cout << __LINE__ << "] " << results(0) << "-" << sigmaCut_ << "*"	     		  \
			                          << results(3) << endl ;			     		  \
                     	 cout << __LINE__ << "] " << results(0) << "+" << sigmaCut_ << "*"	     		  \
			                          << results(3) << endl ;			     		  \
                     	 cout << __LINE__ << "] " << results(1) << "-" << sigmaCut_ << "*"	     		  \
			                          << results(5) << endl ;			     		  \
                     	 cout << __LINE__ << "] " << results(1) << "+" << sigmaCut_ << "*"	     		  \
			                          << results(5) << endl ;			     		  \
                     	 cout << __LINE__ << "] " << results(2) << "-" << sigmaCut_ << "*"	     		  \
			                          << results(8) << endl ;			     		  \
                     	 cout << __LINE__ << "] " << results(2) << "+" << sigmaCut_ << "*"	     		  \
			                          << results(8) << endl ;			     		  \
                        }
#endif

#endif // HELPERS_H
