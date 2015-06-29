import datetime

from logging          import getLogger, FileHandler, StreamHandler, Formatter
from logging          import DEBUG, INFO, CRITICAL, WARNING, ERROR
from logging.handlers import SMTPHandler

from getpass import getuser
from socket  import gethostname


def initLogger(filename          = 'beamspot_workflow.log', 
               mode              = 'w+',
               formatter         = '[%(asctime)s] [%(levelname)-8s] '  \
                                   '[%(funcName)-33s : L%(lineno)4d]: '\
                                   '%(message)s ', 
               formatter_options = '%Y-%m-%d %H:%M:%S',
               emails            = [''],
               file_level        = 'info',
               stream_level      = 'info',
               email_level       = 'critical'):
    
    '''
    Initiates a Logger
    '''

    levels = {'debug'   : DEBUG   ,
              'info'    : INFO    ,
              'warning' : WARNING ,
              'error'   : ERROR   ,
              'critical': CRITICAL}
  
    user, host = getuser(), gethostname()
    subject = 'URGENT! BeamSpot worflow critical error'  
      
    logger = getLogger('beamsporWorkflow')
    logger.setLevel(DEBUG)
  
    date = datetime.datetime.now().date().isoformat()
    time = str(datetime.datetime.now().time()).split('.')[0].split(':')
    h = time[0]
    m = time[1]
    s = time[2]
    
    if not filename.endswith('.log'):
        filename = filename.replace(filename.split('.')[-1:],'log')
    
    filename_appendix = '_date_{DATE}_time{H}-{M}-{S}.log'.format(HOST = host,
                                                                  DATE = date,
                                                                  H    = h   ,
                                                                  M    = m   ,
                                                                  S    = s   )
    
    filename = filename.replace('.log', filename_appendix)
           
    fh = FileHandler(filename = filename, mode = mode)
    ch = StreamHandler()
    mh = SMTPHandler(mailhost    = host              ,
                     fromaddr    = user + '@cern.ch' ,
                     toaddrs     = emails            ,
                     subject     = subject           ,
                     credentials = None              ,
                     secure      = None              )
  
    fh.setLevel(levels[file_level  ])
    ch.setLevel(levels[stream_level])
    mh.setLevel(levels[email_level ])
  
    format = Formatter(formatter, formatter_options)
  
    fh.setFormatter(format)
    ch.setFormatter(format)
    mh.setFormatter(format)
  
    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.addHandler(mh)
    
    return logger
