#!/usr/bin/python

import signal
import time

class TimeoutManager(object):
    '''
    Timeout manager.
    Accepts only call by name, not positional call.
    '''
    def __init__(self, **kwargs):
        '''
        '''
        import pdb; pdb.set_trace()         
        kwargs['timeout'] = 3600*24, 
        kwargs['refresh'] = 3600, 
        kwargs['message'] = 'end of time', 
        kwargs['logger' ] = None, 
        import pdb; pdb.set_trace()         
        
        self.timeout = kwargs['timeout']
        self.refresh = kwargs['refresh']
        self.message = kwargs['message']
        self.logger  = kwargs['logger' ]
        import pdb; pdb.set_trace()         

        signal.signal(signal.SIGALRM, self._handler)
        signal.alarm(self.timeout)

    def start(self):
        '''
        Runs its self function check() and it it takes 
        more than the timeout specified when this object got instantiated,
        raises an exception.
        '''
        try:
            self.check(kwargs)
        except Exception, exc: 
            if self.logger: 
                logger.error(exc)
            else:      
                print exc  

    def _handler(self, signum, frame):
        '''
        What to do if timeout is over
        '''
        if self.logger:
            logger.error(self.message)
        raise Exception(self.message)

    def check(self, kwargs):
        '''
        The function to be overridden.
        '''
        now = time.time()
        msg = '%d \tseconds elapsed' %( round(time.time() - now, 2) )
        if self.logger: 
            logger.info(msg)
        else:      
            print msg
        time.sleep(self.refresh)


# class TimeoutCheckProcessedFiles():
#     def check(self, api, dataset, run, procFileList, missingFilesTolerance):
#         while 1:
#             # number of files in DBS for the given run 
#             DbsFilesForRun = getFilesToProcessForRun(self.api    ,
#                                                      self.dataSet,
#                                                      run         )
# 
#             # number of processed files and number of dbs files
#             # for the given run
#             procFilesForRun = [file for file in self.procFileList
#                                if str(run) in file]
#                            
#             nMissingFiles = abs(len(procFilesForRun) - len(DbsFilesForRun))
#             
#             if nMissingFiles <= self.missingFilesTolerance:
#                 break
# 
#             time.sleep(0.3)


class TimeoutDummy(TimeoutManager):
    '''
    Example child class
    '''
    def __init__(self, run = -99, **kwargs):
        import pdb; pdb.set_trace()         
        super(TimeoutDummy, self).__init__()         
    
    def check(self, run):
        print run
        now = time.time()
        while time.time() - now < 5:
            msg = 'I started %.1f seconds ago' %(round(time.time() - now, 2))
            print msg
            time.sleep(self.refresh)
               
if __name__ == '__main__':
    
    timeoutKwargs = dict( timeout = 10. ,
                          run     = 195660,
                          refresh = 0.5 ,
                          message = 'fuck you' ,
                          logger  = None )
    
    print 'dalsjdh'                      
    timeout = TimeoutDummy(**timeoutKwargs)
    print 'kkkkkkkk'                      
    timeout.start()
 
#     import random
#     def mycheck(run):
#         now = time.time()
#         while 1:
#             print run
#             a = random.random()
#             b = random.random()
#             msg ='I started %.1f seconds ago' %(round(time.time() - now, 2))
#             print msg, a, b, abs(a-b)
#             if abs(a-b) < 0.01: 
#                 print 'FOUND!', abs(a-b)
#                 break
#             time.sleep(0.2)
#     
#     timeout.check = mycheck
#     timeout.start()

# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# import math 
# import re
# import optparse 
# import commands 
# import os 
# import sys 
# import time 
# import datetime
# 
# 
# # alternatively one can use enum, or enum's mockups
# # http://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python?page=1&tab=votes#tab-top
# class timeoutTypes(object):
#     NULL = -1 
#     ZERO =  0 
#     ONE  =  1 
# 
# def timeoutManager(type, timeout = -1, fileName = '.timeout'):
# 
#     if timeout == 0:
#         return 1
#         
#     timeFormat   = '%a,%Y/%m/%d,%H:%M:%S'
#     currentTime  = time.gmtime()
#     timeoutLine  = type + ' ' + time.strftime(timeFormat, currentTime) + '\n'
#     isTimeout    = False
#     alreadyThere = False
#     timeoutType  = -1
#     fileExist    = os.path.isfile(fileName)
#     text         = ''
#     fields       = []
#     reset        = False
# 
#     if timeout == -1:
#         reset = True
# 
#     if fileExist:
#         
#         file = open(fileName)
#         
#         for line in file:
#             text   += line
#             fields  = line.strip('\n').split(' ')
#             
#             if fields[0] == type:
#                 
#                 alreadyThere = True
#                 
#                 if reset:
#                     text = text.replace(line,'')
#                     continue
# 
#                 fileTime      = time.strptime(fields[1],timeFormat)
#                 myTime        = time.mktime(fileTime)
#                 referenceTime = time.mktime(time.gmtime())
#                 daylight      = 0
#                 
#                 if currentTime.tm_isdst == 0:
#                     daylight = 3600
#                 
#                 elapsedTime = referenceTime - myTime - daylight
#                 
#                 if elapsedTime > timeout:
#                     isTimeout   = True
#                     timeoutType = 1
#                     print 'Timeout! ' + str(elapsedTime) + ' seconds passed '\
#                           'since the ' + type + ' timeout was set and you '  \
#                           'can\'t tolerate more than ' + str(timeout) +      \
#                           ' seconds!'
#                 else:
#                     timeoutType = 0
#                     print 'Timeout of type ' + type + ' already exist and '\
#                           'was generated ' + str(elapsedTime) + ' seconds '\
#                           'ago at ' + fields[1]
# 
#         file.close()
# 
#     if not fileExist or not alreadyThere and not reset:
#         timeoutType  = -1
#         text        += timeoutLine
# 
#     if not fileExist or not alreadyThere or \
#        isTimeout or (reset and alreadyThere):
#         
#         if fileExist:
#             commands.getstatusoutput('rm -rf ' + fileName)
#         
#         file = open(fileName,'w')
#         file.write(text)
#         file.close()
# 
#     return timeoutType
