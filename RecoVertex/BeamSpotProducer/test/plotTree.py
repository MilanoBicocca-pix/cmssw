#!/usr/bin/env python
import ROOT
from ROOT import TTree, TFile, AddressOf, gROOT, TChain, TGraphErrors, TCanvas, TLegend, TH1F, gPad, gStyle
from array import array

gStyle.SetTitleAlign(23)
gStyle.SetOptStat(2220)
# gStyle.SetOptStat('emr')
gStyle.SetPadLeftMargin(0.17)
gStyle.SetPadBottomMargin(0.15)

class bs(object):
  def __init__(self, event):
     self.lumi      = event.beginLumi        
     self.x         = event.x        
     self.y         = event.y        
     self.z         = event.z        
     self.xErr      = event.xErr          
     self.yErr      = event.yErr      
     self.zErr      = event.zErr      
     self.sigmaZ    = event.sigmaZ      
     self.sigmaZErr = event.sigmaZErr
     self.dxdz      = event.dxdz     
     self.dxdzErr   = event.dxdzErr  
     self.dydz      = event.dydz     
     self.dydzErr   = event.dydzErr  
     self.widthX    = event.widthX   
     self.widthY    = event.widthY   
     self.widthXErr = event.widthXErr
     self.widthYErr = event.widthYErr


def getResults(tree, lumi_bs):

  for i, ev in enumerate(tree):
    #if i > 100000: break
    try:
      lumi_bs[ev.beginLumi]
    except:
      lumi_bs[ev.beginLumi] = []  

    mybs = bs(ev)
          
    lumi_bs[ev.beginLumi].append(mybs)




if __name__ == '__main__':

#   f_old = TFile('run207231_StreamExpress_addCombinedResultsTree.root','READ')
#   f_new = TFile('run207231_PCLReplay_addCombinedResultsTree.root','READ')
  f_old = TFile('run207231_StreamExpress_Lumi500_900_addCombinedResultsTree.root','READ')
  f_new = TFile('run207231_PCLReplay_Lumi500_900_addCombinedResultsTree.root','READ')

  t_old = f_old.Get("combinedFitResults")
  t_new = f_new.Get("combinedFitResults")

  print t_old.GetEntries()
  print t_new.GetEntries()

  lumi_bs_se  = { }
  lumi_bs_pcl = { }

  getResults(t_old, lumi_bs_se )
  getResults(t_new, lumi_bs_pcl)

  variables = [
    ('x'      , 'xErr'     , 'LS', 'x [cm]' , (  0.066  , 0.0705  ), (0.69, 0.89, 0.55, 0.65), ( -0.001  , 0.001  ), False),
	('y'      , 'yErr'     , 'LS', 'y [cm]' , (  0.0605 , 0.064   ), (0.69, 0.89, 0.55, 0.65), ( -0.001  , 0.001  ), False),
	('z'      , 'zErr'     , 'LS', 'z [cm]' , (  -0.3   , 0.35    ), (0.69, 0.89, 0.55, 0.65), ( -0.5    , 0.5    ), False),
	('sigmaZ' , 'sigmaZErr', 'LS', 'sigmaZ' , (  4      , 6       ), (0.69, 0.89, 0.55, 0.65), ( -0.5    , 0.5    ), False),
	('dxdz'   , 'dxdzErr'  , 'LS', 'dxdz'   , ( -0.1E-3 , 0.3E-3  ), (0.69, 0.89, 0.55, 0.65), ( -0.0005 , 0.0005 ),  True),
	('dydz'   , 'dydzErr'  , 'LS', 'dydz'   , ( -0.2E-3 , 0.15E-3 ), (0.69, 0.89, 0.55, 0.65), ( -0.0005 , 0.0005 ),  True),
	('widthX' , 'widthXErr', 'LS', 'widthX' , (  0      , 0.004   ), (0.69, 0.89, 0.55, 0.65), ( -0.5    , 0.5    ), False),
	('widthY' , 'widthYErr', 'LS', 'widthY' , (  0.0012  , 0.0022 ), (0.69, 0.89, 0.55, 0.65), ( -0.5    , 0.5    ), False)
  ]

 
  for ivar in variables: 
    thelist_var_se      = []
    thelist_var_pcl     = []
    thelist_err_se      = []
    thelist_err_pcl     = []
    thelist_lumi_se     = []
    thelist_lumi_pcl    = []
    thelist_lumierr_se  = []
    thelist_lumierr_pcl = []
    for ilumi in lumi_bs_se:
      thelist_var_se  .append( getattr( lumi_bs_se [ilumi][0],ivar[0] ))
      thelist_err_se  .append( getattr( lumi_bs_se [ilumi][0],ivar[1] ))
      thelist_lumi_se .append( ilumi)
      thelist_lumierr_se.append( 0.5)
      
      
    for ilumi in lumi_bs_pcl:
      thelist_var_pcl .append( getattr( lumi_bs_pcl[ilumi][0],ivar[0] ))
      thelist_err_pcl .append( getattr( lumi_bs_pcl[ilumi][0],ivar[1] ))
      thelist_lumi_pcl.append( ilumi)
      thelist_lumierr_pcl.append( 0.5)
   

    thevar_se      = array ('d', thelist_var_se     )
    theerr_se      = array ('d', thelist_err_se     )
    thelumi_se     = array ('d', thelist_lumi_se    )
    thelumierr_se  = array ('d', thelist_lumierr_se )
    thevar_pcl     = array ('d', thelist_var_pcl    )
    theerr_pcl     = array ('d', thelist_err_pcl    )
    thelumi_pcl    = array ('d', thelist_lumi_pcl   )
    thelumierr_pcl = array ('d', thelist_lumierr_pcl)

    # eval the % difference 
    thediff    = {}
    thedifferr = []
    for ls in lumi_bs_se.keys():
      if ls in lumi_bs_pcl.keys():
        thelsdiff    =   getattr( lumi_bs_se[ls][0],ivar[0]) - getattr(lumi_bs_pcl[ls][0],ivar[0])     
        thediff[ls]  = thelsdiff
        thedifferr.append( min (getattr( lumi_bs_se[ls][0],ivar[1]) , getattr( lumi_bs_pcl[ls][0],ivar[1])) )  

    thelumi_array    = array ('d', thediff.keys()                      )
    thediff_array    = array ('d', thediff.values()                    )
    thelumierr_array = array ('d', [0.5 for i in range(len(thediff)) ] )
    thedifferr_array = array ('d', thedifferr                          )
        
    histo_name = 'hdiff_' + ivar[0]
    hdiff   = TH1F (histo_name, histo_name, 100, -5, 5)
    for i in thediff_array:
      hdiff.Fill(i)
    hdiff.SetTitle('')
    hdiff.SetLineColor(ROOT.kBlack)
    hdiff.GetXaxis().SetTitle(ivar[0] + '  (SE - Replay)')
    hdiff.GetYaxis().SetTitle('# LS')


    g_se = TGraphErrors(len(thelumi_se), thelumi_se, thevar_se, thelumierr_se, theerr_se)
    g_se.SetMarkerStyle(23)
    g_se.SetMarkerSize(0.5)
    g_se.GetYaxis().SetTitleOffset(2.2)
    g_se.GetYaxis().SetTitle(ivar[3])
    g_se.GetXaxis().SetTitle("LS")
    g_se.SetTitle('Run 207231')
    
    g_se.GetYaxis().SetRangeUser( ivar[4][0] , ivar[4][1] )

    g_pcl = TGraphErrors(len(thelumi_pcl), thelumi_pcl, thevar_pcl, thelumierr_pcl, theerr_pcl)
    g_pcl.SetMarkerStyle(23)
    g_pcl.SetMarkerSize(0.5)
    g_pcl.SetMarkerColor(2)
    g_pcl.SetLineColor(2)

    c = TCanvas ('','', 600, 900)
    stackPad = ROOT.TPad('stackPad', 'stackPad', 0.,  .3, 1., 1.  , 0, 0)  
    ratioPad = ROOT.TPad('ratioPad', 'ratioPad', 0., 0. , 1.,  .38, 0, 0)  

    c.cd()
    stackPad.Draw()
    ratioPad.Draw()
    
    stackPad.cd()
    stackPad.SetBottomMargin(0.2)
    stackPad.SetGridx(True)
    g_se .Draw("AP")
    g_pcl.Draw("P" )
  
    l = TLegend(0.7,0.76,0.88,0.88)
    l.SetBorderSize(0)
    l.AddEntry(g_se , "StreamExpress", "pel")
    l.AddEntry(g_pcl, "Replay"       , "pel")
  #   l.AddEntry(g_old, "AlcaBeamSpotProducer"   , "pel")
  #   l.AddEntry(g_new, "BeamSpotProducer"       , "pel")
    l.Draw()


    ratioPad.cd()
    ratioPad.SetGridx(True)
    ratioPad.SetGridy(True)
    ratioPad.SetBottomMargin(0.2)

    g_diff = TGraphErrors(len(thelumi_array), thelumi_array, thediff_array, thelumierr_array, thedifferr_array)
    g_diff.SetMarkerStyle(23)
    g_diff.SetMarkerSize(0.5)
    g_diff.GetYaxis().SetTitle('SE - Replay')
    g_diff.GetXaxis().SetTitle("LS")
    g_diff.SetTitle('')
    g_diff.GetYaxis().SetRangeUser( ivar[6][0],ivar[6][1])
    g_diff.Draw("AP")

    g_diff.GetYaxis().SetNdivisions(6)
    g_diff.GetYaxis().SetLabelSize(0.06)
    g_diff.GetXaxis().SetLabelSize(0.06)
    g_diff.GetYaxis().SetTitleSize(0.06)
    g_diff.GetXaxis().SetTitleSize(0.06)
    g_diff.GetYaxis().SetTitleOffset(1.)

    c.SaveAs("compare" + ivar[0] + "_StreamExpress_Replay_lumi500_900.pdf")



    c2 = TCanvas ('c2','c2', 600, 600)
    c2.cd()
    hdiff.SetTitle('Run 207231, LS 500-900')
    hdiff.Draw()

    c2.Update()
    c2.Modified()
    stats = gPad.GetPrimitive('stats')
    print 'stats', stats
    stats.SetBorderSize(0)
    stats.SetY1NDC(0.74)
    stats.SetY2NDC(0.89)
    stats.SetX1NDC(0.65)
    stats.SetX2NDC(0.89)
#     c2.SaveAs('residual' + ivar[0] + '.pdf')

