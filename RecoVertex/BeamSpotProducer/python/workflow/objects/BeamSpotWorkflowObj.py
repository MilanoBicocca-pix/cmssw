#!/usr/bin/python

import glob
import os
import re

import RecoVertex.BeamSpotProducer.workflow.utils.colorer

from RecoVertex.BeamSpotProducer.workflow.objects.PayloadObj   import Payload

from RecoVertex.BeamSpotProducer.workflow.utils.errorMessages  import *
from RecoVertex.BeamSpotProducer.workflow.utils.setupDbsApi    import setupDbsApi
from RecoVertex.BeamSpotProducer.workflow.utils.locker         import Locker
from RecoVertex.BeamSpotProducer.workflow.utils.readJson       import readJson
from RecoVertex.BeamSpotProducer.workflow.utils.dbsCommands    import getListOfRunsAndLumiFromDBS
from RecoVertex.BeamSpotProducer.workflow.utils.dbsCommands    import getFilesToProcessForRun
from RecoVertex.BeamSpotProducer.workflow.utils.condDbCommands import getLastUploadedIOV
from RecoVertex.BeamSpotProducer.workflow.utils.compareLists   import compareLists
from RecoVertex.BeamSpotProducer.workflow.utils.timeoutManager import TimeoutManager 
from RecoVertex.BeamSpotProducer.workflow.utils.beamSpotMerge  import averageBeamSpot
from RecoVertex.BeamSpotProducer.workflow.utils.beamSpotMerge  import splitByDrift
    
class BeamSpotWorkflow(object):
    '''
    FIXME! docstring to be written
    '''

    def __init__(self, cfg, lock, overwrite, globaltag, logger):
                
        self.logger  = logger
        self.tagName = globaltag
        
        self.logger.info('Initialising a BeamSpotWorkflow class')
        self.logger.info('Configuration: {CFG}'.format(CFG = vars(cfg)))
        
        self.api = setupDbsApi(logger = self.logger)

        for k, v in vars(cfg).items():
            setattr(self, k, v)
        
        if lock: 
            self._checkIfAlreadyRunning()
        
        self._setupDirectories()
        
        # This should be a bit more elaborated, possibly
        self.procFileList = [file for file in os.listdir(self.sourceDir) 
                             if '.txt' in file]

    def _checkIfAlreadyRunning(self):
        '''
        Check whether there's another BeamSpotWorkflow
        running, by assessing the existence of locker.lock file
        '''
        self.logger.info('Check whether another script is running')        
        
        self.locker = Locker('locker.lock')
        
        if self.locker.checkLock():
            self.logger.error('There is already a megascript '\
                              'runnning... exiting')
            exit()
        else:
            self.locker.lock()

    def _setupDirectories(self):
        '''
        Directory setup
        '''
        self.logger.info('Setting up the directory structure')        
        # check that the relevant directories end with a '/'
        for dir in (self.sourceDir, self.archiveDir, self.workingDir):
            if not dir.endswith('/'):
                dir += '/'

        # check that sourceDir exists
        if not ( os.path.isdir(self.sourceDir) and
                 os.path.exists(self.sourceDir) ) :
            self.logger.error(error_source_dir(self.sourceDir))

        # create archiveDir
        if not os.path.isdir(self.archiveDir):
            os.mkdir(self.archiveDir)

        # create workingDir
        if not os.path.isdir(self.workingDir):
            os.mkdir(self.workingDir)
        else:
            os.system('rm -f {WORKDIR}*'.format(WORKDIR = self.workingDir))

    def _getRunLumiBeamspot(self, resultsDir, minRun = -1):
        '''
        Loads the payload files produced by the crab jobs.
        Returns the runs and lumi sections processed as well as a collection
        with one BeamSpotObject for each single fit.
        '''
        # get the run numbers from the file names in resultsDir.
        runs = set([re.findall(r'\d+', file)[1] for file in self.procFileList]) 
        files = []
        for run in runs:
            if int(run) <= minRun: continue
            files.extend(glob.glob('/'.join([resultsDir, '*' + run + '*.txt'])))

        # for each run parse the ASCII files and load the BS objects 
        newPayloadTot = Payload(files)

        # this returns a dictionary like {195660 : [1,2,3,...]}
        runsLumis = newPayloadTot.getProcessedLumiSections() 

        # this returns a dictionary like {195660 : {60 : BeamSpotObject}}
        runsLumisBS = newPayloadTot.fromTextToBS() 
        
        return runsLumis, runsLumisBS
        
    def _getRunDiffs(self, runsLumisCRAB, runsLumisJSON, 
                     runsLumisDBS, lastUnclosedRun):
        '''
        Checks the runs that have been processed by CRAB, or listed
        in DBS or listed in the JSON/RunRegistry.
        For each processed run, it also returns the lumi section
        diffs against the JSON and the DBS.
        If a any run or lumi section is present in CRAB but not in DBS or 
        in JSON, a critical error is issued.
        Returns all the diffs.  
        '''
        # Get run numbers of runs that are in CRAB but not in JSON
        # and vice-versa
        runsInJSONnotInCRAB, runsInCRABnotInJSON = compareLists(
            runsLumisCRAB.keys()   , 
            runsLumisJSON.keys()   , 
            tolerance = 100        , 
            listAName = 'CRAB runs', 
            listBName = 'JSON runs',
            logger = self.logger   
        )
        
        # Get run numbers of runs that are in CRAB but not in DBS
        # and vice-versa
        runsInDBSnotInCRAB, runsInCRABnotInDBS = compareLists(
            runsLumisCRAB.keys()   , 
            runsLumisDBS .keys()   , 
            tolerance = 100        , 
            listAName = 'CRAB runs', 
            listBName = 'DBS  runs',
            logger = self.logger   
        )

        # all the processed runs *must* be present in DBS too
        if runsInCRABnotInDBS and lastUnclosedRun not in runsInCRABnotInDBS:
            self.logger.critical('Runs {RUNS} are processed but not in DBS'\
                                 ''.format(RUNS = runsInCRABnotInDBS))
            exit()

        # all the processed runs *must* be present in JSON too
        if runsInCRABnotInJSON:
            self.logger.critical('Runs {RUNS} are processed but not in JSON'\
                                 ''.format(RUNS = runsInCRABnotInJSON))
            exit()

        lumisInDBSnotInCRAB  = {}
        lumisInCRABnotInDBS  = {}
        lumisInJSONnotInCRAB = {}
        lumisInCRABnotInJSON = {}

        # check also the
        for run in runsLumisCRAB.keys():
            # check how many lumis for the given run have been processed
            lumisInDBSnotInCRABrun, lumisInCRABnotInDBSrun = compareLists(
                runsLumisCRAB[run]                      , 
                runsLumisDBS [run]                      , 
                tolerance = 100                         , 
                listAName = 'CRAB lumis for run %d' %run, 
                listBName = 'DBS  lumis for run %d' %run,
                logger = self.logger                    
            )

            # all the processed lumis *must* be present in DBS too
            if lumisInCRABnotInDBSrun:
                self.logger.critical('Run {RUN}: Lumis {LUMIS} are processed '\
                                     'but not in JSON'                        \
                                     ''.format(RUN   = run                   ,
                                               LUMIS = runsInCRABnotInJSONrun))
                exit()

            lumisInDBSnotInCRAB[run] = lumisInDBSnotInCRABrun            
            lumisInCRABnotInDBS[run] = lumisInCRABnotInDBSrun            

            lumisInJSONnotInCRABrun, lumisInCRABnotInJSONrun = compareLists(
                runsLumisCRAB[run]                      , 
                runsLumisJSON[run]                      , 
                tolerance = 100                         , 
                listAName = 'CRAB lumis for run %d' %run, 
                listBName = 'JSON lumis for run %d' %run,
                logger = self.logger                    
            )

            # all the processed lumis *must* be present in DBS too
            if lumisInCRABnotInJSONrun:
                self.logger.critical('Run {RUN}: Lumis {LUMIS} are processed '\
                                     'but not in JSON'                        \
                                     ''.format(RUN   = run                    ,
                                               LUMIS = lumisInCRABnotInJSONrun))
                exit()
            
            lumisInJSONnotInCRAB[run] = lumisInJSONnotInCRABrun
            lumisInCRABnotInJSON[run] = lumisInCRABnotInJSONrun
            
        return (runsInDBSnotInCRAB , runsInJSONnotInCRAB, 
                lumisInDBSnotInCRAB, lumisInJSONnotInCRAB)
    
    def _writePayload(self, toProcess):
        '''
        Writes the final Payload file.
        Does the weighed averages internally.
        '''
        for run, lumis in toProcess.items():
            
            # if not runbase, 
            # get start and end lumi, for lumi ranges where the 
            # beam spot coordinates are similar enough to 
            # be merged and averaged
            
            if self.fileIOVBase == 'runbase':
                pairs = [ (lumis.keys()[0], lumis.keys()[-1]) ]
            else:
                pairs = splitByDrift(lumis)
        
            # merge the beam spot fits for each lumi range and dump them into 
            # the payload file.
            for p in pairs:
                bs_list = [ lumis[i] for i in range(p[0], p[1] + 1) ]
                aveBeamSpot = averageBeamSpot(bs_list)
                aveBeamSpot.Dump(self.payloadFileName)
             
    def process(self):
        '''
        FIXME! Write the DOC
        '''        
        self.logger.info('Begin process')

        filesToProcess = []

        # Check the last IOV from querying the COND DB
#         lastUploadedIOV = getLastUploadedIOV(self.databaseTag, 
#                                              self.tagName    ,
#                                              self.logger     )
        
        # RIC: just for testing
        lastUploadedIOV = 0

        self.logger.info('Last uploaded run: %d' %lastUploadedIOV)
                                             
        # Get processed files in self.sourceDir, 
        # with run number greater than lastUploadedIOV
        runsLumisCRAB, runsLumisBSCRAB = self._getRunLumiBeamspot(
                                            self.sourceDir, 
                                            lastUploadedIOV
                                            )
        
        self.logger.info('Retrieved CRAB processed runs and lumis')
                
        # Get from DBS the list of Runs and lumis after last IOV
#         runsLumisDBS  = getListOfRunsAndLumiFromDBS(self.api       , 
#                                                     self.dataSet   , 
#                                                     lastUploadedIOV,
#                                                     packed = False )


        runsLumisDBS  = runsLumisCRAB
        runsLumisJSON = runsLumisCRAB







        lastUnclosedRun = max(runsLumisDBS.keys())
        self.logger.info('Retrieved runs and lumis in DBS')
        self.logger.info('Last unclosed DBS run %d' %lastUnclosedRun)

        # Get from JSON the list of Runs and lumis after last IOV
#         runsLumisJSON = readJson(lastUploadedIOV  , 
#                                  self.jsonFileName,
#                                  packed = False   )

        self.logger.info('Retrieved runs and lumis in the JSON')

        # At this point for CRAB, JSON and DBS we have a dictionary like:
        # {194116 : [2, 3, 4, 5, 15, 16, 17, 18]}

        


        # Get from runs in {DBS, CRAB, JSON} but not in {DBS, CRAB, JSON}
        runDiffs =  self._getRunDiffs(runsLumisCRAB  , 
                                      runsLumisJSON  , 
                                      runsLumisDBS   ,
                                      lastUnclosedRun)

        # runs
        runsInDBSnotInCRAB   = runDiffs[0]
        runsInJSONnotInCRAB  = runDiffs[1]
        # lumis
        lumisInDBSnotInCRAB  = runDiffs[2]
        lumisInJSONnotInCRAB = runDiffs[3]

        self.logger.info('Checked different runs and lumis from the '\
                         'three sources, CRAB, DBS and JSON, '       \
                         'against each other')
        
        # let's assume that all the CRAB outputs are good to process.
        # Will prune this collection in the following steps, if
        # anything is wrong
        toProcess = runsLumisBSCRAB
        
        # check how many JSON runs haven't been processed yet
        for run in runsInJSONnotInCRAB:
            if len(runsLumisJSON[run]) < self.rrTolerance:
                self.logger.warning('missing run, but small')
            else:
                self.logger.critical('missing big run. Will process '\
                                     'only the ones before')
                toProcess = { k:v for k, v in toProcess.items() if k < run}
                break


#         import pdb ; pdb.set_trace()
       
        # check that, for the runs that are processed, most, if not all,
        # the lumi sections have been processed.
        # If the number of missing lumis goes beyond the tolerance,
        # warnings and errors are issued. 
        for run in toProcess.keys():
            
#             timeout = TimeoutManager(10, 0.2, 'timeout exceeded', self.logger)
#             timeout.check = self.checkProcessedFiles(run)
#             timeout.start()

            
#             if nMissingFiles >= self.missingFilesTolerance:
#                 self.logger.warning('missing files timeout %' %nMissingFiles)
#                 signal.signal(signal.SIGALRM, handler)
#                 signal.alarm(10)
#                 while nMissingFiles >= self.missingFilesTolerance:  
#                     hang(2)            
#             else:
#                 self.logger.error('out!')
            

            # consider as missing lumis the ones that are present in 
            # both the JSON and DBS but not in CRAB
            missing = set(lumisInJSONnotInCRAB[run]) & \
                      set(lumisInDBSnotInCRAB [run])
            
            # in percentage over the number of lumis in JSON
            missingPercent = float(len(missing)) / \
                             float(len(runsLumisJSON[run]))
            
            if not missing:
                self.logger.debug('All lumis are processed for run {RUN}'\
                                  ''.format(RUN = run))
            elif len(missing)   <  self.dbsTolerance        or \
                 missingPercent <= self.dbsTolerancePercent :
                self.logger.warning('Missing some lumis,for run {RUN}'\
                                    ', but carry on'                  \
                                    ''.format(RUN = run))
            else:
                self.logger.critical('Missing too many lumis for run {RUN}. ' \
                                     'Will process only the runs before this.'\
                                     ''.format(RUN = run))
                toProcess = { k:v for k, v in toProcess.items() if k < run}
        
        # finally write the Payload
        self._writePayload(toProcess)
                      
        if hasattr(self, 'locker'):
            self.locker.unlock()
        

if __name__ == '__main__':

    from RecoVertex.BeamSpotProducer.workflow.utils.initLogger            import initLogger
    
    cfg = object()
    
    cfg.sourceDir             = 'Runs2012B_FULL/Results/'
    cfg.archiveDir            = 'Runs2012B_FULL/Archive/'
    cfg.workingDir            = 'Runs2012B_FULL/Working/'
    cfg.jsonFileName          = 'beamspot_payload_2012BONLY_merged_JSON_all.txt'
    cfg.databaseTag           = 'BeamSpotObjects_2009_LumiBased_SigmaZ_v29_offline'
    cfg.dataSet               = '/StreamExpress/Run2012B-TkAlMinBias-v1/ALCARECO'
    cfg.fileIOVBase           = 'lumibase'
    cfg.dbIOVBase             = 'lumiid'
    cfg.dbsTolerance          = 200000
    cfg.dbsTolerancePercent   = 5.
    cfg.rrTolerance           = 200000
    cfg.missingFilesTolerance = 200000
    cfg.missingLumisTimeout   = 0
    cfg.mailList              = 'manzoni@cern.ch'
    cfg.payloadFileName       = 'PayloadFile.txt'

    logger = initLogger(emails = cfg.mailList)
    
    bswf = BeamSpotWorkflow( 
                             cfg       = cfg              ,
                             lock      = options.lock     ,
                             overwrite = options.overwrite,
                             globaltag = options.tag      ,
                             logger    = logger
                           )

    bswf.process()