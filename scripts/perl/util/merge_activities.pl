#!/usr/bin/perl
#
use strict;
my $files = shift;
#
#print "file list in: $files";


open(FILE, "< $files") or die "can't open file $files. $!";
my @lines = <FILE>;

foreach  (@lines) {
	chomp $_;
#print  $_;
# Add command for checkout files

# remove echo to check out file	
#system ("cleartool co  $_");

# Add command for merge files
#print ("executing ~/tkdiff.tcl /cygdrive/j/ismg_israel_acs/Acs/$_ /cygdrive/h/ismg_israel_acs/Acs/$_\n"); 
#system ("~/tkdiff.tcl /cygdrive/j/ismg_israel_acs/Acs/$_ /cygdrive/h/ismg_israel_acs/Acs/$_");
# Add command for copy merged files over original

  if (/(.*)(\/\w+)\.[h|cpp]/){
		print "path: $1, file name is $2\n";
  }

close FILE;

}
