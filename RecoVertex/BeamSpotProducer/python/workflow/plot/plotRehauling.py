import ROOT
from PlotStyle import PlotStyle
from CMSStyle import CMS_lumi
from RecoVertex.BeamSpotProducer.workflow.utils.fillRunDict import labelByTime, labelByFill, splitByMagneticField

# 2015A ----------------------------------------------
#  ===> run: 247642  ls: 75
#  ===> run: 250932  ls: 135
# 
# 2015B ----------------------------------------------
#  ===> run: 251027  ls: 1
#  ===> run: 252126  ls: 100
# 
# 2015C ----------------------------------------------
#  ===> run: 254227  ls: 20
#  ===> run: 256464  ls: 1609
# 
# 2015D ----------------------------------------------
#  ===> run: 256630  ls: 6
#  ===> run: 260627  ls: 1818
 
ROOT.gROOT.SetBatch(False)
ROOT.gROOT.Reset()
ROOT.gROOT.SetStyle('Plain')
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(1111)
ROOT.gStyle.SetPadLeftMargin(0.1)
ROOT.gStyle.SetPadBottomMargin(0.2)
ROOT.gStyle.SetMarkerSize(1.5)
ROOT.gStyle.SetHistLineWidth(1)
ROOT.gStyle.SetStatFontSize(0.025)
ROOT.gStyle.SetTitleFontSize(0.05)
ROOT.gStyle.SetTitleSize(0.06, 'XYZ')
ROOT.gStyle.SetLabelSize(0.15, 'Y')
ROOT.gStyle.SetLabelSize(0.35, 'X')
ROOT.gStyle.SetNdivisions(510, 'YZ')
ROOT.gStyle.SetNdivisions(10, 'X')
# ROOT.gStyle.SetPadGridX(True)
ROOT.gStyle.SetPadGridY(True)
# ROOT.gStyle.SetGridWidth(1)
ROOT.gStyle.SetLegendFont(42)

# file = ROOT.TFile.Open('/afs/cern.ch/work/m/manzoni/beamspot/CMSSW_7_4_6_patch5/src/RecoVertex/BeamSpotProducer/test/BeamSpot_Run2015B_16July15_3p8T_250985_251883_newStartPar/beamspot_plots_251027_251883_per_iov.root')
# file = ROOT.TFile.Open('/afs/cern.ch/work/m/manzoni/beamspot/CMSSW_7_4_6_patch5/src/RecoVertex/BeamSpotProducer/test/BeamSpot_Run2015A_21July15_0T_246908_247644/beamspot_plots_246908_250932_per_iov.root')
# file = ROOT.TFile.Open('/afs/cern.ch/work/m/manzoni/beamspot/CMSSW_7_4_6_patch5/src/RecoVertex/BeamSpotProducer/test/BeamSpot_Run2015A_21July15_0T_246908_247644/beamspot_plots_246908_250932_per_iov_with_low_lumi.root')
# file = ROOT.TFile.Open('/afs/cern.ch/work/m/manzoni/beamspot/CMSSW_7_4_6_patch5/src/RecoVertex/BeamSpotProducer/test/BeamSpot_Run2015B_16July15_3p8T_plus_2p8T_250985_251883/beamspot_plots_251027_251883_per_iov.root')





# file = ROOT.TFile.Open('/afs/cern.ch/work/m/manzoni/beamspot/26nov/CMSSW_7_4_15_patch1/src/RecoVertex/BeamSpotProducer/test/eoyReReco/histos_post_merging_2015B.root')
# file = ROOT.TFile.Open('/afs/cern.ch/work/m/manzoni/beamspot/26nov/CMSSW_7_4_15_patch1/src/RecoVertex/BeamSpotProducer/test/eoyReReco/histos_post_merging_2015C.root')
# file = ROOT.TFile.Open('/afs/cern.ch/work/m/manzoni/beamspot/26nov/CMSSW_7_4_15_patch1/src/RecoVertex/BeamSpotProducer/test/eoyReReco/histos_post_merging_2015D.root')
# file = ROOT.TFile.Open('/afs/cern.ch/work/m/manzoni/beamspot/26nov/CMSSW_7_4_15_patch1/src/RecoVertex/BeamSpotProducer/test/eoyReReco/histos_post_merging.root')
# file = ROOT.TFile.Open('/afs/cern.ch/work/m/manzoni/beamspot/26nov/CMSSW_7_4_15_patch1/src/RecoVertex/BeamSpotProducer/test/eoyReReco/histos_post_merging_no_slopes.root')
# file = ROOT.TFile.Open('/afs/cern.ch/work/m/manzoni/beamspot/26nov/CMSSW_7_4_15_patch1/src/RecoVertex/BeamSpotProducer/test/eoyReReco/histos_post_merging_no_slopes_3p8T.root')
# file = ROOT.TFile.Open('histos_final_by_run.root')
# file = ROOT.TFile.Open('histos_final_by_fill.root')

# file = ROOT.TFile.Open('histos_final_by_run_2015A.root')
# file = ROOT.TFile.Open('histos_final_by_run_2015B.root')
# file = ROOT.TFile.Open('histos_final_by_run_2015C.root')
file = ROOT.TFile.Open('histos_final_by_run_2015D.root')

file.cd()

X          = file.Get('X'         )
Y          = file.Get('Y'         )
Z          = file.Get('Z'         )
sigmaZ     = file.Get('sigmaZ'    )
beamWidthX = file.Get('beamWidthX')
beamWidthY = file.Get('beamWidthY')
dxdz       = file.Get('dxdz'      )
dydz       = file.Get('dydz'      )

variables = [
    (X         , 'beam spot x [cm]'         ,  0.050 , 0.120 ),
    (Y         , 'beam spot y [cm]'         ,  0.050 , 0.120 ),
    (Z         , 'beam spot z [cm]'         , -10.   ,10.    ),
    (sigmaZ    , 'beam spot #sigma_{z} [cm]',  2.0   , 7.    ),
    (beamWidthX, 'beam spot #sigma_{x} [cm]',  0.000 , 0.020 ),
    (beamWidthY, 'beam spot #sigma_{y} [cm]',  0.000 , 0.020 ),
    (dxdz      , 'beam spot dx/dz [rad]'    , -1.e-3 , 1.e-3 ),
    (dydz      , 'beam spot dy/dz [rad]'    , -1.e-3 , 1.e-3 ),
]

def drawMyStyle(histo, options = '', title = '', byFill = True, byTime = False):
    
    histo.SetLineColor(ROOT.kGray)
    histo.SetLineWidth(1)
#     histo.SetLineStyle(3)

    histo.GetYaxis().SetTitle(var[1])
    histo.GetXaxis().SetTitle('')
    histo.GetYaxis().SetRangeUser(var[2], var[3])

    if byFill:
        labelByFill(histo)
        histo.GetXaxis().SetTitle('Fill')
    
    if byTime:
        labelByFill(histo)
        labelByTime(histo)

    histo.SetTitle('')
    histo.GetXaxis().SetTickLength(0.03)
    histo.GetYaxis().SetTickLength(0.01)
    histo.GetXaxis().SetTitleOffset(1.25)
    histo.GetYaxis().SetTitleOffset(0.6)
    histo.GetYaxis().SetTitleSize(0.06)
    histo.GetXaxis().SetTitleSize(0.06)
    histo.GetYaxis().SetLabelSize(0.04)
    histo.GetXaxis().SetLabelSize(0.06)
    histo.GetXaxis().SetNdivisions(10, True)

    histo.Draw(options)
  
    ROOT.TGaxis.SetMaxDigits(4)
    ROOT.TGaxis.SetExponentOffset(0.005, -0.05)
    ROOT.gPad.SetTicky()
    ROOT.gPad.Update()

def saveHisto(var):

    histo = var[0]

    histo0T, histo3p8T, histo2p8T, histoOther = splitByMagneticField(
        histo, 
        json    = True, 
        json3p8 = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/DCSOnly/json_DCSONLY.txt', 
        json2p8 = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/DCSOnly/json_DCSONLY_2.8T.txt', 
        json0   = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/DCSOnly/json_DCSONLY_0T.txt',
    )
    
    histo0T   .SetMarkerColor(ROOT.kRed   + 1)
    histo3p8T .SetMarkerColor(ROOT.kBlack    )
    histo2p8T .SetMarkerColor(ROOT.kGreen + 1)

    cloneHisto0T    = histo0T   .Clone()
    cloneHisto3p8T  = histo3p8T .Clone()
    cloneHisto2p8T  = histo2p8T .Clone()

    cloneHisto0T   .SetMarkerSize(3.)
    cloneHisto3p8T .SetMarkerSize(3.)
    cloneHisto2p8T .SetMarkerSize(3.)
  
    cloneHisto0T   .SetLineColor(ROOT.kGray + 2)
    cloneHisto3p8T .SetLineColor(ROOT.kGray + 2)
    cloneHisto2p8T .SetLineColor(ROOT.kGray + 2)
    
    byFill = True
    byTime = False

    toplot = [hist for hist in [histo0T, histo3p8T, histo2p8T] if hist.GetEntries() > 0]
        
    for j, hist in enumerate(toplot):
        drawMyStyle(hist, options = 'SAME'*(j!=0), byFill = byFill, byTime = byTime)

    for hist in [histo0T, histo3p8T, histo2p8T, histoOther]:
        hist.SetTickLength(0, 'X')
        
    ROOT.gPad.Update()
    
    # SetNdivisions() does not work when bin labels are changed
    # thank you ROOT
    # https://root.cern.ch/phpBB3/viewtopic.php?t=6901
    f1 = ROOT.TF1('f1', 'x', 0, 16)
    labels = ROOT.TGaxis(ROOT.gPad.GetUxmin(), ROOT.gPad.GetUymin(), 
                         ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymin(), 
                         'f1', 520)
    labels.SetLabelSize(0)
    labels.Draw()
    
    CMS_lumi(ROOT.gPad, 4, 0)
    ROOT.gPad.Update()
    
    leg = ROOT.TLegend( 0.902, 0.5, 1.0, 0.75 )
    leg.SetFillColor(ROOT.kWhite)
    leg.SetLineColor(ROOT.kWhite)
    leg.AddEntry(cloneHisto3p8T , 'B = 3.8 T' , 'EP')
    leg.AddEntry(cloneHisto0T   , 'B = 0 T'   , 'EP')
    leg.AddEntry(cloneHisto2p8T , 'B = 2.8 T' , 'EP')
#     leg.AddEntry(histoOther, 'magnet ramping', 'F')
    leg.Draw('SAME')

    ROOT.gPad.Print('BS_plot_full_by_fill_run2015D_%s.pdf' %histo.GetName())

c1 = ROOT.TCanvas('', '', 3000, 1000)
for var in variables:
    saveHisto(var)


