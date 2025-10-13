#!/usr/bin/perl

use strict;

print "1. print range of 10..20.\n";
for (10..20) {print;}

print "\n2. print this file starting from second line.\n";
open(FILE, "range_op.pl" ) || die "can't open file $!.\n";

line: while (<FILE>){
next line if (1 .. /^$/);
print;
}

print "\n3. generate some lists using .. opertor.\n";
my @alphabet = ('A'..'Z');
print "alphabet: @alphabet\n";

my @combo = ('aa'..'zz');
print "two leter combination (first 30 valuse of ",scalar(@combo), "): @combo[0..30].\n";
