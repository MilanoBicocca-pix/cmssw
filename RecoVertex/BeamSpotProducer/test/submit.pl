#!/usr/bin/perl

use Cwd ;

$v    = $ARGV[0] ;
$pwd  = cwd() ;
$BASE = "/afs/cern.ch/user/m/menasce/beamspot/CMSSW_7_4_0_pre6/src/RecoVertex/BeamSpotProducer" ;

$cmd = "rm ${v}Minuit.log" ;
&exec("$cmd") ;

my $cmd = "cd $BASE && scram b " ;
&exec("$cmd") ;

my $cmd = "cd ${BASE}/test && date > ${v}Minuit.log && cmsRun analyze_d0_phi_cfg.py >> ${v}Minuit.log && date >> ${v}Minuit.log" ;
&exec("$cmd") ;

$cmd = "mv BeamFit_124120_vpv4_Run1.txt BeamFit_124120_vpv4_Run1_${v}Minuit.txt" ;
&exec("$cmd") ;

#==================================================================
sub exec 
{
 my $cmd = shift ;
 print("$cmd \n") ;
 open(PIPE,"$cmd |") ;
 while(<PIPE>) 
 {
  print ;
 }
 close(PIPE) ;
}
