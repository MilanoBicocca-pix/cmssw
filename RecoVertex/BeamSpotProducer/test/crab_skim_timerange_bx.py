from CRABClient.UserUtilities import config as Configuration
from CRABAPI.RawCommand import crabCommand

import os, sys
import json
import argparse
parser = argparse.ArgumentParser('''Submit jobs to skim events for VdM tasks.
The script reads time ranges, run ranges and lumisections from LUMI json files. 
The bunch crossings list is provided as an external argument.
Each submission should correspond to a single dataset and a single VdM configuration (json file).
The crab task is created block-wise to reduce the tape-recall time.
The output consists of events falling in the time ranges specified in the json file, 
matching the given bunch crossing numbers.
[!] the output is saved in /store/user/$USER/BeamSpot/
''')
parser.add_argument('--input'         , required=True             , help='timestamp file from lumi')
parser.add_argument('--storage'       , default='T3_IT_MIB'       , help='storage site')
parser.add_argument('--dataset'       , required=True             , help='input dataset')
parser.add_argument('--bunchcrossing' , required=True,nargs='+'   , help='list of bunchcrossings to select')
parser.add_argument('--workarea'      , default='TimeBX_skim'     , help='crab work area')
parser.add_argument('--subfolder'     , required=True             , help='subfolder name under /store/user/$USER/')
parser.add_argument('--whitelist'     , default=[], nargs='+'     , help='subfolder name under /store/user/$USER/')
parser.add_argument('--dryrun'        , action='store_true'       , help='don\'t run CRAB')
parser.add_argument('--streams'       , default=10    , type=int  , help='number of streams for fetching the block list')
parser.add_argument('--maxMemoryMB'   , default=2499  , type=int  , help='requested job memory in MB')
parser.add_argument('--unitsPerJob'   , default=100   , type=int  , help='crab parameter')

args = parser.parse_args()

class Scan:
  '''main class for building a scan object from a LUMI POG json file.
  A Scan instance identifies a particular scan effort (eg. diagonal X coordinate).
  '''
  def __init__(self, label, json, number):
    self.label  = os.path.basename(label).strip('.json')
    self.main   = json
    self.index  = number
    self.scan   = self.main['Scans'][self.index]
    self.runn   = self.main['Run'  ][self.index]
    self.points = [Point(scan=self, index=i) for i in range(self.scan['NumPoints'])]
    self.times  = ','.join(p.times  for p in self.points)

class Point:
  ''' class for building a scan point object. 
  A Point instance identifies a beam step in a scan effort.
  '''
  def __init__(self, scan, index):
    self.scan     = scan
    self.index    = index
    self.lumib    = self.scan.scan['LSStartTimes'][self.index]
    self.lumie    = self.scan.scan['LSStopTimes' ][self.index]
    self.timeb    = self.scan.scan['StartTimes'  ][self.index]
    self.timee    = self.scan.scan['StopTimes'   ][self.index]
    self.lumis    = set([l for l in range(self.lumib, self.lumie+1)])
    self.times    = '{B}:{E}'.format(B=self.timeb, E=self.timee)

def popen(cmd): return tuple(l.strip('\n') for l in os.popen(cmd).readlines())
def fetch_blocks(points):
  ''' queries needed files (by dataset, run and lumi) from DAS.\n
  Use the file list to query the needed blocks.'''
  from multiprocessing import Pool
  pool = Pool(args.streams)
  FILES   = 'dasgoclient --query="file dataset={D} run={R} lumi={L}"'
  BLOCKS  = 'dasgoclient --query="block file={F}"'
  SIZE    = 'dasgoclient --query="{T}={B} | grep {T}.size"'

  sys.stdout.write("Fetching blocks...") ; sys.stdout.flush()
  queriesF  = list(set([FILES.format(D=args.dataset, R=p.scan.runn, L=l) for p in points for l in p.lumis]))
  files     = set(_ for f in pool.map(popen, queriesF) for _ in f)
  queriesB  = [BLOCKS.format(F=f) for f in files]
  blocks    = set(_ for b in pool.map(popen, queriesB) for _ in b)
  queriesSB = [SIZE.format(T='block', B=b) for b in blocks]
  queriesSF = [SIZE.format(T='file' , B=f) for f in files]
  sizeB     = sum([int(_) for s in pool.map(popen, queriesSB) for _ in s])
  sizeF     = sum([int(_) for s in pool.map(popen, queriesSF) for _ in s])
  sys.stdout.write("\rFetching blocks...done\n") ; sys.stdout.flush()
  print('''{F} files found, {B} blocks will be added to the crab task ({S} GB)'''.format(F=len(files), B=len(blocks), S=sizeB>>30))
  #print('''Expected output size: less than {S} GB'''.format(S=sizeF>>30))
  return blocks

lumijson  = json.load(open(args.input, 'r'))
scans     = [Scan(label=os.path.basename(args.input).strip('.json'), json=lumijson, number=s['ScanNumber']-1) for s in lumijson['Scans']]
points    = [p for s in scans for p in s.points]
blocks    = list(fetch_blocks(points))

if not len(blocks):
  print("[WARNING] no blocks match the requested conditions. Execution stops.")
  sys.exit(1)

JOBNAME     = '_'.join([args.dataset.replace('/', '_')[1:], os.path.basename(args.input).strip('.json')])
RUNSTRING   = ','.join(str(s.runn)  for s in scans)
TIMESTRING  = ','.join(s.times      for s in scans)
BUNCHSTRING = ','.join(b for b in args.bunchcrossing)
OUTPUT      = '/store/user/{}/{}/'.format(os.environ['USER'], args.subfolder)

config = Configuration()
config.General.workArea         = args.workarea
config.General.requestName      = JOBNAME
config.General.transferOutputs  = True
config.JobType.pluginName       = 'Analysis'
config.Data.publication         = False
config.Data.useParent           = False
config.Data.inputDBS            = 'global'
config.Data.splitting           = 'FileBased'
config.Data.inputDataset        = args.dataset
config.Data.runRange            = RUNSTRING
config.Site.storageSite         = args.storage
config.JobType.psetName         = 'EventSkimming_byTime_byBX.py'
config.JobType.maxMemoryMB      = args.maxMemoryMB
config.Data.outLFNDirBase       = OUTPUT
config.Data.inputBlocks         = blocks
config.JobType.maxJobRuntimeMin = 60*24*7
config.JobType.pyCfgParams = [
  "bunchcrossing={}".format(BUNCHSTRING),
  "timerange={}"    .format(TIMESTRING) ,
]
if config.Data.splitting!='Automatic':
  config.Data.unitsPerJob = args.unitsPerJob
if len(args.whitelist):
  config.Site.whitelist = args.whitelist

crabCommand('submit', config=config, dryrun=args.dryrun)