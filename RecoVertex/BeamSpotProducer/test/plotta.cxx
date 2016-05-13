{
 gROOT->Reset() ;
 TFile f("BeamFit.root") ;
 
 TCanvas c("c","c",1000,800) ;
 c.Divide(3,5) ;
 
 string cutm = "lumi == 36 || lumi == 97 || lumi == 133 || lumi == 161" ;
 
 c.cd(1)  ; mytree->Draw("pvxe>>dataErrX(1000,0,.04)","") ;
 c.cd(2)  ; mytree->Draw("pvye>>dataErrY(1000,0,.04)","") ;
 c.cd(3)  ; mytree->Draw("pvze>>dataErrZ(1000,0,.04)","") ;

 c.cd(4)  ; mytree->Draw("vx>>dataPosX(1000,-.2,.2)","") ;
 c.cd(5)  ; mytree->Draw("vy>>dataPosY(1000,-.2,.2)","") ;
 c.cd(6)  ; mytree->Draw("z0>>dataPosZ(1000,-20,20)","") ;
 
 c.cd(7)  ; fitResults->Draw("xErr>>beamWidthX(1000,0,.0004)","") ;
 c.cd(8)  ; fitResults->Draw("yErr>>beamWidthY(1000,0,.0004)","") ;
 c.cd(9)  ; fitResults->Draw("zErr>>beamWidthZ(1000,0,.04 )","") ;
 
 c.cd(10) ; fitResults->Draw("x>>fitPosX(1000,-.2,.2)","") ;
 c.cd(11) ; fitResults->Draw("y>>fitPosY(1000,-.2,.2)","") ;
 c.cd(12) ; fitResults->Draw("z>>fitPosZ(1000,-20,20)","") ;
 
 c.cd(13) ; fitResults->Draw("dxdz>>fitdxdz(1000,-.002,.002)","") ;
 c.cd(14) ; fitResults->Draw("dydz>>fitdydz(1000,-.002,.002)","") ;
}
