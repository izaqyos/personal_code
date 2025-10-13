#!/usr/bin/perl

#use strict turns on variable and ref scope checking (among other checks).
use strict;

#Yosi. play with control structures.

# notice that referencing the array in scalar context returns it's length
# the length is used as the loop stop condition.

while (@ARGV) {
    process(shift @ARGV);
}

# next - skip iteration, last - end loop
my @users = ("yosi", "moshe", "lp", "special", "yaniv", "root");
print "users @users.\n";
foreach my $user (@users) {
    if ($user eq "root" or $user eq "lp") {
       print "skip user $user.\n";
        next;
    }
    if ($user eq "special") {
        print "Found the special account.\n";
        # do some processing
        last;
    }
}

sub process{

print "argument: $_[0]\n";
}
