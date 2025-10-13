#!/usr/bin/perl 
#===============================================================================
#
#         FILE: reverse.pl
#
#        USAGE: ./reverse.pl  
#
#  DESCRIPTION: 
#
#      OPTIONS: ---
# REQUIREMENTS: ---
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: Yosi Izaq
# ORGANIZATION: 
#      VERSION: 1.0
#      CREATED: 04/08/15 18:15:55
#     REVISION: ---
#===============================================================================

use strict;
use warnings;


my $str = "This is a test string";
print "Str is: $str \n";
my $rstr = reverse($str);
print "Reverse Str is: ", $rstr," \n";
my $rwstr = join (" ", reverse( split(" ", $str)));
print "Reverse words Str is: ", $rwstr," \n";


