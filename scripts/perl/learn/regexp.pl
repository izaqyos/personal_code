#!/usr/bin/perl

use strict;
my $fellowship = "Aragorn, gimli, boromir, frodo, gollum, pippin, merry, gandalf, legolas";

print "1. see if frodo is part of the fellowship: $fellowship.\n";
$_ = $fellowship;
if (/frodo/) {print;}

print "\n2. replace gollum with sam!.\n";
$fellowship =~ s/gollum/sam/;
print "The fellowship: $fellowship.\n";

print "3. Names should be capital. no?\n";
$fellowship =~ tr/a-z/A-Z/;
print "fellwoship: $fellowship.\n";

{
print "4. Easy encryption, rotate 13. :) \n";
my $fellowship = $fellowship;
$fellowship =~ tr/a-zA-Z/n-za-mN-ZA-M/ ;
print "\"Encrypted\" fellowship: $fellowship.\n";
}

print "5. use different quates to replace spaces with commas.\n";
$fellowship =~ s# #,#g;
print "fellwoship: $fellowship.\n";
print "and now remove the double commas.\n";
$fellowship =~ s$,,$, $g;
print "fellwoship: $fellowship.\n";

print "6. match markers, before match, match and after match.\n";
$fellowship =~ /FRODO/;
print "before match $`.\n";
print "actual match $&.\n";
print "after match $'.\n";
print "WARNING. THIS MIGHT SLOW DOWN THE PROGRAM!!!\n";

print "6. match addressing using () and ignore case.\n";
$fellowship =~ /(.*)(frodo)(.*)/i;
print "before match $1.\n";
print "actual match $2.\n";
print "after match $3.\n";

print "7. default match returns last match use ?? instead of // to return first match.\n";
open FILE, "regexp.pl" or die "Can't open script file: $!\n";
#match_with_??
#match_with_//
my ($first, $last);
while (<FILE>) {
     $first = $1 if ?(^#match_with.*)?;
     $last  = $1 if /(^#match_with.*)/;
}
print " first match: $first \n";          
print " last match:  $last \n";          

print "8. substitute (s//). replace by perl code instead of interpolated string using /e.\n";
my $ring_nums = "13 79";
print "for example, replace following numbers to hex format $ring_nums\n";
$ring_nums =~ s/([0-9]+)/sprintf("%#x", $1)/ge;
print "hex format: $ring_nums.\n";

print "9. replace all occurrences of the word bilbo to Bilbo Baggins in an array\n";
my @words = qw(bilbo was the main character of the hobbit. bilbo played a minor role in lotr);
for (@words) {
s/
bilbo
/
Bilbo Baggins/xgi;

print "$_ ";
}
print "\n";

print "10. multiple substitutions on same string using once-through loop and also join and split.\n";
my $string = "         w e_    want_ t o_ cl   ean_         al    l_ th  ose_   annoying_    space s_         ";
print "string: $string.\n";
for ($string){
s/^\s+//; #remove leading whitespace
s/\s+$//; #remove trailing whitespace
s/\s+/ /g; #replace all whitepsaces with one space.
}

print "fixed string: $string.\n";
print "same can be done via jone and split.\n";
$string = join(" ", split " ", $string);
print "fixed string: $string.\n";

print "11. global substitution. some examples in which /g isn't enough, so the substitution is repeated in a loop.\n";

my $price="\t13456729347521\$";
print "put commas in the right places in an integer $price.\n";
$_ = $price;
s/(\d)(\d\d\d)/$1,$2/g;
print "first attempt using /g. price is $_.\n";
$_ = $price;
while (s/(\d)(\d\d\d)(?!\d)/$1,$2/){
  #print "match $1 $2\n";
};
#s/(\d)(\d\d\d)(?!\d)/ # we want to start match from the right to left else we'll get the first example so we make sure after the match there
# is a zero or one digits.
#$1,$2/
#
print "second attempt using loop. price is $_.\n";

$_ = $price;
print " expand tabs to 16-column spacing.\n";
while (s/\t+/' ' x (length($&)*16 - length($`)%16)/e){};
print "formatted price: $price.\n";

my $comment  = "statement.(this is a (nested comment (ok, very)))";
print "remove nested remarks like in $comment.\n";
$_ = $comment;
while (s/\([^()]*\)//g){
#print "before $`, match $&, after $'.\n";
};
print "fixed comment: $_\n";
#(s/\([^()]*\) #match to something like ( anything but '(' or ')' ) which is the inner most (comment).
#//g)


my $message = "reMOvE duplicate woRRRdS \$\$\$ \%\%\% (aaaaannnndddd tRIPlicate (aNd quadruplicate...1,2,3,4...)) like like like like this.\n";
print $message, "\n";
while ($message =~ s/\b(\w+) \1\b/$1/gi){};
print "fixed: $message";

print "12. transliteration operator.\n";
$_ = $message;

tr/aeiou/!/;                 # change any vowel into !
print "change vowel's to !. like: $_ \n";

#tr{/\\\r\n\b\f. }{_};        # change strange chars into an underscore

$message =~ tr/A-Z/a-z/;       # canonicalize to lowercase ASCII
print "canonicalize to lowercase ASCII: $message";

#$count = ($para =~ tr/\n//); # count the newlines in $para
my $count = tr/0-9//;           # count the digits in $_
print "this strig has  $count digits.\n";

$message =~ tr/a-zA-Z//s;       # bookkeeper -> bokeper
print "squash (/s) repetetive characters: $message\n";

$message =~ tr/@$%*//d;                  
print "delete \$ \% chars. : $message\n";
#tr#A-Za-z0-9+/##cd;          # remove non-base64 chars

# change en passant
#($HOST = $host) =~ tr/a-z/A-Z/;

#$pathname =~ tr/a-zA-Z/_/cs; # change non-(ASCII)alphas to single underbar
