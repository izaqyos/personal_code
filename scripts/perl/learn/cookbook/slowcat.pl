#!/usr/bin/perl 
#===============================================================================
#
#         FILE: slowcat.pl
#
#        USAGE: ./slowcat.pl  
#
#  DESCRIPTION: :
## slowcat - emulate a   s l o w   line printer
#  # usage: slowcat [-DELAY] [files ...]
#      OPTIONS: ---
# REQUIREMENTS: ---
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: Yosi Izaq
# ORGANIZATION: 
#      VERSION: 1.0
#      CREATED: 04/09/15 11:33:21
#     REVISION: ---
#===============================================================================

use strict;
use warnings;

my $delay = ($ARGV[0] =~ /^-((\d\.)?\d+)/ ) ? (shift, $1) : 1;
#print "delay is $delay \n";
while (<>)
{
	for (split(//,$_))
	{
		print;
		select(undef,undef,undef,0.005*$delay);
	}
}
