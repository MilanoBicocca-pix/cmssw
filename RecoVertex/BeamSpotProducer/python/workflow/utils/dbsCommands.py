#!/usr/bin/python

import pprint
import sys
import itertools
from RecoVertex.BeamSpotProducer.workflow.utils.readJson import readJson


if sys.version_info < (2,6,0):
    import json
else:
    import simplejson as json


def ranges(i):
    '''
    Unpacks a list of ranges into a fully extended list, e.g.:
    [ [1,3], [6,10] ] ==> [1, 2, 3, 6, 7, 8, 9, 10] 
    '''
    for a, b in itertools.groupby(enumerate(i), lambda (x, y): y - x):
        b = list(b)
        yield b[0][1], b[-1][1]

def getFilesToProcessForRun(api, dataset, run):
    '''
    Returns the list of files present in DBS for a given run.
    '''
    run = int(run)
    files = api.listFiles(dataset = dataset, run_num = run) 
    return files
    
def getJsonOfRunsAndLumiFromDBS(api, dataSet, lastRun = -1, logger = None):
    '''
    Queries the DBS for the runs and lumi sections for the dataset <dataSet>
    and run number >= <lastRun>.
    Returns a dictionary of this kind:
        {
            Run : [lumi_1, lumi_2, ...]
            ...
        }
    '''    
    datasetList    = dataSet.split(',')
    outputFileList = []
    runsAndLumis   = {}
    
    if logger: logger.info('Getting list of runs and lumis from DBS')
    
    for data in datasetList:
        
        if logger: logger.info('Getting list of files from DBS for the %s '    \
                               'dataset. From this list we will query for the '\
                               'run and lumisections' %data)
        
        output_files = [i.values()[0] for i in api.listFiles(dataset = data)]
        
        for file in output_files:
            
            # listFileLumis() only possible call by name   
            output = api.listFileLumis(logical_file_name = file) 
            run    = output[0]['run_num']
            lumis  = output[0]['lumi_section_num']
            
            if run < lastRun             : continue
            
            if run in runsAndLumis.keys(): 
                runsAndLumis[run] += sorted(list(ranges(sorted(lumis))))
            else:         
                runsAndLumis[run]  = sorted(list(ranges(sorted(lumis))))
    
    if len(runsAndLumis) == 0:
       if logger: logger.error('There are no new runs or lumis in DBS '\
                               'to process, exiting.')
       exit()
    
    runsAndLumisJson = json.dumps(runsAndLumis)        
    return runsAndLumisJson  # the nice CMS like json

def getListOfRunsAndLumiFromDBS(api, dataSet, lastRun = -1, 
                                logger = None, packed = False):

    '''
    Reads a json and returns a dictionary like
    {194116 : [[2,5], [15,18]]}               if packed
    {194116 : [2, 3, 4, 5, 15, 16, 17, 18]}   if not packed
    '''
    runsAndLumisJson = getJsonOfRunsAndLumiFromDBS(api    ,
                                                   dataSet, 
                                                   lastRun,
                                                   logger )
    
    runsAndLumisList = readJson(lastRun, runsAndLumisJson, packed)
                                                   
    return runsAndLumisList

if __name__ == '__main__':

    from RecoVertex.BeamSpotProducer.workflow.utils.setupDbsApi import setupDbsApi

    api     = setupDbsApi()
    dataSet = '/StreamExpress/Run2012B-TkAlMinBias-v1/ALCARECO'
    lastRun = 194000
    
#     runsAndLumis = getListOfRunsAndLumiFromDBS(api, dataSet, lastRun)
    runsAndLumis = getListOfRunsAndLumiFromDBS(api, dataSet, lastRun)
    
    print runsAndLumis[195660]
    
#     pp = pprint.PrettyPrinter(indent = 4)
#     pp.pprint(runsAndLumis)

