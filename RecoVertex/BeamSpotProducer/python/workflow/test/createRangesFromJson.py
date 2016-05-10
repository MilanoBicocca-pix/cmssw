#!/usr/bin/python

from RecoVertex.BeamSpotProducer.workflow.utils.readJson import readJson
from RecoVertex.BeamSpotProducer.workflow.utils.unpackList import unpackList

def group(lslist, groupLength = 10, maxGap = 1):
    '''
    Pass a list of LS, returns a list of pairs of at most groupLength LS
    (until LS run out, or a gap occurs).
    Gaps are in principle allowed via the tunable parameter maxGap.
    '''
    lslist = sorted(lslist)
    
    pairs = []
    start = lslist[0]
    end   = -1
    
    counter = 0
    
    for i, el in enumerate(lslist):
        next_index = min(i+1, len(lslist)-1)
        next_el    = lslist[next_index]
        counter   += 1
        if counter >= 10 or next_el - el > maxGap:
            end = el
            pairs.append( (start, end) )
            start = next_el
            counter = 0
        elif i == len(lslist) - 1:
            end = el
            pairs.append( (start, end) )
                
    return pairs


myjson = readJson(fileName = '../utils/json_DCSONLY.txt')                  
unpackedmyjson = unpackList(myjson)

# print unpackedmyjson                  

# 247267: [[1, 25], [26, 28], [146, 146]]
#   "247267": [
#     [
#       1,
#       25
#     ],
#     [
#       26,
#       28
#     ],
#     [
#       146,
#       146
#     ]

lumilists = {}

for k, v in unpackedmyjson.items():
    lumiPairs = group(v)
    lumilist = ['%d:%d-%d:%d' %(k, p[0], k, p[1]) for p in lumiPairs]
    lumilists[k] = lumilist

print lumilists[246908]

# lumilist_246908 = [
# '246908:0-246908:10',
# '246908:11-246908:20'
# ]
# 
# print '\n'*2, myjson[247267]                  
# mypairs = group(unpackedmyjson[247267])
# print mypairs
# 
# print '\n'*2, myjson[246959]                  
# mypairs = group(unpackedmyjson[246959])
# print mypairs
# 
# print '\n'*2, myjson[247398]                  
# mypairs = group(unpackedmyjson[247398])
# print mypairs
# 
# 
# 
# print mypairs
# 
