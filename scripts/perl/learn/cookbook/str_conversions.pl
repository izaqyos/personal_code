#!/usr/bin/perl  
#===============================================================================
#
#         FILE: str_conversions.pl
#
#        USAGE: ./str_conversions.pl  
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
#      CREATED: 04/08/15 10:22:02
#     REVISION: ---
#===============================================================================

#use strict;
use warnings;

print "EstablishingY a Default Value...\n";
my $str ||= "Default Value";
print "Str value: $str\n";


print "Establishing a Default Value using defined...\n";
my $str1 = defined($str1)? $str1 :  "Default Value1" ;
print "Str value: $str1\n";

print "find the user name on Unix systems\n";
$user = $ENV{USER} || $ENV{LOGNAME} || getlogin( ) || (getpwuid($<))[0] || "Unknown uid number $<";
print "User $user\n";

print "EstablishingY a Default Value for arrays...\n";
@a = ( "a", "b", "c");
@b = @a unless @b ; #can also do @b = @b? @b: @a;
print "array b:  @b \n";

print "Exchanging Values Without Using Temporary Variables\n";
($str, $str1) = ($str1, $str);
print "Str values after swap: $str, $str1 \n";

print "Converting Between Characters and Values\n";
my $c = "a";
print "ASCII value of $c ", ord($c), " character from ASCII value: ", chr(ord($c)), "\n" ;

$i = 0;
for (a..z, A..Z,0..9) 
{
	$i++;  
	print "[$_ , ",ord($_),"] ";
	if ( ($i % 10 ) == 0 ) {print "\n"; $i=0;};
}
print "\n";


print "Unpack and pack...\n";
@int_val_arr = unpack("C*", "My name is yosi");
print  pack("C*", @int_val_arr ), " unpacked:  @int_val_arr \n";
