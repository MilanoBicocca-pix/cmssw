#!/usr/bin/python

class BeamSpotWorkflowCfg(object):
    
    '''
    Object that contains all the configuration
    parameters to be passed to a BemSpotWorkflow.
        
    The user can append whatever number of additional
    parameters as attributes to this class.
    
    E.g.:
    
    mycfg = BeamSpotWorkflowCfg()
    mycfg.myNewMethod = 'something clever'
    
    A Print() function is also provided. 
    For each method it returns its value. 
    
    RIC: can plug here already the minimum set 
    needed to run, e.g.: 
        sourceDir            
        archiveDir           
        workingDir           
        jsonFileName         
        databaseTag          
        dataSet              
        fileIOVBase          
        dbIOVBase            
        dbsTolerance         
        dbsTolerancePercent  
        rrTolerance          
        missingFilesTolerance
        missingLumisTimeout  
        mailList             
        payloadFileName      
        ...
    
    '''
    
    def __init__(self):
        pass
        
    def Print(self):
        maxSpacing = len(max(vars(self).keys(), key=len))
        for k, v in vars(self).items():
            myKstr = '{K}'.format(K=k).ljust(maxSpacing)
            myVstr = '= {V}'.format(V=v)
            print myKstr, myVstr 


if __name__ == '__main__':

    # Example:
    # only dummy and longDummy and defined here 
    # as attributes, both set to None.

    mycfg = BeamSpotWorkflowCfg()
    mycfg.dummy     = None
    mycfg.longDummy = None
    mycfg.Print()
