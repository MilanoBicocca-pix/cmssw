#!/usr/bin/python

def unpackList(packedList):
    '''
    Unpacks a JSON like dictionary into something plainer
    e.g.:
    {194116 : [[2,5], [15,18]]}
    {194116 : [2, 3, 4, 5, 15, 16, 17, 18]}
    '''

    unpackedList = {}
    
    for k, v in packedList.items():
        LSlist = []
        for lr in v:
            LSlist += [l for l in range(lr[0], lr[1]+1)]
        
        unpackedList[k] = LSlist
    
    return unpackedList


if __name__ == '__main__':
    
    packed   = {194116: [[2,5], [15,18]]}
    unpacked = unpackList(packed)
    
    print 'Before'
    print packed
    print 'After'
    print unpacked 
