**Purpose of this branch**

Run the BS fit on custom ranges defined by given timestamps.  
Useful for, e.g., determine the BS parameters during the scan steps in VdM scans.  

In addition, these improvements are included:
- uncertainty on sigmaY is saved and printed out
- value and uncertainty of dxdy are saved and printed out 
- the results of the pure 3D fit to the PVs (values and full covariance matrix) are also saved and printed
- the number of PVs used in the 3D fit is also saved and printed
- the final value of the likelihood returned by minuit is also saved and printed





**How to setup this branch**  

```
cmsrel CMSSW_X_X_X  
cd CMSSW_X_X_X/src
git cms-addpkg RecoVertex/BeamSpotProducer
git cms-addpkg DataFormats/Math
git cms-addpkg DataFormats/BeamSpot

git remote add mib git@github.com:MilanoBicocca-pix/cmssw.git
git fetch mib

git checkout -b bsInTimeRange

git checkout mib/bsInTimeRange DataFormats/BeamSpot/interface/BeamSpotExt.h
git checkout mib/bsInTimeRange DataFormats/BeamSpot/src/BeamSpotExt.cc
git checkout mib/bsInTimeRange DataFormats/BeamSpot/src/classes.h
git checkout mib/bsInTimeRange DataFormats/BeamSpot/src/classes_def.xml
git checkout mib/bsInTimeRange DataFormats/Math/src/classes.h
git checkout mib/bsInTimeRange RecoVertex/BeamSpotProducer/interface/BSFitter.h
git checkout mib/bsInTimeRange RecoVertex/BeamSpotProducer/interface/BeamFitter.h
git checkout mib/bsInTimeRange RecoVertex/BeamSpotProducer/interface/BeamSpotExtWrite2Txt.h
git checkout mib/bsInTimeRange RecoVertex/BeamSpotProducer/interface/PVFitter.h
git checkout mib/bsInTimeRange RecoVertex/BeamSpotProducer/plugins/BeamSpotAnalyzer.cc
git checkout mib/bsInTimeRange RecoVertex/BeamSpotProducer/python/d0_phi_analyzer_cff.py
git checkout mib/bsInTimeRange RecoVertex/BeamSpotProducer/src/BSFitter.cc
git checkout mib/bsInTimeRange RecoVertex/BeamSpotProducer/src/BeamFitter.cc
git checkout mib/bsInTimeRange RecoVertex/BeamSpotProducer/src/FcnBeamSpotFitPV.cc
git checkout mib/bsInTimeRange RecoVertex/BeamSpotProducer/src/PVFitter.cc
git checkout mib/bsInTimeRange RecoVertex/BeamSpotProducer/test/BeamFit_LumiBased_NoRefit_Template.py
git checkout mib/bsInTimeRange RecoVertex/BeamSpotProducer/test/BeamFit_LumiBased_PVRefit_Template.py
git checkout mib/bsInTimeRange RecoVertex/BeamSpotProducer/test/README.md
git checkout mib/bsInTimeRange RecoVertex/BeamSpotProducer/test/filelist_318984_scanX1_ZBAOD.py
git checkout mib/bsInTimeRange RecoVertex/BeamSpotProducer/test/script_bs_condor_template.sh
git checkout mib/bsInTimeRange RecoVertex/BeamSpotProducer/test/submit_RunFitOnLumiRange_forCondor.py
git checkout mib/bsInTimeRange RecoVertex/BeamSpotProducer/test/submit_RunFitOnTimeRange_forCondor.py
git checkout mib/bsInTimeRange RecoVertex/BeamSpotProducer/test/condor_bs_template.cfg
git checkout mib/bsInTimeRange RecoVertex/BeamSpotProducer/test/time_ranges_274100_scans_1_2_3_4_5.txt
git checkout mib/bsInTimeRange RecoVertex/BeamSpotProducer/test/datasets
git checkout mib/bsInTimeRange RecoVertex/BeamSpotProducer/test/timestamps

scram b -j 10  
cd RecoVertex/BeamSpotProducer/test  
```

In order to submit jobs to the CERN HTCondor system you can use the script `submit_RunFitOnTimeRange_forCondor.py`.
You can see all the available options and needed inputs by doing 
```
python submit_RunFitOnTimeRange_forCondor.py --help
```






