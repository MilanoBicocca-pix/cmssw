#!/usr/bin/python

def compareLists(listA, listB, tolerance = 0, 
                 listAName = 'listA', listBName = 'listB',
                 logger = None, verbose = True):
    '''
    Reads two lists, listA and listB.
    Returns a list of elements that are included in listA
    but not in listB and the equivalent list for A<-->B.
    A tolerance in per cent units can be passed. Default = 0.
    
    Nota Bene: sorting the lists is important, as the tolerance
               is applied on one side only:
               len(listA) < len(listB) * (1 - 0.01 * tolerance)
               is tolerated, but an warning log is issued
    '''
    if logger and verbose: 
        logger.info('\tComparing %s and %s' %(listAName, listBName))
    
    # this holds if there are no repeated LS in a single Run
    setA = set(listA)
    setB = set(listB)
    
    if len(setA) != len(listA) or len(setB) != len(listB):
        if logger and verbose: 
            logger.warning('\t\tRepeated element sections in {A} or {B}'\
                         ''.format(A = listAName,
                                   B = listBName))
    
    if setA == setB:
        if logger and verbose: 
            logger.info('\t\tThe lists are the same')
        return [], [] # all is well, return
    
    if len(listA) < len(listB) * (1 - 0.01 * tolerance):
        if logger and verbose: 
            logger.warning('\t\tThe number of element sections is different: '\
                           '{A}({LENA})!=(LENB){B}'                           \
                           ''.format(A    = lisAName ,
                                   LENA = len(setA),
                                   LENB = len(setB),
                                   B    = listBName))

    in_A_not_in_B = sorted(list(setA - setB))  
    in_B_not_in_A = sorted(list(setB - setA))      
    
    for ele in in_A_not_in_B:
        if logger and verbose: 
            logger.warning('\t\tElement {ELE} is in {A} but not in {B}'\
                           ''.format(ELE = ele      , 
                                     A   = listAName,
                                     B   = listBName))        

    for ele in in_B_not_in_A:
        if logger and verbose: 
            logger.warning('\t\tElement {ELE} is in {B} but not in {A}'\
                           ''.format(ELE = ele      , 
                                     B   = listBName,
                                     A   = listAName))        

    return in_B_not_in_A, in_A_not_in_B

if __name__ == '__main__':

    listA = [1,2,3,4,5,7]
    listB = [1,3,4,5,6,7]
    
    print 'listA', listA
    print 'listB', listB
    
    in_B_not_in_A, in_A_not_in_B = compareLists(listA, listB)
     
    print 'in_B_not_in_A', in_B_not_in_A
    print 'in_A_not_in_B', in_A_not_in_B
    
