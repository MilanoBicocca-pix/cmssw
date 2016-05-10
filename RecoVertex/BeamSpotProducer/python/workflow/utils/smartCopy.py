import os
import commands

def cp(fromDir          ,
       toDir            ,
       listOfFiles      ,
       overwrite = False,
       smallList = False,
       logger    = None ):

    '''
    Moves a bunch of files from one directory to another
    '''

    # RIC: this needs some rehauling I believe. Castor anyone anymore?

    cpCommand   = ''
    copiedFiles = []
    
    if fromDir.find('castor') != -1 or toDir.find('castor') != -1 :
    	cpCommand = 'rf'
    elif fromDir.find('resilient') != -1:
    	cpCommand = 'dc'
    
    if fromDir[len(fromDir)-1] != '/':
        fromDir += '/'

    if toDir[len(toDir)-1] != '/':
        toDir += '/'
        
    for file in listOfFiles:
        if os.path.isfile(toDir + file):
            if overwrite:
                if logger: logger.info('\t\tFile ' + file + ' already exists in destination directory. We will overwrite it.')
                else     : print 'File ' + file + ' already exists in destination directory. We will overwrite it.'
            else:
                if logger: logger.info('\t\tFile ' + file + ' already exists in destination directory. We will Keep original file.')
                else     : print 'File ' + file + ' already exists in destination directory. We will Keep original file.'
                if not smallList:
                    copiedFiles.append(file)
                continue
    	# copy to local disk
    	aCommand = cpCommand + 'cp '+ fromDir + file + ' ' + toDir
    	if logger: logger.info(aCommand)
    	else     : print ' >> ' + aCommand
    	
        tmpStatus = commands.getstatusoutput( aCommand )
        if tmpStatus[0] == 0:
            copiedFiles.append(file)
        else:
            if logger: logger.error('Can\'t copy file ' + file)
            else     : print ' Can\'t copy file ' + file
    return copiedFiles


def cyclicCp(fromDir          ,
             toDir            ,
             listOfFiles      ,
             overwrite = False,
             smallList = False,
             logger    = None ,
             attempts  = 3    ):

    if logger: logger.info('Copying files from %s to %s' %(fromDir, toDir))
    copiedFiles = []
    for i in range(attempts):
        if logger: logger.info('\t|___ Attempt %d' %(i+1))
        copiedFiles = cp(fromDir, toDir, listOfFiles, logger = logger)
        if len(copiedFiles) == len(listOfFiles):
            if logger: logger.info('\t\t|___ %d/%d files copied or already existing' %(len(copiedFiles), len(listOfFiles)))
            break
    if len(copiedFiles) != len(listOfFiles):            
        if logger: logger.error(error_failed_copy(copiedFiles, listOfFiles))
    return copiedFiles









