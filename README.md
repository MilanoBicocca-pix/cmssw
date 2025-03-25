**Purpose of this branch**

Run the BS fit on custom ranges defined by given timestamps **using Run3 data/releases**.  
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

git checkout -b bsInTimeRange_Run3

git checkout mib/bsInTimeRange_Run3 DataFormats/BeamSpot/interface/BeamSpotExt.h
git checkout mib/bsInTimeRange_Run3 DataFormats/BeamSpot/src/BeamSpotExt.cc
git checkout mib/bsInTimeRange_Run3 DataFormats/BeamSpot/src/classes.h
git checkout mib/bsInTimeRange_Run3 DataFormats/BeamSpot/src/classes_def.xml
git checkout mib/bsInTimeRange_Run3 DataFormats/Math/src/classes.h
git checkout mib/bsInTimeRange_Run3 RecoVertex/BeamSpotProducer/interface/BSFitter.h
git checkout mib/bsInTimeRange_Run3 RecoVertex/BeamSpotProducer/interface/BeamFitter.h
git checkout mib/bsInTimeRange_Run3 RecoVertex/BeamSpotProducer/interface/BeamSpotExtWrite2Txt.h
git checkout mib/bsInTimeRange_Run3 RecoVertex/BeamSpotProducer/interface/PVFitter.h
git checkout mib/bsInTimeRange_Run3 RecoVertex/BeamSpotProducer/plugins/BeamSpotAnalyzer.cc
git checkout mib/bsInTimeRange_Run3 RecoVertex/BeamSpotProducer/python/d0_phi_analyzer_cff.py
git checkout mib/bsInTimeRange_Run3 RecoVertex/BeamSpotProducer/src/BSFitter.cc
git checkout mib/bsInTimeRange_Run3 RecoVertex/BeamSpotProducer/src/BeamFitter.cc
git checkout mib/bsInTimeRange_Run3 RecoVertex/BeamSpotProducer/src/FcnBeamSpotFitPV.cc
git checkout mib/bsInTimeRange_Run3 RecoVertex/BeamSpotProducer/src/PVFitter.cc
git checkout mib/bsInTimeRange_Run3 RecoVertex/BeamSpotProducer/test/BeamFit_LumiBased_NoRefit_Template.py
git checkout mib/bsInTimeRange_Run3 RecoVertex/BeamSpotProducer/test/BeamFit_LumiBased_PVRefit_Template.py
git checkout mib/bsInTimeRange_Run3 RecoVertex/BeamSpotProducer/test/README.md
git checkout mib/bsInTimeRange_Run3 RecoVertex/BeamSpotProducer/test/filelist_318984_scanX1_ZBAOD.py
git checkout mib/bsInTimeRange_Run3 RecoVertex/BeamSpotProducer/test/script_bs_condor_template.sh
git checkout mib/bsInTimeRange_Run3 RecoVertex/BeamSpotProducer/test/submit_RunFitOnLumiRange_forCondor.py
git checkout mib/bsInTimeRange_Run3 RecoVertex/BeamSpotProducer/test/submit_RunFitOnTimeRange_forCondor.py
git checkout mib/bsInTimeRange_Run3 RecoVertex/BeamSpotProducer/test/condor_bs_template.cfg
git checkout mib/bsInTimeRange_Run3 RecoVertex/BeamSpotProducer/test/time_ranges_274100_scans_1_2_3_4_5.txt
git checkout mib/bsInTimeRange_Run3 RecoVertex/BeamSpotProducer/test/datasets
git checkout mib/bsInTimeRange_Run3 RecoVertex/BeamSpotProducer/test/timestamps

scram b -j 10  
cd RecoVertex/BeamSpotProducer/test  
```
# van der Meer scans
Before submitting vdM jobs, it might be useful to recall datasets from tape and store them in a trustful storage:
```bash
rucio add-rule cms:/DATASETNAME/CAMPAIGN/TIER 1 YOUR_FAVOURITE_T2 --lifetime 7776000 --activity "User AutoApprove" --ask-approval --comment "BeamSpot computation for VdM Scans"
```
van der Meer scan fitting happens in three steps:
- **skimming**: event skimming is based on the time range and bunch crossing ID of the needed lumisections. The skimming is performed by the [BunchCrossingFilter.cc](RecoVertex/BeamSpotProducer/plugins/BunchCrossingFilter.cc) and [TimeRangeFilter.cc](RecoVertex/BeamSpotProducer/plugins/TimeRangeFilter.cc) plugins and a CMSSW configuration is in place ([EventSkimming_byTime_byBX.py](RecoVertex/BeamSpotProducer/test/EventSkimming_byTime_byBX.py)). A python script ([crab_skim_timerange_bx.py](RecoVertex/BeamSpotProducer/test/crab_skim_timerange_bx.py)) has been created in order to simplify the job scheduling. The script input is a LUMI .json file formatted similarly to [this one](https://gist.github.com/lguzzi/7276517bcf6d0a43f31818615ee2d4a5). The script must be run on the different input datasets and LUMI .json files needed. A command example is:
```bash
python3 crab_skim_timerange_bx.py --input 8381_11Nov22_114759_11Nov22_121408.json --dataset /SpecialHLTPhysics15/Run2022F-PromptReco-v1/AOD --bunchcrossing 282 822 2944 3123 3302 --subfolder BeamSpot --maxMemoryMB 4999
```
- **fitting**: fitting is done by the [BeamSpotAnalyzer.cc](RecoVertex/BeamSpotProducer/plugins/BeamSpotAnalyzer.cc) plugin, and a flexible python configuration is in place inside the [BeamSpotTools](https://github.com/MilanoBicocca-pix/BeamspotTools) repository ([BeamFit_custom_workflow.py](https://github.com/MilanoBicocca-pix/BeamspotTools/blob/master/test/BeamFit_custom_workflow.py)). The fitting must be run on the skimmed datasets for each input LUMI .json file. A command example is:
```bash
python3 submit_condor_timerange.py --lumijson 8381_11Nov22_114759_11Nov22_121408.json --bunchcrossing 208 282 548 822 1197 1376 2716 2944 3123 1081 1881 2653 2997 --globaltag 130X_dataRun3_Prompt_v3 --input /gwteras/cms/store/user/lguzzi/BeamSpot/SpecialHLTPhysics*/crab_SpecialHLTPhysics*_Run2023C-PromptReco-v*_AOD_VDM6/*/0000/*.root --jobdir VdM2023
```
This step will produce multiple .txt files, among which BSFit\_Fill<FILL\_NUMBER>\_Run<RUN\_NUMBER>\_<SCAN\_NAME>\_<BUNCH\_CROSSING>\_<TIME\_RANGE>.txt.txt contains the fit results. Single .txt files can then be merged together using *cat*, if need be.
- **formatting**: this step converts the output .txt files into a formatted tabular .txt file used by LUMI. DESCRIPTION TO BE ADDED.

A .txt result file can be quickly plotted using [this](https://github.com/lguzzi/BSPlotter) repo.
