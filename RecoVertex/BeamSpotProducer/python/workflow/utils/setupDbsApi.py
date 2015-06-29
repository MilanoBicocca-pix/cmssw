#!/usr/bin/python

import os

try:
    from dbs.apis.dbsClient import DbsApi
except:
    print 'ERROR: you need to set up a Crab environment first, in order '\
          'to connect to DBS3'
    shell = os.getenv('SHELL')
    if 'csh' in shell:  
        print 'source /cvmfs/cms.cern.ch/crab3/crab.csh' # CRAB3 does not work
        #print 'source /afs/cern.ch/cms/ccs/wm/scripts/Crab/crab.csh'      
    else:
        #print 'source /cvmfs/cms.cern.ch/crab3/crab.csh'
        print 'source /afs/cern.ch/cms/ccs/wm/scripts/Crab/crab.sh'      
    exit()


def setupDbsApi(url = 'https://cmsweb.cern.ch/dbs/prod/global/DBSReader',
                logger = None):
    ''' 
    Adding api for dbs3 queries.
    Default = https://cmsweb.cern.ch/dbs/prod/global/DBSReader DBS3
    This works only if the crab environment is set.
    '''
    if logger: logger.info('Opening a DBS3 instance %s' %url)
    else     : print 'Opening a DBS3 instance %s' %url
    api = DbsApi(url = url)
    return api

if __name__ == '__main__':
    print 'connected to DBS3'
    api = setupDbsApi()
