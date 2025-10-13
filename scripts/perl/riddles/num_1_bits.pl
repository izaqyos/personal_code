#!/usr/bin/perl 
#===============================================================================
#
#         FILE: num_1_bits.pl
#
#        USAGE: ./num_1_bits.pl  
#
#  DESCRIPTION: 
#
#      OPTIONS: ---
# REQUIREMENTS: ---
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: YOUR NAME (), 
# ORGANIZATION: 
#      VERSION: 1.0
#      CREATED: 04/14/15 15:22:54
#     REVISION: ---
#===============================================================================

use strict;
use warnings;

sub ret_num_1_bits
{

    my $num = $_;
    my $bits = 0;
    
    while ($num >0)
    {
		$num = $num & ($num--) ;    
		$bits++;
    }

	$bits;

}
while (<>)
{
	print "-"x32,"\n";
	print "processing num: $_";
	print "number of bits: ",&ret_num_1_bits($_), " \n";
}
	print "-"x32,"\n";

