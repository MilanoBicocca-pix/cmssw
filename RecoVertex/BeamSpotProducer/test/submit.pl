#!/usr/bin/perl

use Cwd ;

if( scalar @ARGV < 3 )
{
 print("Usage: ./submit [(Old|New)] [(Data|Mc)] [testType]\n\n") ;
 exit(0) ;
}

$v    = $ARGV[0] ; # (Old|New) 
$t    = $ARGV[1] ; # (Data|Mc)
$T    = $ARGV[2] ; # (testType)

if($t  eq "Data")
{
 $Run = 203991 ;
}
else
{
 $Run = 1 ;
}

$pwd  = cwd() ;
$BASE = "/afs/cern.ch/user/m/menasce/beamspot/CMSSW_7_4_0_pre6/src/RecoVertex/BeamSpotProducer" ;

unless( -e "$T" )
{
  $cmd = "mkdir $T" ;
  &exec("$cmd") ;
}

$cmd = "cd $T ; rm -f ${v}Minuit_${t}.log" ;
&exec("$cmd") ;

my $cmd = "cd $BASE && scram b " ;
&exec("$cmd") ;

my $cmd = "cd ${BASE}/test && date > ${v}Minuit_${t}.log && cmsRun analyze_d0_phi_cfg.py >> ${v}Minuit_${t}.log && date >> ${v}Minuit_${t}.log" ;
&exec("$cmd") ;

$cmd = "mv BeamFit_124120_vpv4_Run${Run}.txt ${T}/BeamFit_${v}Minuit_${t}.txt" ;
           BeamFit_124120_vpv4_Run203991.txt
&exec("$cmd") ;

$cmd = "mv run124120_all_vpv3.root ${T}/BeamFit_${v}Minuit_${t}.root" ;
&exec("$cmd") ;

$cmd = "mv ${v}Minuit_${t}.log ${T}/${v}Minuit_${t}.log" ;
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
