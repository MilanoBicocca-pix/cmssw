#!/usr/bin/python

'''
Add here the error messages.
Helps keeping the scripts clean.

'''

def error_crab():
    msg = 'Please set a crab environment in order to get the proper JSON lib'
    return msg


def error_lumi_range(run, line, runListDir, fileName):
    msg = 'The lumi range is greater than 1 for run '\
          '{RUN} {LINE} in file: '                   \
          '{RUNLISTDIR}{FILENAME}'.format(RUN        = str(run)  ,
                                          LINE       = line      ,
                                          RUNLISTDIR = runListDir,
                                          FILENAME   = fileName  )
    return msg


def error_run_not_in_DBS(run):
    msg = 'Impossible but run {RUN} has been processed and it is also in the '\
          'run registry but it is not in DBS! Exit.'.format(RUN = str(run))
    return msg


def error_timeout(runsAndFiles, missingLumisTimeout, run):
    myRunsAndFiles = runsAndFiles[run]
    msg = 'I previously set a timeout that expired... '                  \
          'I can\'t continue with the script because there are too many '\
          '({MISSFILES} files missing) and for too long {HOURS} hours! ' \
          'I will process anyway the runs before this one '              \
          '({RUN})'.format(MISSFILES = str(nFiles - len(myRunsAndFiles)),
                           HOURS     = str(missingLumisTimeout/3600)    ,
                           RUN       = str(run)                         )
    return msg


def error_out_of_tolerance(run, lenA, lenB, dbsTolerancePercent, dbsTolerance):
    msg = 'For run {RUN} I didn\'t process {PERCENT}% of the lumis and '      \
          'I am not within the {TOLERANCEPERCENT}% set in the configuration. '\
          'The number of lumis that I didn\'t process ({LENA} out of '        \
          '{LENB}) is greater also than the {TOLERANCE} lumis that '          \
          'I can tolerate. I can\'t process runs >= {RUN} but I\'ll process ' \
          'the runs before!'.format(RUN              = str(run)                ,
                                    PERCENT          = str(100.*lenA/lenB)     ,
                                    TOLERANCEPERCENT = str(dbsTolerancePercent),
                                    LENA             = str(lenA)               ,
                                    LENB             = str(lenB)               ,
                                    TOLERANCE        = str(dbsTolerance)       )
    return msg


def error_run_not_in_rr(run):
    msg = 'Run {RUN} is in the run registry but it has '\
          'not been processed yet!'.format(RUN = run)
    return msg


def warning_missing_small_run(run, RRList, rrTolerance):
    msg = 'I previously set the MISSING_RUNREGRUN_Run{RUN} '               \
          'timeout that expired... I am missing run {RUN} but it only had '\
          '{RRLIST} <= {RRTOLERANCE} lumis. So I will continue and ignore '\
          'it... '.format(RUN         = str(run)        ,
                          RRLIST      = str(len(RRList)),
                          RRTOLERANCE = str(rrTolerance))
    return msg


def error_missing_large_run(run, RRList, rrTolerance):
    msg = 'I previously set the MISSING_RUNREGRUN_Run{RUN} timeout '          \
          'that expired...I am missing run {RUN} which has {RRLIST} > '       \
          '{RRTOLERANCE} lumis. I can\'t continue but I\'ll process the runs '\
          'before this one'.format(RUN         = str(run)        ,
                                   RRLIST      = str(len(RRList)),
                                   RRTOLERANCE = str(rrTolerance))
    return msg


def error_source_dir(sourceDir):
    msg = 'The source directory {SOURCEDIR} doesn\'t '\
          'exist!'.format(SOURCEDIR = sourceDir)
    return msg


def error_failed_copy(copiedFiles, newProcessedFileList):
    msg = 'I can\'t copy more than {COPIEDFILES} files out of '\
          '{ALLFILES}'.format(COPIEDFILES = str(len(copiedFiles))          ,
                              ALLFILES    = str(len(newProcessedFileList)) )
    return msg


def error_failed_copy_dirs(copiedFiles, selectedFilesToProcess, 
                           archiveDir, workingDir):
    msg = 'I can\'t copy more than {COPIEDFILES} files out of '\
          '{ALLFILES} from {ARCHIVEDIR} to '\
          '{WORKDIR}'.format(COPIEDFILES = str(len(copiedFiles))           ,
                             ALLFILES    = str(len(selectedFilesToProcess)),
                             ARCHIVEDIR  = archiveDir                      ,
                             WORKDIR     = workingDir                      )
    return msg


def warning_no_valid_fit():
    msg = 'None of the processed and copied payloads has a valid '           \
          'fit so there are no results. This shouldn\'t happen since we are '\
          'filtering using the run register, '                               \
          'so there should be at least one good run.'
    return msg


def warning_unable_to_create_payload():
    msg = 'I wasn\'t able to create any payload even '\
          'if I have some BeamSpot objects.'
    return msg


def error_sql_write_failed(tmpSqliteFileName):
    msg = 'An error occurred while writing the sqlite file: '\
          '{SQLITE}'.format(SQLITE = tmpSqliteFileName)
    return msg


def error_iov_not_implemented(dbIOVBase):
    msg = 'IOV {DBIOVBASE} still not '\
          'implemented.'.format(DBIOVBASE = dbIOVBase)
    return msg


def error_iov_unrecognised(dbIOVBase):
    msg = 'IOV {DBIOVBASE} unrecognised!'.format(DBIOVBASE = dbIOVBase)
    return msg


def error_tag_exist_last_iov_doesnt(tagName):
    msg = 'The tag {TAGNAME} exists but I can\'t '\
          'get the value of the last IOV'.format(TAGNAME= self.tagName)
    return msg


def warning_create_new_tag(dbError):
    msg = 'Creating a new tag because I got the following '\
          'error contacting the DB \n%s' %dbError
    return msg
    
    
def warning_not_all_file_yet(run, runsAndFiles, nFiles):
    msg = 'I haven\'t processed all files yet : {RUNSNFILES} out of '\
          '{NFILES} for run: '\
          '{RUN}'.format(RUNSNFILES = str(len(runsAndFiles[run])),
                         NFILES     = str(nFiles)                ,
                         RUN        = str(run)                   )
    return msg
    

def warning_dbs_mismatch_setting_timeout(run):    
    msg = 'Setting the DBS_VERY_BIG_MISMATCH_Run{RUN} timeout because '\
          'I haven\'t processed all files!'.format(RUN = str(run))
    return msg
    
    
def warning_dbs_mismatch_timeout(run):
    msg = 'Timeout DBS_VERY_BIG_MISMATCH_Run{RUN} '\
          'is in progress.'.format(RUN = str(run))
    return msg


def error_cant_connect_db(dbError):
    msg = 'Can\'t connect to db because:\n' + dbError
    return msg


def warning_setting_dbs_mismatch_timeout(run):
    msg = 'Setting the DBS_MISMATCH_Run{RUN} '\
          'timeout because I haven\'t processed all '\
          'files!'.format(RUN = str(RUN))
    return msg


def warning_dbs_mismatch_timeout_progress(run):
    msg = 'Timeout DBS_MISMATCH_Run{RUN} '\
          'is in progress.'.format(RUN = str(run))
    return msg
    

def warning_more_lumi_than_dbs():
    msg = 'This is weird because I processed more lumis than the '\
          'ones that are in DBS!'
    return msg
    

def warning_some_lumi_not_processed(run):
    msg = 'I have not processed some of the lumis that are in the run '\
          'registry for run: {RUN}'.format(RUN = str(run))
    return msg
    
    
def warning_bad_rr_size(badRRProcessed, badDBSProcessed):
    msg = 'badRRProcessed size is {BADRR} and badDBSProcessed size '\
          'is {BADDBS}'.format(BADRR  = str(len(badRRProcessed))  ,
                               BADBDS = str(len(badDBSProcessed)) )
    return msg


def error_lumi_in_run(begLumi, run):
    msg = 'Lumi {BEGLUMI} in event {RUN} already exist. '\
          'This MUST not happen but right now           '\
          'I will ignore this lumi!'.format(BEGLUMI = str(begLumi),
                                            RUN     = str(run)    )
    return msg
