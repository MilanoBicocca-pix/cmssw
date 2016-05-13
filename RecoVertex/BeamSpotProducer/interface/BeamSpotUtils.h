#ifndef __BEAMSPOTUTILS_H__
#define __BEAMSPOTUTILS_H__

#include <iostream>

using namespace std; 

#define CO(s1,s2) cout << __LINE__            << "] ["  \
                       << __PRETTY_FUNCTION__ << "] "   \
		       << s1                  << " "    \
		       << s2                  << endl ;

#endif
