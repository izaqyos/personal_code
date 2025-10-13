#!/usr/bin/perl

print "1. print 40 *.\n";
print '*' x 40, "\n";

print "2. tab over, define tab space to 13 spaces.\n";
my $tab = 13;
print "\t" x ($tab/8), ' ' x ($tab%8). '>>'; 

print "3. initialize an array of 40 1s.\n";
my @ones = (1) x 80;           # a list of 80 1's
print "array: @ones\n";
print "and now multiply all values by five.\n";
@ones = (5) x @ones;        # set all elements to 5
print "array: @ones\n";

print "4. intilialize hash values.\n";
my @keys = qw(perls before swine);
print "hash keys: @keys\n";
@hash{@keys} = ("=>NULL ") x @keys;
print 'initialized hash: ', %hash, ".\n";
