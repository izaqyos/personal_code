#!/usr/bin/perl

print "Continuing the regexps!!!\n";

my $burglar = "Bilbo Baggins";
print "1. positions, print position of b in \"$burglar\".\n";
while ($burglar =~ /b/gi) {
    printf "Found a B at %d\n", pos($burglar)-1;
}

print " add /c so that postion isn't reset after match. find b and the i from last b position!\n";
while ($burglar =~ /b/gci) {        # ADD /c
    printf "Found a B at %d\n", pos($burglar)-1;
}
while ($burglar =~ /i/gi) {
    printf "Found an I at %d\n", pos($burglar)-1;
}

my $number = "0508464424";
print "2. clustering and capturing (). match digits in $number.\n"; 
$number =~ /(\d+)/;     # Match one or more digits, capturing them all into $1
print "first match using (\d+): $1.\n";
$number =~ /(\d)+/;     # Match a digit one or more times, capturing the last into $1
print "second match using (\d)+ (match last digit): $1.\n";


print "3. populating a list/map from backreferences.\n";
my $name = "Yosi Izaq";
my ($first, $last, $full);
$_ = $name;
($first, $last)        =  /^(\w+) (\w+)$/;
print "first name, $first. last name, $last.\n";
($full, $first, $last) =  /^((\w+) (\w+))$/;
print "full name, $full. first name, $first. last name, $last.\n";

print "3. clustering without capturing (?:pattern). refer to following commented description.\n";
#/prob|n|r|l|ate/    # Match prob, n, r, l, or ate
#/pro(b|n|r|l)ate/   # Match probate, pronate, prorate, or prolate
#/pro(?:b|n|r|l)ate/ # Match probate, pronate, prorate, or prolate 

print "4. variable interpolation to make pattern match more readable. refer to following commented description.\n";

#compare this
#if ($num =~ /^[-+]?\d+\.?\d*$/) { ... }

#But what you mean is more apparent when you write:
#$sign = '[-+]?';
#$digits = '\d+';
#$decimal = '\.?';
#$more_digits = '\d*';
#$number = "$sign$digits$decimal$more_digits";
#...
#if ($num =~ /^$number$/o) { ... }

print "5. use variable interpolaion to compare to a known list of string.\n";
print "please enter action.\n";
chomp(my $answer = <STDIN>);
if    ("SEND"  =~ /^\Q$answer/i) { print "Action is send\n"  }
elsif ("STOP"  =~ /^\Q$answer/i) { print "Action is stop\n"  }
elsif ("ABORT" =~ /^\Q$answer/i) { print "Action is abort\n" }
elsif ("LIST"  =~ /^\Q$answer/i) { print "Action is list\n"  }
elsif ("EDIT"  =~ /^\Q$answer/i) { print "Action is edit\n"  }
