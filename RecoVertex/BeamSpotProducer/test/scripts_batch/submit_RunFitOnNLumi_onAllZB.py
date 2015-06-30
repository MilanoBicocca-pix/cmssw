from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-Q"  , "--queue"     , dest = "queue"    ,  help = "choose queue. Available 1nh 8nh 1nd 2nd 1nw 2nw. Default is 1nd" , default = '1nd'   )
parser.add_argument("-i"  , "--initlumi"  , dest = "initlumi" ,  help = "choose initial lumi"                                             , default = ''      )
parser.add_argument("-e"  , "--endlumi"   , dest = "endlumi"  ,  help = "choose final lumi"                                               , default = ''      )
parser.add_argument("-r"  , "--lumirange" , dest = "lumirange",  help = "choose range lumi"                                               , default = 10      )
parser.add_argument("-c"  , "--cfg"       , dest = "cfg"      ,  help = "input cfg file"                                                  , default = "../BeamFit_LumiBased_NewAlignWorkflow_template.py"             )
parser.add_argument("-f"  , "--files"     , dest = "files"    ,  help = "input file list"                                                 , default =  "fileList_run247710.py"   )
parser.add_argument("-t"  , "--test"      , dest = "test"     ,  help = "do not submit to queue"                                          , default = False, action='store_true')


options = parser.parse_args()


import os
import datetime
import re
from RecoVertex.BeamSpotProducer.workflow.utils.readJson            import readJson
from RecoVertex.BeamSpotProducer.workflow.utils.unpackList          import unpackList
from RecoVertex.BeamSpotProducer.workflow.test.createRangesFromJson import group

thelumirange  = options.lumirange

# open the fileList, eval number of dataset to analyze and retrieve the run list
execfile(options.files)
list_toprocess = []
therunlist     = []
for k, v in globals().items():  
  if k == 'args' or k == 'list_toprocess' or k == 'therunlist':
    continue
  if isinstance(v, list):
    therunlist.append(k.split('_')[2])
    therunlist = list(set(therunlist))
      

# read the json file and create a dictionary run: [run:initlumi-run:endlumi] 
# in this way the lumirange takes into account if any LS is missing in json
myjson = readJson(fileName = 'json_DCSONLY.txt')                  
unpackedmyjson = unpackList(myjson)
lumilists = {}

for k, v in unpackedmyjson.items():
    lumiPairs = group(v, thelumirange, 3)
    lumilist = ['%d:%d-%d:%d' %(k, p[0], k, p[1]) for p in lumiPairs]
    lumilists[k] = lumilist

# import pdb; pdb.set_trace()


# now loop on the runlist 
for counter, theirun in enumerate(therunlist):
 
  list_toprocess = []

  # open the fileList and append to list_toprocess the lists of files to be analyzed for this run 
  for k, v in globals().items():  
    if k == 'args' or k == 'list_toprocess' or k == 'therunlist':
      continue
    if isinstance(v, list) and theirun in k:
        # print 'dataset names: ', k
        list_toprocess.append(k)

#   if counter > 0:  break 
#   import pdb; pdb.set_trace()
  # recover list of lumi ranges for this run 
  if int(theirun) in lumilists.keys():
    lumiforthisrun = lumilists[int(theirun)]
  else: 
    continue
  # create a new folder for this run
  newFolder = 'rerunBS_{RUN}'.format(RUN=theirun)
  if os.path.exists('{FOLDER}'.format(FOLDER=newFolder)):
    print 'warning: the directory {FOLDER} already exists. \n   exiting...'.format(FOLDER=newFolder)
    exit()
  else: 
    os.system('mkdir {FOLDER}'.format(FOLDER=newFolder))
  os.system('cp {LIST} {FOLDER}'.format(LIST=options.files, FOLDER=newFolder))
  os.chdir(os.getcwd() +'/' + newFolder)


  # eval the number of jobs to be submitted -> one for each lumirange
  njobs = len(lumiforthisrun)
  print 'njobs: ', njobs


  for j in range(njobs): 

    thisinitlumi = re.findall(r"[\w']+", lumiforthisrun[j])[1]
    thisfinlumi  = re.findall(r"[\w']+", lumiforthisrun[j])[3]

    print 'job ' + str(j) + ' will cover lumi range ' + lumiforthisrun[j]

    # write the .cfg file
    f   = open(options.cfg)
    f1  = open('{M}_{NUM}.py'.format(M=options.cfg.replace(".py","").replace("../","").rstrip(), NUM=str(j)), "w")
    for line in f:
      newline = None
      newfile = None
      if 'myLumiRange' in line:
          line = line.replace('myLumiRange', '"' + lumiforthisrun[j].rstrip() + '"').rstrip()
          print >> f1, line
      elif 'beamspot_firstData_NewAlignWorkflow_runXXX_byLumi.' in line:
          line = line.replace('beamspot_firstData_NewAlignWorkflow_runXXX_byLumi.', 'beamspot_firstData_NewAlignWorkflow_run{RUN}_byLumi_lumi{IN}_{END}.'.format(RUN=theirun, IN=thisinitlumi, END=str(thisfinlumi))).rstrip()
          print >> f1, line
      elif 'thefilelist' in line:
        thestringlist = ''
        for iii in range(len(list_toprocess) ):
            if iii == 0:
              thestringlist += list_toprocess[iii]  
            else:
              thestringlist += ' + '  + list_toprocess[iii]  
#         thestringlist = thestringlist.strip('+')    
        line = line.replace('thefilelist', str(thestringlist) + ' \n').rstrip()
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
    if not options.test:
      print 'submit'
      os.system("bsub -q {QUEUE} {SH}".format(QUEUE=options.queue, SH=shName))   
  
  # go back to master folder
  os.chdir('../')
