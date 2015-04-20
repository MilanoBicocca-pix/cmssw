#!/usr/bin/python

import sys

if sys.version_info < (2,6,0):
    import json
else:
    import simplejson as json

def readJson(firstRun = -1, fileName = ''):
    '''
    Reads the json <fileName> file and casts the run 
    number from string to integer.
    Returns only runs with run number >= <firstRun>
    '''
    
    try:
        # load the json if this is in a file
        file = open(fileName)
        jsonFile = file.read()
        file.close()
        jsonList = json.loads(jsonFile)
    except:
        # but can work even if you passed the full json string
        jsonList = json.loads(fileName)
            
    selected_dcs = {int(k):v for k, v in jsonList.items() if int(k) >= firstRun}
    
    return selected_dcs

if __name__ == '__main__':
    myjson = readJson(194000, 
                      '../cfg/beamspot_payload_2012BONLY_merged_JSON_all.txt')
    print myjson                  
