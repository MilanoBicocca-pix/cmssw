from argparse import ArgumentParser

parser = ArgumentParser()
# parser.add_argument("-Q"  , "--queue"     , dest = "queue"      ,  help = "choose queue (1nh 8nh 1nd 2nd 1nw 2nw). Default is 1nd" , default = '1nd'   )
# parser.add_argument("-R"  , "--run"       , dest = "run"      ,  help = "choose run number "                                     , default = ''      )
parser.add_argument("-c"  , "--cfg"       , dest = "cfg"        ,  help = "input cfg file"                          , default =  "../BeamFit_LumiBased_NoRefit_Template.py"             )
parser.add_argument("-t"  , "--test"      , dest = "test"       ,  help = "do not submit to queue"                  , default =  False, action='store_true')
parser.add_argument("-r"  , "--range"     , dest = "timefile"   ,  help = "time interval file"                      , default =  "time_ranges_319894_scan1_X1.txt"   )
parser.add_argument("-i"  , "--input"     , dest = "inputfiles" ,  help = "input file list"                         , default =  "filelist_318984_scanX1_ZBAOD.py"     )
parser.add_argument("-d"  , "--folder"    , dest = "newFolder"  ,  help = "out folder name"                         , default =  "folder_test"            )
parser.add_argument("-b"  , "--bunch"     , dest = "bx"         ,  help = "selected bx, if -1 no selection"         , default =  -1                       )
parser.add_argument("--ilumi"             , dest = "initls"     ,  help = "initial LS"                              , default =  "0"                      )
parser.add_argument("--flumi"             , dest = "endls"      ,  help = "final LS"                                , default =  "99999"                  )
parser.add_argument("--runN"              , dest = "runN"       ,  help = "run number"                              , default =  "254991"                 )

options = parser.parse_args()

print 'please check RUN Number!!!!'
# RUN_NUMBER = 318984
RUN_NUMBER = int(options.runN)
# if not options.run:   
#   parser.error('Run number not given')


import os
import datetime

flist   = open(options.timefile)
ranges  = flist.readlines()

# eval the number of jobs to be submitted
njobs = len(ranges)
print 'njobs: ', njobs

# create a new folder 
newFolder = options.newFolder
if os.path.exists('{FOLDER}'.format(FOLDER=newFolder)):
  print 'warning: the directory {FOLDER} already exists. \n   exiting...'.format(FOLDER=newFolder)
  exit()
else: 
  os.system('mkdir {FOLDER}'.format(FOLDER=newFolder))
  os.system('mkdir {FOLDER}/outCondor'.format(FOLDER=newFolder))
  
os.system('cp {LIST} {FOLDER}'.format(LIST=options.inputfiles, FOLDER=newFolder))
os.chdir(os.getcwd() +'/' + newFolder)


## create a cfg per each job and the corresponding .sh
for j in range(njobs): 
  k = j
  
  low_time = ranges[j].split(',')[0].rstrip()
  max_time = ranges[j].split(',')[1].rstrip()

  # write the .cfg file
  f   = open(options.cfg)
  f1  = open('{M}_{MIN}_{MAX}.py'.format(M=options.cfg.replace(".py","").replace("../","").rstrip(), MIN=str(low_time), MAX=str(max_time) ), "w")
  for line in f:
      newline = None
      newfile = None

      if 'timerange' in line:
          newline = line.replace('min_time_t,max_time_t', '{MIN},{MAX}'.format( MIN=str(low_time), MAX=str(max_time)).rstrip())
      if 'BeamFit_LumiBased_alcareco_template.' in line:
          newline = line.replace('BeamFit_LumiBased_alcareco_template', 'BeamFit_LumiBased_alcareco_{MIN}_{MAX}'.format( MIN=str(low_time), MAX=str(max_time) )).rstrip()
      if 'theBx' in line:
          newline = line.replace('theBx', '{BX}'.format( BX=str(options.bx)).rstrip())
      if 'filelist_template' in line:
          newline = line.replace('filelist_template', '{LIST}'.format( LIST=str(options.inputfiles).strip('.py')).rstrip())
          newline = newline.replace('file_list', 'file_list_{MIN}_{MAX}'.format( MIN=str(low_time), MAX=str(max_time)).rstrip())
      if 'file_list' in line and not 'filelist_template' in line:
          newline = line.replace('file_list', 'file_list_{MIN}_{MAX}'.format( MIN=str(low_time), MAX=str(max_time)).rstrip())
      if 'thelumirange' in line:
          newline = line.replace('thelumirange', '{run}:{ils}-{run}:{fls}'.format( run = RUN_NUMBER, ils = options.initls, fls = options.endls).rstrip())
      if newline:
        print >> f1,newline.strip()
      if not (newline or newfile):
        print >> f1,line.rstrip() 
  f1.close()
  f.close()


  # now write the .sh file
  shName = "script_bs_condor_{K}.sh".format(K=str(k))
  sh     = open("../script_bs_condor_template.sh")
  sh1    = open(shName,"w")
  os.system("chmod +x {SH}".format(SH=shName)) 
  for shline in sh:
      if '/wdir'  in shline:
          shline = shline.replace('/wdir', '/{FOLDER}'.format(FOLDER=newFolder)).rstrip()
          print >> sh1, shline.rstrip()
      elif 'thecfg.py'  in shline:
          shline = shline.replace('thecfg.py', '{FOLDER}/{M}_{MIN}_{MAX}.py'.format(M=options.cfg.replace("../","").replace(".py","").rstrip(), MIN=str(low_time), MAX=str(max_time), FOLDER=newFolder)).rstrip()
          print >> sh1, shline.rstrip()
      elif 'FILELIST'  in shline:
          shline = shline.replace('FILELIST', '{FILELIST}'.format(FILELIST=str(options.inputfiles))).rstrip()
          shline = shline.replace('FOLDER', '{FOLDER}'    .format(FOLDER=newFolder )).rstrip()
          print >> sh1, shline.rstrip()
      elif 'MINT'  in shline:
          shline = shline.replace('MINT', '{MIN}'.format(MIN=str(low_time))).rstrip()
          shline = shline.replace('MAXT', '{MAX}'.format(MAX=str(max_time))).rstrip()
          print >> sh1, shline.rstrip()
      else: 
        print >> sh1, shline.rstrip()
  sh1.close()
  sh.close()


  # now write the .cfg file to sbmit via condor
  cfgName = "condor_bs_template_{K}.cfg".format(K=str(k))
  cfg     = open("../condor_bs_template.cfg")
  cfg1    = open(cfgName,"w")
  to_sub = ['Log', 'Output','Error']
  for cfgline in cfg:
      if 'script_bs_condor_NN'  in cfgline:
          cfgline = cfgline.replace('NN', '{K}'.format(K=str(k))).rstrip()
          print >> cfg1, cfgline.rstrip()
      elif any(lll in cfgline for lll in to_sub):
          cfgline = cfgline.replace('FOLDER', '{FOLDER}'.format(FOLDER=newFolder)).rstrip()
          cfgline = cfgline.replace('KINDEX', '{K}'.format(K=str(k))).rstrip()
          print >> cfg1, cfgline.rstrip()
      elif 'FOLDER' in cfgline:
          cfgline = cfgline.replace('FOLDER', '{FOLDER}'.format(FOLDER=newFolder)).rstrip()
          print >> cfg1, cfgline.rstrip()
      elif 'INFILE' in cfgline:
          cfgline = cfgline.replace('INFILE', '{LIST}'.format(LIST=str(options.inputfiles))).rstrip()
          print >> cfg1, cfgline.rstrip()
      else: 
        print >> cfg1, cfgline.rstrip()
  cfg1.close()
  cfg.close()


  # submit to the queue
  print 'submitting {CFG}'.format(CFG=cfgName)
  print 'condor_submit {CFG}'.format(CFG=cfgName)
  if not options.test:
	print 'submit {SH}'.format(SH=shName)
	os.system("condor_submit {CFG}".format(CFG=cfgName))   
