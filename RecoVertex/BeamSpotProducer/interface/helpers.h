#ifndef HELPERS_H
#define HELPERS_H

/*
 Author: D. Menasce
 INFN Milano-Bicocca
*/

#include <iostream>
#include <iomanip>
#include <string>

#include "RecoVertex/BeamSpotProducer/interface/ANSIColors.h"

using namespace std ;

#define _L_  40
#define _S_  setw(5) 
#define _SS_ _S_ << "       "
#define _SP_ _S_ << endl << _SS_

#define _MSG_(text) 	{										  \
        	    	 string p = __PRETTY_FUNCTION__ ; p = p.substr(0,_L_) ; cout << ACGreen 	  \
        	    	 << ACBold   << _S_	  << __LINE__	 << "]"    << ACPlain << " ["		  \
		    	 << ACYellow << setw(_L_) << p  	 << "..."  << ACPlain << "] "		  \
		    	 << "V"      << endl	  << _SS_        << ""     << text			  \
        	    	 << endl ;									  \
        	    	}
        

#define _HERE_()        {										  \
        	         string p = __PRETTY_FUNCTION__ ; p = p.substr(0,_L_) ;  cout << ACGreen	  \
		         << ACBold   << _S_	  << __LINE__	 << "]"    << ACPlain << " ["		  \
		         << ACYellow << setw(_L_) << p  	 << "..."  << ACPlain << "] "		  \
        	         << endl ;									  \
        	        }

#define _WARNING_(text) {                            	  					    	  \
        		 string p = __PRETTY_FUNCTION__ ; p = p.substr(0,_L_) ;  cout << ACGreen          \
        		 << ACBold   << _S_       << __LINE__    << "]"    << ACPlain << " ["             \
			 << ACYellow << setw(_L_) << p  	 << "..."	      << ACPlain  << "] " \
			 << ACRed    << ACBold    << "WARNING: " << ACCyan                                \
			 << _SS_     << ""        << text        << ACPlain 	                          \
			 << endl ;									  \
        		}
        

#endif // HELPERS_H
