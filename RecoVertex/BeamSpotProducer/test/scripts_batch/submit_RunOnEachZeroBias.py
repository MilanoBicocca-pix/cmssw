import os
import datetime
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument("-Q"  , "--queue"     , dest = "queue"    ,  help = "choose queue. Available 1nh 8nh 1nd 2nd 1nw 2nw. Default is 1nd" , default = '1nd'   )
parser.add_argument("-R"  , "--run"       , dest = "run"      ,  help = "choose run number "                                              , default = ''      )
parser.add_argument("-c"  , "--cfg"       , dest = "cfg"      ,  help = "input cfg file"                                                  , default =  "../analyze_d0_phi_cfg_firstData_promptReco_template.py")
parser.add_argument("-f"  , "--files"     , dest = "files"    ,  help = "input file list"                                                 , default =  "fileList_run247710.py"   )

options = parser.parse_args()

if not options.run:   
  parser.error('Run number not given')
therun        = options.run

# create a new folder 
newFolder = 'rerunBS_{RUN}'.format(RUN=therun)
if os.path.exists('{FOLDER}'.format(FOLDER=newFolder)):
  print 'warning: the directory {FOLDER} already exists. \n   exiting...'.format(FOLDER=newFolder)
  exit()
else: 
  os.system('mkdir {FOLDER}'.format(FOLDER=newFolder))
os.system('cp {LIST} {FOLDER}'.format(LIST=options.files, FOLDER=newFolder))
os.chdir(os.getcwd() +'/' + newFolder)


# open the fileList and eval number of dataset to analyze -> njobs
execfile(options.files)
list_toprocess = []
for k, v in globals().items():  
  if k == 'args' or k == 'list_toprocess':
    continue
  if isinstance(v, list):
    print 'dataset names: ', k
    list_toprocess.append(k)
 

njobs = len(list_toprocess)
print 'njobs: ', njobs

for j in range(njobs): 

  # write the .cfg file
  f   = open(options.cfg)
  f1  = open('{M}_{NUM}.py'.format(M=options.cfg.replace("../","").replace(".py","").replace("","").rstrip(), NUM=str(j)), "w")
  for line in f:
    newline = None
    newfile = None
    if 'thefilefile' in line:
        line = line.replace('thefilefile', str(options.files.replace(".py",""))).rstrip()
        print >> f1, line
    elif 'thefilelist' in line:
        line = line.replace('thefilelist', str(list_toprocess[j])).rstrip()
        print >> f1, line
    elif 'beamspot_firstData_runXXX_byLumi_ZeroBiasXX.' in line:
        line = line.replace('beamspot_firstData_runXXX_byLumi_ZeroBiasXX.', 'beamspot_firstData_run{RUN}_byLumi_ZeroBias{N}.'.format(RUN=therun, N=j))
        print >> f1, line 
    else:
      print >> f1,line.rstrip() 

  # now write the .sh file
  sh   = open("../script_template.sh")
  shName = "script_{NUM}.sh".format(NUM=str(j))
  sh1  = open(shName,"w")
  os.system("chmod +x {SH}".format(SH=shName)) 
  for shline in sh:
      mycfg = None
      if '/wdir'  in shline:
          shline = shline.replace('/wdir', '/{FOLDER}'.format(FOLDER=newFolder)).rstrip()
          print >> sh1, shline.rstrip()
      elif 'thecfg.py'  in shline:
          shline = shline.replace('thecfg.py', '{FOLDER}/{M}_{NUM}.py'.format(FOLDER=newFolder, M=options.cfg.replace(".py","").replace("../","").rstrip(), NUM=str(j))).rstrip()
          print >> sh1, shline.rstrip()
      else: 
        print >> sh1, shline.rstrip()

#   if j != 0:
#   os.system("bsub -q {QUEUE} {SH}".format(QUEUE=options.queue, SH=shName))    
