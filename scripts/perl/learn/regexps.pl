#!/usr/bin/perl

use strict;

#Yosi. regexp examples.
print "1. using split to get a list of tokens seperated by given seperator.\n";
my @fields = split(/,/, "vi,emacs,teco");
print " input: vi,emacs,teco.\n seperator: ,.\n fields: @fields.\n"; 

print "2. simple patter match on $_.\n";
  foreach (@fields){
    print if /vi/;
  }

print "3. match quantifiers {min,max}. (example + <-> {1,}, ? <-> {0,1}, * <-> {0, }).\n";
my $phone_number = "0508464424";
$phone_number =~ /(\d{1,3})(\d{2,4})/;
print "first three digts $1, next four digits $2.\n";

print "4. rex exp match is greedy!\n";
my $inp1 = "larry:JYHtPh0./NJTU:100:10:Larry Wall:/home/larry:/bin/tcsh";
print "input: $inp1\n";
$inp1 =~ /(.+:)/;
print "match via .+: (all chars up to :) is $1\n";
$inp1 =~ /([^:]+:)/;
print "match via [^:]+: (one or more non : chars up to : char) is $1\n";









