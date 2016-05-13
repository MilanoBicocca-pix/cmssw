#!/usr/bin/perl

@files = `ls result_BeamFit_Run272775_errorScale\*.txt` ;

foreach $f (@files) 
{
 chomp($f) ;
 $f =~ m/_errorScale_(.+)?\.txt/ ;
 print(" $1 \t") ;
 open(IN,"$f") ;
 while(<IN>)
 {
  if( m/LumiRange\s+(\d+)\s+/ )   {$lumi = $1 ;}
  if( m/Type\s+((\+|-)*\d+)\s+/ ) {$type = $1; $data{$f}{$lumi}{"TP"} = $1 ;}
  if( m/X0\s+(.+)/ )              {	       $data{$f}{$lumi}{"X0"} = $1 ;}
  if( m/Y0\s+(.+)/ )              {	       $data{$f}{$lumi}{"Y0"} = $1 ;}
  if( m/Z0\s+(.+)/ )              {	       $data{$f}{$lumi}{"Z0"} = $1 ;}
 }
}
print("\n") ;

foreach $kf (keys %data)
{
 foreach $kl (sort {$a <=> $b} keys %{$data{$kf}})
 {
  $conv{$kl}{$kf} = $data{$kf}{$kl}{"TP"} ;
  if( $data{$kf}{$kl}{"TP"} == "2" )
  {
   $succ{$kf}++ ;
  }
  else
  {
   $fail{$kf}++ ;
  } 
#  print("$kf | $kl | $data{$kf}{$kl}{\"TP\"}\n") ;
 }
}

foreach $kl (sort {$a <=> $b} keys %conv)
{
 print("Lumi: $kl ") ;
 foreach $kf (sort {$a <=> $b} keys %{$conv{$kl}})
 {
  $type = $conv{$kl}{$kf} ;
  print("$type\t") ;
 }
 print("\n") ;
}

print("Succ:    ") ;
foreach $kf (sort {$a <=> $b} keys %data)
{
 print("$succ{$kf}\t") ;
}
print("\nFail:   ") ;
foreach $kf (sort {$a <=> $b} keys %data)
{
 print("$fail{$kf}\t") ;
}
print("\n") ;
