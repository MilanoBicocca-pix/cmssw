from ROOT               import TFile, TTree, gDirectory, TH1F, TH2F, TCanvas, TLegend
from DataFormats.FWLite import Events
from optparse import OptionParser

parser = OptionParser()
parser.usage = '''
'''
parser.add_option("-i"  , "--input"     , dest = "input"     ,  help = "input file"      , default = ''                )
parser.add_option("-o"  , "--output"    , dest = "output"    ,  help = "output file"     , default = 'out_test.root'   )
parser.add_option("-s"  , "--startlumi" , dest = "startlumi" ,  help = "starting LS"     , default = '1'               )
parser.add_option("-e"  , "--endlumi"   , dest = "endlumi"   ,  help = "ending LS"       , default = '100'             )

(options,args) = parser.parse_args()	
if not options.input:   
  parser.error('Input filename not given')


class pv(object):
  def __init__(self, event):
     self.x        = event.position[0]   
     self.y        = event.position[1] 
     self.z        = event.position[2]        
     self.xErr     = event.posError[0]              
     self.yErr     = event.posError[1]          
     self.zErr     = event.posError[2]          
     self.posCorr0 = event.posCorr[0]             
     self.posCorr1 = event.posCorr[1]
     self.posCorr2 = event.posCorr[2]


def fillHistos(tree    ,
               hlumi   , 
               hnpv,
               hpvx   ,
               hpvy   ,
               hpvz   
               ):

  lumi_npv = {}

  for i, ev in enumerate(tree):
    if i > 100000: break
    try:
      lumi_npv[ev.lumi]
    except:
      lumi_npv[ev.lumi] = []  
    
    mypv = pv(ev)
          
    lumi_npv[ev.lumi].append(mypv)

    hpvy .Fill (mypv.x )
    hpvx .Fill (mypv.y )
    hpvz .Fill (mypv.z )
      
  for k, v in lumi_npv.items():
    hnpv.Fill(k, len(v))


file_base = TFile.Open(options.input, 'r')
tree_base = file_base.Get('PrimaryVertices')

try:
  tree_base.GetEntries()
except:
  print 'pv tree not found'
  exit()

print 'output filename:' + options.output

list_base  = []
nbins      = int(options.endlumi) - int(options.startlumi)

# histos
hlumi_base = TH1F ('hlumi_base'  , 'hlumi_base'   , nbins, int(options.startlumi),  int(options.endlumi))
hnpv_base  = TH2F ('hnpv_base'   , 'hnpv_base'    , nbins, int(options.startlumi),  int(options.endlumi), 1000, 0, 10000)
         
hpvx_base  = TH1F ('hpvx_base'   , 'hpvx_base'    ,  1000, -0.2,  0.2)
hpvy_base  = TH1F ('hpvy_base'   , 'hpvy_base'    ,  1000, -0.2,  0.2)
hpvz_base  = TH1F ('hpvz_base'   , 'hpvz_base'    ,   400, -20 ,  20 )

hpvx_base.GetXaxis().SetTitle('PV x [cm]')
hpvy_base.GetXaxis().SetTitle('PV y [cm]')
hpvz_base.GetXaxis().SetTitle('PV z [cm]')

print 'filling...'

fillHistos(tree_base    , 
           hlumi_base   , 
           hnpv_base    ,
           hpvx_base    ,
           hpvy_base    ,
           hpvz_base    
           )

print 'filled '

list_base.extend (( hpvx_base,  hpvy_base,  hpvz_base ))

outfile = TFile.Open(options.output, 'recreate')
outfile.cd()
for i in list_base:
  i.Write()
hnpv_base.Write()

outfile  .Close() 
   
