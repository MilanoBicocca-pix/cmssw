class IOV(object):
    '''
    Interval of Validity object
    '''
    def __init__(self, *args):
        '''
        IOV() initiates a dummy IOV, all values set to -1.
        '''
        self.since     = -1
        self.till      = -1
        self.RunFirst  = -1
        self.RunLast   = -1
        self.LumiFirst = -1
        self.LumiLast  = -1
