import glob
import os
import subprocess
from itertools import product
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-f"  , "--folder"     , dest = "folder"    ,  help = "input folder to list", default = '')
parser.add_argument("-o"  , "--outfile"    , dest = "outfile"   ,  help = "output file name"    , default = '')
options = parser.parse_args()

if not options.outfile:   
  parser.error('outfilelist name not given')


thelowlumiruns = [
'247910',
'247911',
'247912',
'247913',
'247914',
'247915',
'247917',
'247919',
'247920',
'247921',
'247923',
'247924',
'247926',
'247927',
'247928',
'247931',
'247933',
'247934',
'247702',
'247703',
'247704',
'247705',
'247707',
'247708',
'247710',
'247711',
'247716',
'247718',
'247719',
'247720',
'247685',
'247642',
'247644',
'247646',
'247647',
'247648',
'247623',
'247607',
'247609',
'247610',
'247611',
'247612',
'247377',
'247379',
'247380',
'247381',
'247382',
'247383',
'247384',
'247385',
'247386',
'247387',
'247388',
'247389',
'247394',
'247395',
'247397',
'247398',
'247302',
'247303',
'247305',
'247306',
'247307',
'247309',
'247310',
'247313',
'247317',
'247318',
'247319',
'247320',
'247323',
'247324',
'247326',
'247328',
'247333',
'247334',
'247335',
'247336',
]


def eos_command():

  shell = os.getenv('SHELL')
  cmd = subprocess.Popen(shell+' -c "which eos"', shell=True, stdout=subprocess.PIPE)

  for i, line in enumerate(cmd.stdout):
      if i > 0 : break
      eos = line.split(' ')[-1].rstrip()

  return eos


def get_eos_folders(path, folders):
    eos = eos_command()
    list_files_cmd = '{EOS} ls {PATH}'.format(EOS = eos, PATH = path)
    cmd = subprocess.Popen(list_files_cmd, shell = True,
                           stdout = subprocess.PIPE)

    for i, line in enumerate(cmd.stdout):
        file = line.split(' ')[-1].rstrip()
        if '.root' not in file :
            folders.append(file)


def get_eos_files_and_folders(path, files, folders):
    eos = eos_command()
    list_files_cmd = '{EOS} ls {PATH}'.format(EOS = eos, PATH = path)
    cmd = subprocess.Popen(list_files_cmd, shell = True,
                           stdout = subprocess.PIPE)

    for i, line in enumerate(cmd.stdout):
        file = line.split(' ')[-1].rstrip()
        if '.root' not in file :
            folders.append('/'.join([path, file]))
        else:
            files.append('/'.join([path, file]))


def get_eos_files(path):

    files                 = []
    newfiles              = []
    folders               = []
    subfolders            = []
    subsubfolders         = []
    subsubsubfolders      = []
    
    outfile   = open(options.outfile,'w+')
    print >> outfile, 'import FWCore.ParameterSet.Config as cms \n'    

#     for xx in product (['1', '2' ], ['247']):
    for xx in product (['1','2','3','4','5','6','7','8'], ['247']):

        folders    = []
        thedataset = 'ZeroBias' + xx[0]
        thepath    = '/store/data/Run2015A/' + thedataset + '/RECO/PromptReco-v1/000/' + xx[1]     
        get_eos_folders(thepath, folders)
#         print 'zero bias '  + xx[0]
#         print '\n'.join(folders)
    
#     
        for i in folders:
        
            # discard runs not in the thelowlumiruns list
            therunstring = xx[1] + i
            if therunstring not in thelowlumiruns: continue
            
            newfiles      = []
            thefolderpath = thepath + '/' + i + '/00000/'
            # print thefolderpath
            try: 
                get_eos_files_and_folders(thefolderpath, newfiles, folders)
            except:
                continue

            try:
                newfiles[0] 
                print >> outfile, 'list_zerobias' + xx[0] + '_run' + xx[1] + i + ' = cms.untracked.vstring('
                for ifile in newfiles:
                    print >> outfile, '\'' + ifile + '\','
                print >> outfile, ')'
            except:
                print 'no files found'

    return files


def get_afs_files(path):
    '''
    accepts wildcards too, e.g.
    PATH1/*PATH2*/CommonString*.root
    '''
    allfiles = glob.glob(path)
    files = []
    for f in allfiles:
        if f.endswith('.root'):
            files.append(f)
    return files


def get_files(path):

    if path.startswith('/store'):
        return get_eos_files(path)
    else:
        return get_afs_files(path)

if __name__ == '__main__':
    
#     outfile   = open(options.outfile,'w+')

    if options.folder:
        for file in get_files(options.folder):
#             print file
            print >> outfile, file.rstrip()
        

    else: 
        print 'warning: no input folder given, using example folder'
        for file in get_files('/store/relval/CMSSW_7_3_0/RelValQQH1352T_Tauola_13/GEN-SIM-DIGI-RAW-HLTDEBUG/PU25ns_MCRUN2_73_V7-v1/00000/'):
            print file
        print 'warning: no input folder given, using example folder'

