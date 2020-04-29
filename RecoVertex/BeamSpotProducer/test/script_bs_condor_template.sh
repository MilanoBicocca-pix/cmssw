#!/bin/tcsh
# on hercules (MIB) use /bin/bash

# pushd $CMSSW_BASE/src
pushd /afs/cern.ch/work/f/fiorendi/private/BeamSpot/2018/CMSSW_10_1_7/src
eval `scramv1 runtime -csh` # on hercules (MIB) use `scramv1 runtime -sh`
popd
# mkdir tmp 
# setenv TMPDIR $PWD/tmp
# mkdir job
# cd job

# if running on hercules (MIB) uncomment these two lines:
#export KRB5CCNAME=/gwpool/users/brivio/krb5cc_`id -u brivio` # <- fix with appropriate username
#eosfusebind

cp /afs/cern.ch/work/f/fiorendi/private/BeamSpot/2018/CMSSW_10_1_7/src/RecoVertex/BeamSpotProducer/test/FOLDER/FILELIST . 
cmsRun /afs/cern.ch/work/f/fiorendi/private/BeamSpot/2018/CMSSW_10_1_7/src/RecoVertex/BeamSpotProducer/test/thecfg.py
# cp $CMSSW_BASE/src/RecoVertex/BeamSpotProducer/test/FOLDER/FILELIST . 
# cmsRun $CMSSW_BASE/src/RecoVertex/BeamSpotProducer/test/thecfg.py

cp -v BeamFit_LumiBased_alcareco_MINT_MAXT_Run*.txt $LS_SUBCWD
if [ $? -ne 0 ]; then
  echo 'ERROR: problem copying job directory back'
else
  echo 'job directory copy succeeded'
fi