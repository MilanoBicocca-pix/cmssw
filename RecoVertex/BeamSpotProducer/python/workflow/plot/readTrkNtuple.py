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
# parser.add_option("-c"  , "--compare"   , dest = "compfile"  ,  help = "file to compare" , default = ''                )

(options,args) = parser.parse_args()	
if not options.input:   
  parser.error('Input filename not given')

# define track selection
trk_MinpT_         = 1.0
trk_MaxEta_        = 2.4
trk_MaxIP_         = 1.0
trk_MaxZ_          = 60
trk_MinNTotLayers_ = 6
trk_MinNPixLayers_ = -1
trk_MaxNormChi2_   = 20
min_Ntrks_         = 50
convergence_       = 0.9
inputBeamWidth_    = -1


def selectTrk(ev):
  if  ev.nTotLayerMeas   >= trk_MinNTotLayers_   \
  and ev.nPixelLayerMeas >= trk_MinNPixLayers_   \
  and ev.normchi2        <  trk_MaxNormChi2_     \
  and abs( ev.d0 )       <  trk_MaxIP_           \
  and abs( ev.z0 )       <  trk_MaxZ_            \
  and ev.pt              >  trk_MinpT_           \
  and abs( ev.eta )      <  trk_MaxEta_:
    return 1

  else:
    return 0

class track(object):
  def __init__(self, event):
     self.nTotLayerMeas   = event.nTotLayerMeas   
     self.nPixelLayerMeas = event.nPixelLayerMeas 
     self.normchi2        = event.normchi2        
     self.pt              = event.pt              
     self.d0              = event.d0              
     self.z0              = event.z0              
     self.eta             = event.eta             
     self.phi0            = event.phi0
     self.d0              = event.d0
     self.good            = selectTrk(event)


def fillHistos(tree    ,
               hlumi   , 
               hntracks,
               hgtracks,
               hpixL   ,
               htotL   ,
               hchi2   ,
               hpt     ,  
               hd0     ,   
               hz0     ,  
               heta    ,
               hphid0  ,       
               hpixL_g ,
               htotL_g ,
               hchi2_g ,
               hpt_g   ,  
               hd0_g   ,   
               hz0_g   ,  
               heta_g  ,
               hphid0_g       
               ):

  lumi_ntrks = {}

  for i, ev in enumerate(tree):
    if i % 10000 == 0:
      print i
    if i > 100000: break
    try:
      lumi_ntrks[ev.lumi]
    except:
      lumi_ntrks[ev.lumi] = []  
    
    mytrack = track(ev)
          
    lumi_ntrks[ev.lumi].append(mytrack)

    htotL .Fill (mytrack.nTotLayerMeas   )
    hpixL .Fill (mytrack.nPixelLayerMeas )
    hchi2 .Fill (mytrack.normchi2        )
    hpt   .Fill (mytrack.pt              )
    hd0   .Fill (mytrack.d0              )
    hz0   .Fill (mytrack.z0              )
    heta  .Fill (mytrack.eta             )
    hphid0.Fill (mytrack.phi0, mytrack.d0)

    if selectTrk(ev):
      htotL_g .Fill (mytrack.nTotLayerMeas   )
      hpixL_g .Fill (mytrack.nPixelLayerMeas )
      hchi2_g .Fill (mytrack.normchi2        )
      hpt_g   .Fill (mytrack.pt              )
      hd0_g   .Fill (mytrack.d0              )
      hz0_g   .Fill (mytrack.z0              )
      heta_g  .Fill (mytrack.eta             )
      hphid0_g.Fill (mytrack.phi0, mytrack.d0)
      
  for k, v in lumi_ntrks.items():
    hntracks.Fill(k, len(v))
    goods = [tr for tr in v if tr.good]
    hgtracks.Fill(k, len(goods))


  
  
  
file_base = TFile.Open(options.input, 'r')
tree_base = file_base.Get('mytree')

try:
  tree_base.GetEntries()
except:
  print 'track tree not found'
  exit()

print 'output filename:' + options.output
  

list_base  = []
nbins      = int(options.endlumi) - int(options.startlumi)

hlumi_base        = TH1F ('hlumi_base'       , 'hlumi_base'       ,   nbins, int(options.startlumi),  int(options.endlumi))
hntracks_base     = TH2F ('hntracks_base'    , 'hntracks_base'    ,   nbins, int(options.startlumi),  int(options.endlumi), 1000, 0, 50000)
hgtracks_base     = TH2F ('hgtracks_base'    , 'hgtracks_base'    ,   nbins, int(options.startlumi),  int(options.endlumi), 1000, 0, 50000)
hphi_d0_base      = TH2F ('hphi_d0_base'     , 'hphi_d0_base'     ,  314, -3.14, 3.14, 500, -0.5, 0.5)
hphi_d0_g_base    = TH2F ('hphi_d0_g_base'   , 'hphi_d0_g_base'   ,  314, -3.14, 3.14, 500, -0.5, 0.5)
         
hpixL_base        = TH1F ('hpixL_base'       , 'hpixL_base'       ,   20,   0,  20)
htotL_base        = TH1F ('htotL_base'       , 'htotL_base'       ,   20,   0,  20)
hchi2_base        = TH1F ('hchi2_base'       , 'hchi2_base'       ,  100,   0,  10)
hpt_base          = TH1F ('hpt_base'         , 'hpt_base'         ,   70,   0, 100)
hd0_base          = TH1F ('hd0_base'         , 'hd0_base'         ,  100,   0,  10)
hz0_base          = TH1F ('hz0_base'         , 'hz0_base'         ,  200, -20,  20)
heta_base         = TH1F ('heta_base'        , 'heta_base'        ,   60,  -3,   3)

hpixL_good_base   = TH1F ('hpixL_good_base'  , 'hpixL_good_base'  ,   20,   0,  20)
htotL_good_base   = TH1F ('htotL_good_base'  , 'htotL_good_base'  ,   20,   0,  20)
hchi2_good_base   = TH1F ('hchi2_good_base'  , 'hchi2_good_base'  ,  100,   0,  10)
hpt_good_base     = TH1F ('hpt_good_base'    , 'hpt_good_base'    ,   70,   0, 100)
hd0_good_base     = TH1F ('hd0_good_base'    , 'hd0_good_base'    ,  100,   0,  10)
hz0_good_base     = TH1F ('hz0_good_base'    , 'hz0_good_base'    ,  200, -20,  20)
heta_good_base    = TH1F ('heta_good_base'   , 'heta_good_base'   ,   60,  -3,   3)


hpixL_base.GetXaxis().SetTitle('# pixel layer')
htotL_base.GetXaxis().SetTitle('# total layer')
hchi2_base.GetXaxis().SetTitle('# norm chi2'  )
hpt_base  .GetXaxis().SetTitle('p_{T} [GeV]'  )
hd0_base  .GetXaxis().SetTitle('d0'           )
hz0_base  .GetXaxis().SetTitle('z0'           )
heta_base .GetXaxis().SetTitle('#eta'         )

print 'filling...'

fillHistos(tree_base        , 
           hlumi_base       , 
           hntracks_base    ,
           hgtracks_base    ,
           hpixL_base       ,
           htotL_base       ,
           hchi2_base       ,
           hpt_base         ,
           hd0_base         ,
           hz0_base         ,
           heta_base        ,
           hphi_d0_base     ,
           hpixL_good_base  ,
           htotL_good_base  ,
           hchi2_good_base  ,
           hpt_good_base    ,
           hd0_good_base    ,
           hz0_good_base    ,
           heta_good_base   ,
           hphi_d0_g_base   ,
           )

print 'filled '

list_base.extend ((    hpixL_base,       htotL_base,       hchi2_base,       hpt_base,       hd0_base,       hz0_base,       heta_base ))
list_base.extend((hpixL_good_base,  htotL_good_base,  hchi2_good_base,  hpt_good_base,  hd0_good_base,  hz0_good_base,  heta_good_base ))

outfile = TFile.Open(options.output, 'recreate')
outfile.cd()
for i in list_base:
  i.Write()
hntracks_base   .Write()
hgtracks_base   .Write()
hphi_d0_base    .Write()
hphi_d0_g_base  .Write()

outfile.Close() 
   
