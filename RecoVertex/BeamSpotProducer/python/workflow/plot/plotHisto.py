from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-i"  , "--input"     , dest = "input"     ,  help = "input file"      , default = ''                        )
parser.add_argument("-o"  , "--output"    , dest = "output"    ,  help = "output file"     , default = 'out_test.root'           )
parser.add_argument("-s"  , "--startlumi" , dest = "startlumi" ,  help = "starting LS"     , default = '1'                       )
parser.add_argument("-e"  , "--endlumi"   , dest = "endlumi"   ,  help = "ending LS"       , default = '100'                     )
parser.add_argument("-c"  , "--compare"   , dest = "compfile"  ,  help = "file to compare" , default = ''                        )
parser.add_argument("-k"  , "--kind"      , dest = "kind"      ,  help = "track or PV"     , default = 'track'                   )
parser.add_argument("-r"  , "--run"       , dest = "run"       ,  help = "run number"      , default = ''                        )
parser.add_argument("-l"  , "--leg"       , dest = "legend"    ,  help = "legend entries"  , default = ''                        )
parser.add_argument("-d"  , "--diff"      , dest = "diff"      ,  help = "plot differences", default = False, action='store_true')

options = parser.parse_args()
if not options.input:   
  parser.error('Input filename not given')
if not options.run:   
  parser.error('Run number not given')


import ROOT
from   ROOT     import TFile, TTree, gDirectory, TH1F, TH2F, TCanvas, TLegend, gPad, gStyle, TGaxis


gStyle.SetTitleAlign(23)
TGaxis.SetMaxDigits(3)

file = TFile.Open(options.input  , 'r')
if options.compfile:
  file_comp = TFile.Open(options.compfile  , 'r')

c = TCanvas('', '', 600,400)
c.cd()

gStyle.SetOptStat('emr')
if options.diff:
  stackPad = ROOT.TPad('stackPad', 'stackPad', 0.,  .3, 1., 1.  , 0, 0)  
  ratioPad = ROOT.TPad('ratioPad', 'ratioPad', 0., 0. , 1.,  .38, 0, 0)  
else:
  stackPad = ROOT.TPad('stackPad', 'stackPad', 0,  0. , 1., 1.  , 0, 0)  
  ratioPad = ROOT.TPad('ratioPad', 'ratioPad', 0., 0. , 0., 0.  , 0, 0)  


c.cd()
stackPad.Draw()
ratioPad.Draw()
        
if 'PV' in options.kind:
  TGaxis.SetMaxDigits(3)

  variables = [
    # varName    # x-axis title    # y-axis title          # x-axis range  # legend position         # y-axis low pad  # rebin  # log y
    ('hpvx'      , 'PV x [cm]'     , '# selected PV'     , ( 0.04, 0.16),  (0.69, 0.89, 0.55, 0.65), (-0.5, 0.5 ),      4,      False),
    ('hpvy'      , 'PV y [cm]'     , '# selected PV'     , ( 0.0,  0.13),  (0.69, 0.89, 0.55, 0.65), (-0.5, 0.5 ),      4,      False),
    ('hpvz'      , 'PV z [cm]'     , '# selected PV'     , (-20 ,  20  ),  (0.69, 0.89, 0.55, 0.65), (-0.5, 0.5 ),      4,      False),
  ]

elif 'track' in options.kind:
  variables = [
    # varName    # x-axis title    # y-axis title          # x-axis range  # legend position         # y-axis low pad  # rebin  # log y
    ('hpixL'     , '# pixel layer' , '# tracks'          , (   0,    7 ),  (0.69, 0.89, 0.55, 0.65), (-0.1, 0.5 ),      1,       False),
    ('htotL'     , '# total layer' , '# tracks'          , (   3,   20 ),  (0.69, 0.89, 0.55, 0.65), (-0.1, 1   ),      1,       False),
    ('hchi2'     , '# norm chi2'   , '# tracks'          , (   0,    6 ),  (0.69, 0.89, 0.55, 0.65), (-1  , 0.5 ),      1,       False),
    ('hpt'       , 'p_{T} [GeV]'   , '# tracks'          , (   0,  100 ),  (0.69, 0.89, 0.55, 0.65), (-0.5, 1   ),      1,        True),
    ('hd0'       , 'd0 [cm]'       , '# tracks'          , (   0,   10 ),  (0.69, 0.89, 0.55, 0.65), (0   , 0.5 ),      1,        True),
    ('hz0'       , 'z0 [cm]'       , '# tracks'          , ( -20,   20 ),  (0.69, 0.89, 0.55, 0.65), (0.  , 0.65),      1,       False),
    ('heta'      , '#eta'          , '# tracks'          , (  -3,    3 ),  (0.69, 0.89, 0.55, 0.65), (0.  , 0.2 ),      1,       False),
    ('hpixL_good', '# pixel layer' , '# selected tracks' , (   0,    7 ),  (0.69, 0.89, 0.55, 0.65), (-0.1, 0.5 ),      1,       False),
    ('htotL_good', '# total layer' , '# selected tracks' , (   3,   20 ),  (0.69, 0.89, 0.55, 0.65), (-0.1, 0.2 ),      1,       False),
    ('hchi2_good', '# norm chi2'   , '# selected tracks' , (   0,    6 ),  (0.69, 0.89, 0.55, 0.65), (-2  , 0.2 ),      1,       False),
    ('hpt_good'  , 'p_{T} [GeV]'   , '# selected tracks' , (   0,  100 ),  (0.69, 0.89, 0.55, 0.65), (-0.1, 0.5 ),      1,        True),
    ('hd0_good'  , 'd0 [cm]'       , '# selected tracks' , (   0,    2 ),  (0.69, 0.89, 0.55, 0.65), ( 0  , 0.4 ),      1,        True),
    ('hz0_good'  , 'z0 [cm]'       , '# selected tracks' , ( -20,   20 ),  (0.69, 0.89, 0.55, 0.65), (-0.1, 0.5 ),      1,       False),
    ('heta_good' , '#eta'          , '# selected tracks' , (  -3,    3 ),  (0.69, 0.89, 0.55, 0.65), ( 0. ,  .1 ),      1,       False)
]

else:
  print 'no category selected'
  exit()    


for var in variables:

  h_base  = file.Get(var[0] + '_base' )

  h_base.Rebin(var[6])

  h_base.SetTitle('Run {RUN}'.format(RUN=options.run))
  h_base.GetXaxis().SetTitle(var[1])
  h_base.GetYaxis().SetTitle(var[2])
  h_base.GetYaxis().SetTitleOffset(1.3)
  h_base.GetXaxis().SetRangeUser(var[3][0], var[3][1])
  h_base.SetLineColor(ROOT.kBlack)

  stackPad.cd()
  h_base.Draw()
  c.Update()
  c.Modified()

  stats = gPad.GetPrimitive('stats')
  stats.SetBorderSize(0)
  stats.SetY1NDC(0.77)
  stats.SetY2NDC(0.89)
  stats.SetX1NDC(0.69)
  stats.SetX2NDC(0.89)
  stats.SetName('stat1')

  stackPad.SetLogy(var[7])
  # same for file2, if present
  if options.compfile:

    h_comp = file_comp.Get(var[0] + '_base')
    h_comp.SetLineColor(2)
    h_comp.Rebin(var[6])
    h_comp.Draw('sames')
    c.Update()
    c.Modified()
    stats = gPad.GetPrimitive('stats')
    print 'stats', stats
    stats.SetBorderSize(0)
    stats.SetY1NDC(0.65)
    stats.SetY2NDC(0.77)
    stats.SetX1NDC(0.69)
    stats.SetX2NDC(0.89)
    stats.SetTextColor(2)

    # draw legend
    if options.legend:
      entry_base = options.legend.split(',')[0]
      entry_comp = options.legend.split(',')[1]

      l = TLegend(var[4][0], var[4][2], var[4][1], var[4][3])
      l.AddEntry(h_base,  entry_base, 'l')
      l.AddEntry(h_comp,  entry_comp, 'l')
      l.SetBorderSize(0)
      l.Draw()

    # draw bottom pad with difference (h1-h2)/h1
    if options.diff:
      c.SetCanvasSize(600,900)
      stackPad.SetBottomMargin(0.2)
      ratioPad.cd()
      ratioPad.SetGridy(True)
      ratioPad.SetBottomMargin(0.2)
      h_base_clone = h_base.Clone()
      h_comp_clone = h_comp.Clone()
      h_base_clone.Sumw2()
      h_comp_clone.Sumw2()
      h_ratio = h_base_clone.Clone()
      for i in range(h_ratio.GetNbinsX()):
        n_comp = h_comp_clone .GetBinContent(i+1)
        n_base = h_base_clone .GetBinContent(i+1)
        e_comp = h_comp_clone .GetBinError(i+1)
        e_base = h_base_clone .GetBinError(i+1)
        h_ratio.SetBinContent(i+1, 1 - n_comp/max(0.000001,n_base))
        h_ratio.SetBinError  (i+1, (min (e_comp, e_base))/max(0.000001,n_base))
      h_ratio.GetYaxis().SetRangeUser( var[5][0], var[5][1])
      h_ratio.Draw('e')

      c.Update()
      c.Modified()
      stats = gPad.GetPrimitive('stat1')
      stats.SetBorderSize(0)
      stats.SetTextColor(0)
      stats.SetY1NDC(0.77)
      stats.SetY2NDC(0.77)
      stats.SetX1NDC(0.69)
      stats.SetX2NDC(0.69)
      h_ratio.SetTitle('')
      h_ratio.SetMarkerStyle(8)
      h_ratio.GetYaxis().SetNdivisions(6)
      h_ratio.GetYaxis().SetLabelSize(0.05)
      h_ratio.GetXaxis().SetLabelSize(0.06)
      h_ratio.GetYaxis().SetTitleSize(0.04)
      h_ratio.GetXaxis().SetTitleSize(0.07)  
      h_ratio.GetYaxis().SetTitleOffset(1)
      h_ratio.GetYaxis().SetTitle('difference/' + entry_base)

      c.SetLogy(var[7])

  if options.compfile:
    c.SaveAs('h_compare_' + var[0] + '_' + options.run + '.pdf')
  else: 
    c.SaveAs('h_' + var[0] + '_' + options.run + '.pdf')



#  plot per LUMI
c2 = TCanvas('', '', 600,400)
c2.cd()

gStyle.SetOptStat('')
TGaxis.SetMaxDigits(3)

if 'track' in options.kind:
  lumivar = [
    # varName     # x-axis title       # y-axis title  # x-axis range  # legend position          # log y
    ('hntracks', '# tracks'          , 'LS'         , (  0, 35000)  , (0.69, 0.89, 0.55, 0.65),   False),
    ('hgtracks', '# selected tracks' , 'LS'         , (  0, 30000)  , (0.69, 0.89, 0.55, 0.65),   False),
] 
if 'PV' in options.kind:
  lumivar = [
    # varName     # x-axis title       # y-axis title  # x-axis range  # legend position          # log y
    ('hnpv'    , '# selected PV'     , 'LS'         , (  0,  1000)  , (0.69, 0.89, 0.55, 0.65),   False),
] 

for ivar in lumivar:
  h_base = file.Get(ivar[0] + '_base' )

  h_base.SetTitle('Run {RUN}'.format(RUN=options.run))
  h_base.GetXaxis().SetTitle(ivar[2])
  h_base.GetYaxis().SetTitle(ivar[1])
  h_base.GetYaxis().SetTitleOffset(1)
  h_base.GetYaxis().SetRangeUser(ivar[3][0], ivar[3][1])
  
  h_base.SetLineColor(ROOT.kBlack)
  h_base.SetMarkerStyle(8)
  h_base.Draw('box')

  
  # same for file2, if present
  if options.compfile:
    h_comp = file_comp.Get(ivar[0] + '_base' )
    h_comp.SetLineColor(ROOT.kRed)

    h_comp.SetMarkerStyle(8)
    h_comp.SetMarkerColor(ROOT.kRed)
    h_comp.Draw('box sames')

    # draw legend
    if options.legend:
      l = TLegend(var[4][0], var[4][2], var[4][1], var[4][3])
      l.AddEntry(h_base,  entry_base, 'l')
      l.AddEntry(h_comp,  entry_comp, 'l')
      l.SetBorderSize(0)
      l.Draw()

  gPad.SetGridx()
  c2.SetLogy(ivar[5])
  
  if options.compfile:
    c2.SaveAs('h_compare_' + ivar[0] + '_' + options.run + '.pdf')
  else: 
    c2.SaveAs('h_' + ivar[0] + '_' + options.run + '.pdf')










