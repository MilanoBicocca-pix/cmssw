import FWCore.ParameterSet.Config       as cms
import FWCore.ParameterSet.VarParsing   as VarParsing

options = VarParsing.VarParsing('analysis')
options.inputFiles = ''
options.maxEvents  = -1
options.register('jobName', 'skimmedForVdM',
    VarParsing.VarParsing.multiplicity.singleton,
    VarParsing.VarParsing.varType.string        ,
    "determines the output files names"         ,
)
options.register('bunchcrossing', '',
    VarParsing.VarParsing.multiplicity.list ,
    VarParsing.VarParsing.varType.int       ,
    "list of selected bunch crossings"      ,
)
options.register('timerange', '',
    VarParsing.VarParsing.multiplicity.list ,
    VarParsing.VarParsing.varType.string    ,
    "list of selected time ranges in the format start:end",
)
options.register('runs', '0:min-9999999:max'    ,
    VarParsing.VarParsing.multiplicity.singleton,
    VarParsing.VarParsing.varType.string        ,
    "lumirange in the format 'run:ls-run:ls,run:ls[...]'",
)
options.register('verbose', False,
    VarParsing.VarParsing.multiplicity.singleton,
    VarParsing.VarParsing.varType.bool          ,
)
options.parseArguments()
timeranges = [tuple(int(_) for _ in t.split(':')) for t in options.timerange]
assert any(len(t)==2  for t in timeranges), "Time ranges are ill-formatted\n"+str(timeranges)
assert any(t[0]<=t[1] for t in timeranges), "Time ranges are ill-formatted\n"+str(timeranges)

process = cms.Process(options.jobName)

process.source = cms.Source("PoolSource", 
    fileNames      = cms.untracked.vstring(options.inputFiles),
    lumisToProcess = cms.untracked.VLuminosityBlockRange(options.runs) 
)
process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(options.maxEvents))
process.options   = cms.untracked.PSet(wantSummary=cms.untracked.bool(True))
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.debugModules   = ['TimeRangeFilter', 'BunchCrossingFilter']
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet(reportEvery = cms.untracked.int32(1000))

process.skim_by_time = cms.EDFilter("TimeRangeFilter",
  verbose     = cms.untracked.bool(options.verbose),
  timeranges  = cms.VPSet(
    cms.PSet(start=cms.uint32(s),end=cms.uint32(e)) for s,e in timeranges
  )
)
process.skim_by_bx = cms.EDFilter("BunchCrossingFilter",
  verbose         = cms.untracked.bool(options.verbose),
  bunchcrossings  = cms.vuint32(options.bunchcrossing)
  
)
process.output = cms.OutputModule("PoolOutputModule", 
  fileName      = cms.untracked.string(options.jobName+".root"),
  SelectEvents  = cms.untracked.PSet(SelectEvents=cms.vstring("TimeBXfilter"))
)

process.TimeBXfilter = cms.Path(process.skim_by_time+process.skim_by_bx)
process.end          = cms.EndPath(process.output)
