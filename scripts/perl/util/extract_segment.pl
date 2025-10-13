#!/usr/bin/perl

# Description, extract a segment that start with a given pattern and ends with a given pattern from a text file.

# Author Yosi Izaq

use strict;


if (@ARGV != 3){
  help();
  exit(-1);
}
sub help(){

my $message =
  "\n".
  "\tThis script extracts from a text file all segments.\n".
  "\t start with a given pattern and end with a given pattern.\n";

my $usage  = "usage: extract_segment.pl <file> <pattern 1> <pattern 2> .... \n";

print $message, "\n\t", $usage;

}

my $file_name	= shift;
my $pattern1	= shift;
my $pattern2	= shift;

print "Args: $file_name $pattern1 $pattern2 \n.";

open(FH, "+< $file_name")                 or die "Opening $file_name:  $!";
my @ARRAY = <FH>;

my $start_segment = 0;

foreach (@ARRAY){
	#print $_;

	if (/${pattern1}/){
		$start_segment = 1;
		print "\t<<< START SEGMENT >>>\n";
		print $_;
		#print "found start pattern at: $_\n.";
		next;	#Skip checking the line for second pattern when first pattern found
				# This will allow for a segment to be found in such cases (otherwise nothing is printed)

	}
	

	if (/${pattern2}/){
		if ($start_segment == 1){
			print $_;
			print "\t<<< END SEGMENT >>>\n\n";
		}

		$start_segment = 0;

	}
	
	if ($start_segment == 1 ){
		print $_
	}
}#//foreach
