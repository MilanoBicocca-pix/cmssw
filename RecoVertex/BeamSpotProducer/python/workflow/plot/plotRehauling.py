import ROOT
from PlotStyle import PlotStyle
from CMSStyle import CMS_lumi
from RecoVertex.BeamSpotProducer.workflow.utils.fillRunDict import labelByTime, splitByMagneticField

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
ROOT.gStyle.SetNdivisions(510, 'XYZ')
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
file = ROOT.TFile.Open('/afs/cern.ch/work/m/manzoni/beamspot/eoy0T/CMSSW_7_4_15_patch1/src/RecoVertex/BeamSpotProducer/test/histos_post_merging_no_slopes.root')

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
# Run 2015B
(X         , 'beam spot x [cm]'         ,  0.050 , 0.120 ),
(Y         , 'beam spot y [cm]'         ,  0.050 , 0.120 ),
(Z         , 'beam spot z [cm]'         , -10.   ,10.    ),
(sigmaZ    , 'beam spot #sigma_{z} [cm]',  2.0   , 7.    ),
(beamWidthX, 'beam spot #sigma_{x} [cm]',  0.000 , 0.020 ),
(beamWidthY, 'beam spot #sigma_{y} [cm]',  0.000 , 0.020 ),
(dxdz      , 'beam spot dx/dz [rad]'    , -1.e-3 , 1.e-3 ),
(dydz      , 'beam spot dy/dz [rad]'    , -1.e-3 , 1.e-3 ),
# Run 2015A
# (X         , 'beam spot x [cm]'         ,  0.055 , 0.072 ),
# (Y         , 'beam spot y [cm]'         ,  0.090 , 0.105 ),
# (Z         , 'beam spot z [cm]'         , -3.    , 0.    ),
# (sigmaZ    , 'beam spot #sigma_{z} [cm]',  3.6   , 5.0   ),
# (beamWidthX, 'beam spot #sigma_{x} [cm]',  0.001 , 0.0101),
# (beamWidthY, 'beam spot #sigma_{y} [cm]',  0.001 , 0.0101),
# (dxdz      , 'beam spot dx/dz [rad]'    , -1.e-4 , 4.e-4 ),
# (dydz      , 'beam spot dy/dz [rad]'    , -1.e-4 , 4.e-4 ),
]

def drawMyStyle(histo, options = '', title = ''):
    
    histo.SetLineColor(ROOT.kGray)
    histo.SetLineWidth(1)
#     histo.SetLineStyle(3)

    histo.GetYaxis().SetTitle(var[1])
    histo.GetXaxis().SetTitle('')
    histo.GetYaxis().SetRangeUser(var[2], var[3])

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

    histo0T, histo3p8T, histo2p8T, histoOther = splitByMagneticField(histo)
    
    histo0T   .SetMarkerColor(ROOT.kRed   ) #+ 2)
    histo3p8T .SetMarkerColor(ROOT.kBlack ) #   )
    histo2p8T .SetMarkerColor(ROOT.kGreen ) #+ 2)
    histoOther.SetMarkerColor(ROOT.kBlue  ) #+ 2)

    histo0T   .SetFillColor(ROOT.kRed   ) #+ 2)
    histo3p8T .SetFillColor(ROOT.kBlack ) #   )
    histo2p8T .SetFillColor(ROOT.kGreen ) #+ 2)
    histoOther.SetFillColor(ROOT.kBlue  ) #+ 2)

    # for 0T
    histoOther.SetMarkerColor(ROOT.kRed  ) #+ 2)
    histoOther.SetFillColor(ROOT.kRed  ) #+ 2)

    
    drawMyStyle(histo0T                     )
    drawMyStyle(histo3p8T , options = 'SAME')
    drawMyStyle(histo2p8T , options = 'SAME')
    drawMyStyle(histoOther, options = 'SAME')
    
    CMS_lumi(ROOT.gPad, 4, 0)
    ROOT.gPad.Update()

    leg = ROOT.TLegend( 0.902, 0.5, 1.0, 0.75 )
    leg.SetFillColor(ROOT.kWhite)
    leg.SetLineColor(ROOT.kWhite)
    leg.AddEntry(histo3p8T , '3.8 T runs'    , 'F')
    leg.AddEntry(histo0T   , '0 T runs'      , 'F')
    leg.AddEntry(histo2p8T , '2.8 T runs'    , 'F')
    leg.AddEntry(histoOther, 'magnet ramping', 'F')
#     leg.Draw('SAME')


#     ROOT.gPad.Print('BS_plot_246908_250932_%s.pdf' %histo.GetName())
#     ROOT.gPad.Print('BS_plot_251027_251883_%s.pdf' %histo.GetName())

#     ROOT.gPad.Print('BS_plot_run2015B_251027_252126_%s.pdf' %histo.GetName())
#     ROOT.gPad.Print('BS_plot_run2015C_254227_256464_%s.pdf' %histo.GetName())
#     ROOT.gPad.Print('BS_plot_run2015D_256630_260627_%s.pdf' %histo.GetName())
#     ROOT.gPad.Print('BS_plot_run2015_251027_260627_%s_3p8T.pdf' %histo.GetName())
#     ROOT.gPad.Print('BS_plot_run2015_251027_260627_%s.pdf' %histo.GetName())
    ROOT.gPad.Print('BS_plot_run0T_2015_251027_260627_%s.pdf' %histo.GetName())


# PlotStyle.initStyle()

c1 = ROOT.TCanvas('', '', 3000, 1000)
for var in variables:
    saveHisto(var)


