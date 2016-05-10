import os
import subprocess

class Locker(object):
    
    def __init__(self, name):
        self.lockFileName = name
         
    def checkLock(self):
        if os.path.isfile(self.lockFileName):
            return True
        else:
            return False
    
    def lock(self):
        subprocess.call(['touch', self.lockFileName])

    def unlock(self):
        if self.checkLock():
            subprocess.call(['rm', self.lockFileName])
