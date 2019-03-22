**Submitting to CERN Condor system**

You can use the submit_RunFitOnTimeRange_forCondor.py script, which accepts in inputs different options:
```

  -c CFG, --cfg CFG     input cfg file (e.g., BeamFit_LumiBased_NoRefit_Template.py)
  -t, --test            do not submit to queue, for debugging
  -r TIMEFILE, --range TIMEFILE
                        time interval file
  -i INPUTFILES, --input INPUTFILES
                        input file list
  -d NEWFOLDER, --folder NEWFOLDER
                        out folder name
  -b BX, --bunch BX     selected bx, if -1 no selection
  --ilumi INITLS        first Lumi Section to be processed
  --flumi ENDLS         last Lumi Section to be processed
  
```

e.g., 
```
python submit_RunFitOnTimeRange_forCondor.py -r time_ranges_254992_scan8_imgY.txt -i filelist_254992_scanImgY.py --ilumi 154 --flumi 184 --runN 254992 -d scan8_imgY_bx51   -b 51


