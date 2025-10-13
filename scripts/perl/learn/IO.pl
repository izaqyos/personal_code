#!/usr/bin/perl

use strict;

print "1.read this file.\n";

open(MY_SCRIPT, "IO.pl") || die "can't open file $!";

while (<MY_SCRIPT>){
  print;
}

print "2. globbing. used like ls.\n";
#my @files = <*.pl>;
my @files = glob ("*.pl");
print "perl scripts in this dir are @files.\n";

print "3. null filehandle process all file names in command line and if there are none then STDIN.\n";
print "if you ran this script with no file arguments you get a prompt >>.\n";
print "to quit press ctrl+D.\n";
while (<>){
  print ">>$_";
}
