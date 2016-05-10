import os
from subprocess import Popen, PIPE


def source(script, update=True):
  '''
  http://pythonwise.blogspot.fr/2010/04/sourcing-shell-script.html (Miki Tebeka)
  '''
  proc = Popen('. %s; env -0' % script, stdout=PIPE, shell=True)
  output = proc.communicate()[0]
  env = dict((line.split('=', 1) for line in output.split('\x00') if line))
#   import pdb ; pdb.set_trace()
  if update:
      os.environ.update(env)
  return env

def initCrab(crab_init_script = '/afs/cern.ch/cms/ccs/wm/scripts/Crab/crab.sh'):

  print 'initialising Crab environment'

  shell = os.getenv('SHELL')
  source(crab_init_script)
  return source(crab_init_script)

if __name__ == '__main__':
  initCrab()



# from RecoVertex.BeamSpotProducer.workflow.utils.initCrab      import initCrab
# RIC: cannot make it work, as the environment variables set in 
# a subprocess don't outlive the subprocess itself. 
# Child processes cannot affect their parent. Need to do it the old way.
# os.environ.update(initCrab())


