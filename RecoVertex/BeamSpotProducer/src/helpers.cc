#include <sstream>
#include "RecoVertex/BeamSpotProducer/interface/helpers.h"

namespace H
{
 static bool _active = true ;
 void set(bool a)
 {
  _active = a ; 
 }
 bool get(void)
 {
  return _active ; 
 }
}
