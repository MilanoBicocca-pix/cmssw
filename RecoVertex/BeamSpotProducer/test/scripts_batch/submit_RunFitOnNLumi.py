from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-Q"  , "--queue"     , dest = "queue"    ,  help = "choose queue. Available 1nh 8nh 1nd 2nd 1nw 2nw. Default is 1nd" , default = '1nd'   )
parser.add_argument("-R"  , "--run"       , dest = "run"      ,  help = "choose run number "                                              , default = ''      )
parser.add_argument("-i"  , "--initlumi"  , dest = "initlumi" ,  help = "choose initial lumi"                                             , default = ''      )
parser.add_argument("-e"  , "--endlumi"   , dest = "endlumi"  ,  help = "choose final lumi"                                               , default = ''      )
parser.add_argument("-r"  , "--lumirange" , dest = "lumirange",  help = "choose range lumi"                                               , default = ''      )
parser.add_argument("-c"  , "--cfg"       , dest = "cfg"      ,  help = "input cfg file"                                                  , default = "../analyze_d0_phi_cfg_promptReco_Xlumi_template.py"             )
parser.add_argument("-f"  , "--files"     , dest = "files"    ,  help = "input file list"                                                 , default =  "fileList_run247710.py"   )

options = parser.parse_args()

if not options.run:   
  parser.error('Run number not given')
if not (options.initlumi and options.endlumi):   
  parser.error('Initial and final lumi not given, please select them with -i and -e')
if not (options.lumirange):   
  parser.error('Lumi interval not defined, please do -r RANGE')


import os
import datetime

therun        = options.run
theinitlumi   = options.initlumi
theendlumi    = options.endlumi
thelumirange  = options.lumirange

# create a new folder 
newFolder = 'rerunBS_{RUN}'.format(RUN=therun)
if os.path.exists('{FOLDER}'.format(FOLDER=newFolder)):
  print 'warning: the directory {FOLDER} already exists. \n   exiting...'.format(FOLDER=newFolder)
  exit()
else: 
  os.system('mkdir {FOLDER}'.format(FOLDER=newFolder))
os.system('cp {LIST} {FOLDER}'.format(LIST=options.files, FOLDER=newFolder))
os.chdir(os.getcwd() +'/' + newFolder)


# eval the number of jobs to be submitted
njobs = (int(theendlumi) - int(theinitlumi)) /  int(thelumirange) 
print 'njobs: ', njobs

for j in range(njobs): 

  thisinitlumi = j*int(thelumirange) + int(theinitlumi) 
  thisfinlumi  = thisinitlumi + int(thelumirange) - 1

  therangestring = therun + ':' + str(thisinitlumi) + '-' + therun + ':' + str(thisfinlumi) 
  print 'job ' + str(j) + ' will cover lumi range ' + therangestring
  if j == int(len(range(njobs))) -1:
    print 'warning! still missing lumi from ' + str(thisfinlumi + 1)  + ' to ' + theendlumi  

  # write the .cfg file
  f   = open(options.cfg)
  f1  = open('{M}_{NUM}.py'.format(M=options.cfg.replace(".py","").replace("../","").rstrip(), NUM=str(j)), "w")
  for line in f:
    newline = None
    newfile = None
    if 'myLumiRange' in line:
        line = line.replace('myLumiRange', '"' + therangestring.rstrip() + '"').rstrip()
        print >> f1, line
    elif 'beamspot_firstData_runXX_byLumi_all_template.' in line:
        line = line.replace('beamspot_firstData_runXX_byLumi_all_template.', 'beamspot_firstData_run{RUN}_byLumi_all_lumi{IN}_{END}.'.format(RUN=therun, IN=thisinitlumi, END=str(thisfinlumi))).rstrip()
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
          shline = shline.replace('thecfg.py', '{FOLDER}/{M}_{NUM}.py'.format(M=options.cfg.replace("../","").replace(".py","").rstrip(), NUM=str(j), FOLDER=newFolder)).rstrip()
          print >> sh1, shline.rstrip()
      else: 
        print >> sh1, shline.rstrip()

  # submit to the queue
  os.system("bsub -q {QUEUE} {SH}".format(QUEUE=options.queue, SH=shName))    
