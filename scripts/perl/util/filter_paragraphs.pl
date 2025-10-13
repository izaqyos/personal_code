#!/usr/bin/perl

# Author: Yosi Izaq
# Description: Three parameters, file, anchor1 and anchor2, the script will
#  filter the paragraphs that start with anchor1 and end with anchor2.

use strict;

if (@ARGV != 3){
  help();
}
else{
    filter(@ARGV);
}

sub help{

print "usage filter_paragraphs.pl file anchor1 anchor2\n";
print "Description: Three parameters, file, anchor1 and anchor2, the script will filter the paragraphs that start with anchor1 and end with anchor2.";
}


sub filter{
my $file_name = "$_[0]";
my $anchor1 = "$_[1]";
my $anchor2 = "$_[2]";
my $found = 0;
my @Paragraph;
print "Arguments. file, $file_name; anchor1, $anchor1; anchor2, $anchor2;\n";

#open for read
open(FILE, "< $file_name") or die "can't open file $file_name. $!";
my @lines = <FILE>;

#print @lines;
my $line_num = 0;
foreach  (@lines){

	#anchor 1
	if (/$anchor1/){
		#print "Found anchor1: $_\n";
		$found = 1;
	}

	#fill buffer with potentially matched paragraph lines
	if ($found == 1)
	{
		#print "filling potentially matched paragraph lines.\n";
		push @Paragraph, $_;

	}

	#Found closing anchor, flush matched paragraph
	#anchor 2
	if (/$anchor2/){
		#print "Found anchor2: $_\n";
		print @Paragraph, "\n";
		@Paragraph = ();
		$found = 0;
	}

	
  }
close(FILE);

}



