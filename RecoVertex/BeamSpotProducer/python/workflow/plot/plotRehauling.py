import ROOT
from PlotStyle import PlotStyle
from CMSStyle import CMS_lumi

ROOT.gROOT.SetBatch(False)
ROOT.gROOT.Reset()
ROOT.gROOT.SetStyle('Plain')
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(1111)
ROOT.gStyle.SetPadLeftMargin(0.1)
ROOT.gStyle.SetPadBottomMargin(0.15)
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

# file = ROOT.TFile.Open('/afs/cern.ch/work/m/manzoni/beamspot/CMSSW_7_4_6_patch5/src/RecoVertex/BeamSpotProducer/test/BeamSpot_Run2015B_16July15_3p8T_250985_251883_newStartPar/beamspot_plots_251027_251883_per_iov.root')
# file = ROOT.TFile.Open('/afs/cern.ch/work/m/manzoni/beamspot/CMSSW_7_4_6_patch5/src/RecoVertex/BeamSpotProducer/test/BeamSpot_Run2015A_21July15_0T_246908_247644/beamspot_plots_246908_250932_per_iov.root')
file = ROOT.TFile.Open('/afs/cern.ch/work/m/manzoni/beamspot/CMSSW_7_4_6_patch5/src/RecoVertex/BeamSpotProducer/test/BeamSpot_Run2015A_21July15_0T_246908_247644/beamspot_plots_246908_250932_per_iov_with_low_lumi.root')
# file = ROOT.TFile.Open('/afs/cern.ch/work/m/manzoni/beamspot/CMSSW_7_4_6_patch5/src/RecoVertex/BeamSpotProducer/test/BeamSpot_Run2015B_16July15_3p8T_plus_2p8T_250985_251883/beamspot_plots_251027_251883_per_iov.root')
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
# (X         , 'beam spot x [cm]'         ,  0.076 , 0.082 ),
# (Y         , 'beam spot y [cm]'         ,  0.094 , 0.104 ),
# (Z         , 'beam spot z [cm]'         , -3.    , 0.    ),
# (sigmaZ    , 'beam spot #sigma_{z} [cm]',  4.05  , 4.55  ),
# (beamWidthX, 'beam spot #sigma_{x} [cm]',  0.0012, 0.0018),
# (beamWidthY, 'beam spot #sigma_{y} [cm]',  0.0010, 0.0016),
# (dxdz      , 'beam spot dx/dz [rad]'    ,  5.e-5 , 20.e-5),
# (dydz      , 'beam spot dy/dz [rad]'    ,  5.e-5 , 20.e-5),
# Run 2015A
(X         , 'beam spot x [cm]'         ,  0.055 , 0.072 ),
(Y         , 'beam spot y [cm]'         ,  0.090 , 0.105 ),
(Z         , 'beam spot z [cm]'         , -3.    , 0.    ),
(sigmaZ    , 'beam spot #sigma_{z} [cm]',  3.6   , 5.0   ),
(beamWidthX, 'beam spot #sigma_{x} [cm]',  0.001 , 0.0101),
(beamWidthY, 'beam spot #sigma_{y} [cm]',  0.001 , 0.0101),
(dxdz      , 'beam spot dx/dz [rad]'    , -1.e-4 , 4.e-4 ),
(dydz      , 'beam spot dy/dz [rad]'    , -1.e-4 , 4.e-4 ),
]

def saveHisto(var):

    histo = var[0]
    histo.GetYaxis().SetTitle(var[1])
    histo.GetXaxis().SetTitle('LHC Fill')
    histo.GetYaxis().SetRangeUser(var[2], var[3])

    histo.SetTitle('')
    histo.Draw()
    CMS_lumi(ROOT.gPad, 4, 0)
    histo.GetXaxis().SetTickLength(0.03)
    histo.GetYaxis().SetTickLength(0.01)
    histo.GetXaxis().SetTitleOffset(1.25)
    histo.GetYaxis().SetTitleOffset(0.6)
    histo.GetYaxis().SetTitleSize(0.06)
    histo.GetXaxis().SetTitleSize(0.06)
    histo.GetYaxis().SetLabelSize(0.04)
    histo.GetXaxis().SetLabelSize(0.06)
    histo.GetXaxis().SetNdivisions(10, True)
  
    ROOT.TGaxis.SetMaxDigits(4)
    ROOT.TGaxis.SetExponentOffset(0.005, -0.05)
    ROOT.gPad.SetTicky()
    ROOT.gPad.Update()

    # shaded area
    p0 = ROOT.TPad('p0', 'p0', 0.3, 0.151, 0.61, 0.9) # Run 2015A, low PU
#     p0 = ROOT.TPad('p0', 'p0', 0.417, 0.151, 0.5372, 0.9) # Run 2015B, 2.8T
    p0.SetLineWidth(1)
    p0.SetFillColor(ROOT.kGray)
    p0.SetFillStyle(3345)
    ROOT.gStyle.SetHatchesSpacing(4)
    ROOT.gStyle.SetHatchesLineWidth(1)
    p0.Draw()

    ROOT.gPad.Update()
    ROOT.gPad.Modified()


    ROOT.gPad.Print('BS_plot_246908_250932_%s.pdf' %histo.GetName())
#     ROOT.gPad.Print('BS_plot_251027_251883_%s.pdf' %histo.GetName())
    

# PlotStyle.initStyle()

c1 = ROOT.TCanvas('', '', 3000, 1000)
for var in variables:
    saveHisto(var)


