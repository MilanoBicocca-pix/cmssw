#!/usr/bin/python

import ROOT
from math import sqrt, pow
from numpy import average
from collections import OrderedDict # only with python >= 2.7
from RecoVertex.BeamSpotProducer.workflow.objects.BeamSpotObj import BeamSpot

def cleanAndSort(fullList, cleanBadFits = True):
    '''
    Sorts the lumi:BS dictionary and cleans it up
    from the not properly converged fits.
    '''
    # clean from badly converged
    cleaned =  {k:v for k, v in fullList.items() if v.Type > 0 and cleanBadFits}

    # sort by LS
    ordered = OrderedDict(sorted(cleaned.items(), key = lambda t: t[0]))
                                         
    return ordered

def delta(x, xe, y, ye):
    '''
    Returns the distance between x and y and, its error 
    and its significance.
    Order matters, x first, y second.
    Gives the sign of the difference.
    '''
    delta        = x - y
    deltaErr     = sqrt(pow(xe, 2) + pow(ye, 2))
    significance = 0.   
    
    # protect against divisions by 0.
    if delta:
        significance = abs(delta) / max(1e-6 * abs(delta), deltaErr)

    return delta, deltaErr, significance

def splitByDrift(fullList, maxLumi = 60, splitInfo = False, run = -1, 
                 slopes = False, relaxedCriteria = False):
    '''
    Group lumi sections where the Beam Spot position does not 
    drift beyond the parameters specified by the user.
    If the drift in any direction exceeds the boundaries,
    split the lumi section collection.
    Returns a list of lumi section ranges.
    
    The lumi list is anyways split in chunks of at most 
    maxLumi lumi sections. Default = 60.
    
    The lumi section where the fit hasn't converged properly
    are excluded (Type > 0 is required).
    '''
    # instantiate a TH1 to check what drifts how often
    if splitInfo:
        ROOT.gROOT.SetBatch(True)
        histo = ROOT.TH1F('histoRun%d' %run,
                          'Run %d where the drift occurs' %run, 
                          8, 0, 8)
        file = ROOT.TFile.Open('splitInfo.root', 'update')
    
    # Clean up badly converged fits and sort the dictionary
    fullList = cleanAndSort(fullList)
    
    # breaking points. 
    # First LS is the first starting point by definition
    if not len(fullList.keys()):  return []
    breaks = [fullList.keys()[0]]
        
    # lumi counter
    i = 0
    
    # check the beam spot position against the one before 
    # and the one after.
    # Reset every maxLumi lumi sections or at every drift
    for j in range( 1, len(fullList.items())-1 ):
        
        lumi        = fullList.keys()[j  ]
        lumi_before = fullList.keys()[j-1]
        lumi_after  = fullList.keys()[j+1]

        bs        = fullList[lumi       ]  # bs        is the current beam spot
        bs_before = fullList[lumi_before]  # bs_before is the previous
        bs_after  = fullList[lumi_after ]  # bs_after  is the next
        
        i += 1

        # variables are constructed as follows:
        # (variable, its error, resolution (if any), 
        #  minimum drift, drift significance,
        #  full drift check, partial drift check)
        #
        # this mess is inherited from the old code...

        if relaxedCriteria:
            variables = [
              ('X'         , 'Xerr'      , 'beamWidthX', 0.05, 7., True , True ),
              ('Y'         , 'Yerr'      , 'beamWidthY', 0.05, 7., True , True ),
              ('Z'         , 'Zerr'      , 'sigmaZ'    , 0.  , 7., False, False),
              ('sigmaZ'    , 'sigmaZerr' , ''          , 0.  , 7., False, False),
              ('beamWidthX', 'beamWidthX', ''          , 0.  , 7., False, True ),
              ('beamWidthY', 'beamWidthY', ''          , 0.  , 7., False, True )
            ]
            if slopes:
                variables += [('dxdz', 'dxdzerr', '', 0., 10., False, True ),
                              ('dydz', 'dydzerr', '', 0., 10., False, True )]
        else:
            variables = [
              ('X'         , 'Xerr'      , 'beamWidthX', 0.0025, 3.5, True , True ),
              ('Y'         , 'Yerr'      , 'beamWidthY', 0.0025, 3.5, True , True ),
              ('Z'         , 'Zerr'      , 'sigmaZ'    , 0.    , 3.5, False, False),
              ('sigmaZ'    , 'sigmaZerr' , ''          , 0.    , 5. , False, False),
              ('beamWidthX', 'beamWidthX', ''          , 0.    , 5. , False, True ),
              ('beamWidthY', 'beamWidthY', ''          , 0.    , 5. , False, True )
            ]
            if slopes:
                variables += [('dxdz', 'dxdzerr', '', 0., 5., False, True ),
                              ('dydz', 'dydzerr', '', 0., 5., False, True )]
        
        for variable in variables:
            
            x  = getattr(bs       , variable[0])
            y  = getattr(bs_before, variable[0])
            z  = getattr(bs_after , variable[0])
            
            xe = getattr(bs       , variable[1])
            ye = getattr(bs_before, variable[1])
            ze = getattr(bs_after , variable[1])
            
            try:
                minDeviation = max(getattr(bs, variable[2])/2., variable[3])
            except:
                minDeviation = variable[3]
            
            minSignificance = variable[4] 
             
            drifted = drift(x, xe, y, ye, z, ze,
                            minDeviation, minSignificance,
                            checkTrendsFull = variable[5],
                            checkTrendsPartial = variable[6])
            
            if drifted or i >= maxLumi:
                breaks.append(lumi_before)  # append ending lumi
                breaks.append(lumi)         # append starting lumi
                i = 0                       # reset lumi counter
                if drifted and splitInfo:
                    histo.Fill(variable[0], 1.)
                elif splitInfo:
                    histo.Fill('max lumi', 1.)    
                break

    # Last LS is the first breaking point by definition
    breaks.append(fullList.keys()[-1])

    # sort the list. There may be repeated breaking points in case
    # one finds a lumi range of one lumi only
    breaks = sorted(breaks)
    
    pairs = []
    
    # create start, end pairs. 
    for b in range(0, len(breaks), 2):
        pairs.append( (breaks[b], breaks[b+1]) )
    
    if splitInfo:
        histo.Draw()
        file.cd()
        histo.Write()
        file.Close()
        
    return pairs

def drift(x, xe, y, ye, z, ze, minDeviation = 0., 
          minSig = 3.5, checkTrendsFull = True, 
          checkTrendsPartial = True):
    '''
    What a Beam Spot "drift" is is defined here.
    Takes the two quantities to compute the difference of, x and y,
    and their errors, xe and ye.
    
    The minimum absolute difference between x and y can be
    specified by minDeviation, as well as the minimum (L / sigma),
    specified by minSigma, beyond which a drift is detected.
    
    default: minDeviation = 0.
    default: minSig = 0.
    '''
    # mind the order, this is a signed difference        
    diff_to_pre , err_to_pre , sig_to_pre  = delta(x, xe, y, ye)
    diff_to_post, err_to_post, sig_to_post = delta(x, xe, z, ze)
    
    # simple drift, significant deviation from
    # one lumi section to another
    drifted = sig_to_pre > minSig and abs(diff_to_pre) >= minDeviation 

    # maybe the drift before in not very significant,
    # but there is a trend
    #
    # lumi section
    # ^
    # |--                          bs_after         
    # |                           *|
    # |                          * |
    # |                         *  |
    # |                        *   |
    # |--                    bs    |               
    # |                     * |    |  
    # |                  *    |    |
    # |               *       |    |
    # |            *          |    | 
    # |-- bs_before|          |    |               
    # |____________|__________|____|___________ position
    # |            |               |    
    #               combined diff > limit    
    if not drifted and checkTrendsFull:
        if diff_to_pre * diff_to_post < 0                   and \
           abs(diff_to_pre) + abs(diff_to_post) >= minDeviation :
            drifted = True

    # maybe it looks like a drift but at the following LS
    # it goes back    
    #
    # lumi section
    # ^
    # |--        bs_after         
    # |                 | *
    # |                 |  * 
    # |                 |   *
    # |                 |    * 
    # |--               |     bs     
    # |                 |   * |
    # |                  *    |
    # |               * |     |
    # |            *    |     |
    # |-- bs_before|    |     |     
    # |____________|____|_____|________________ position
    # |            |    |     |          
    elif drifted and checkTrendsPartial:
        if diff_to_pre * diff_to_post >= 0         and \
           diff_to_post != 0.                      and \
           abs(diff_to_pre / diff_to_post) > 1./3. and \
           abs(diff_to_pre / diff_to_post) < 3.        :
            drifted = False

    return drifted    
    
def averageBeamSpot(bslist, doNotCheck = []):
    '''
    Returns a Beam Spot object containing the weighed average position
    of the Beam Spots in the list.
    
    Start and end time and lumi section are taken from the first and 
    last Beam Spot object respectively, so make sure the collection
    is sorted.
    '''

    # RIC: Type should have something to do with the fit convergence
    #      Possibly we should filter by Type.
    #      Add some logging. 

    bslist = [bs for bs in bslist if bs.Type > 0]
        
    # get the first and the last BS in the list
    firstBS = bslist[0 ]
    lastBS  = bslist[-1]
    
    # instantiate a new, empty Beam Spot object that will store the averages
    averageBS = BeamSpot()
        
    # weighed average of the position
    # if you want to average additional quantities
    # just add a variable (quantity, its error) to the list of pairs    
    for pair in [('X'         ,'Xerr'         ),
                 ('Y'         ,'Yerr'         ),
                 ('Z'         ,'Zerr'         ),
                 ('sigmaZ'    ,'sigmaZerr'    ),
                 ('dxdz'      ,'dxdzerr'      ),
                 ('dydz'      ,'dydzerr'      ),
                 ('beamWidthX','beamWidthXerr'),
                 ('beamWidthY','beamWidthYerr')]:
        value = lambda x: getattr(x, pair[0])
        error = lambda x: 1./max(1e-22, 
                                 getattr(x, pair[1]) * getattr(x, pair[1]))
    
        ave_value, ave_error = average(a        = [value(bs) for bs in bslist],
                                       weights  = [error(bs) for bs in bslist],
                                       returned = True                        )

        setattr(averageBS, pair[0], ave_value         )
        setattr(averageBS, pair[1], 1./sqrt(ave_error))
    
    # assuming that ls are contiguous in the list given.
    averageBS.IOVfirst     = firstBS.IOVfirst    
    averageBS.IOVlast      = lastBS .IOVlast     
    averageBS.IOVBeginTime = firstBS.IOVBeginTime
    averageBS.IOVEndTime   = lastBS .IOVEndTime  

    # check that these attributes are the same for all BS in the list.  
    for attr in ('Type', 'Run', 'EmittanceX', 'EmittanceY', 'betastar'):
        if attr in doNotCheck:
            continue
        for i, bs in enumerate(bslist):
            if getattr(bs, attr) != getattr(firstBS, attr):
                print 'ERROR: "%s" for the %d element of the '    \
                      'Beam Spot collection varies from the first'\
                      %(attr, i)
                exit()
        
        setattr(averageBS, attr, getattr(firstBS, attr))

    return averageBS

if __name__ == '__main__':
    print 'not yet implemented. Put here your tests'

