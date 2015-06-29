#!/bin/tcsh -f
       setenv SCRAM_ARCH slc6_amd64_gcc491
       set W_DIR = "/afs/cern.ch/work/f/fiorendi/private/BeamSpot/CMSSW_7_4_4_patch1/src/RecoVertex/BeamSpotProducer/test/wdir"
       set CFG = "/afs/cern.ch/work/f/fiorendi/private/BeamSpot/CMSSW_7_4_4_patch1/src/RecoVertex/BeamSpotProducer/test/thecfg.py"
       cd $W_DIR
       eval `scramv1 runtime -csh`
       cmsenv
       cmsRun $CFG 
#        /afs/cern.ch/project/eos/installation/0.3.15/bin/eos.select cp RESFILE EOSDIR
#        rm RESFILE