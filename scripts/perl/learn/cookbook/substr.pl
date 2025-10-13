#!/usr/bin/perl 
#===============================================================================
#
#         FILE: substr.pl
#
#        USAGE: ./substr.pl  
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
#      CREATED: 04/06/15 12:25:56
#     REVISION: ---
#===============================================================================

use strict;
use warnings;

my $str = "This is a test string";

print "Extract substring\n";
print "String prefix ", substr($str, 0, 8), "\n";
print "String suffix ", substr($str, 8, length($str) -1), "\n";

print "Change substring\n";
substr($str, 0, 4) = "THIS";
print "Modified string ", $str, "\n";

print "Change substring 2nd time\n";
substr($str, 0, 4,  "thhiis") ;
print "Modified string ", $str, "\n";

print "Change substring 3rd time\n";
substr($str,  -6) =  "str" ;
print "Modified string ", $str, "\n";
