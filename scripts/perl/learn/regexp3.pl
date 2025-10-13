#!/usr/bin/perl

=head1 pattern generation

=begin text
Suppose you wanted to pull out all the words with a certain vowel-consonant sequence; for example, "audio" and "eerie" both follow a VVCVV pattern. Although describing what counts as a consonant or a vowel is easy, you wouldn't ever want to type that in more than once. Even for our simple VVCVV case, you'd need to type in a pattern that looked something like this:

^[aeiouy][aeiouy][cbdfghjklmnpqrstvwxzy][aeiouy][aeiouy]$

A more general-purpose program would accept a string like "VVCVV" and programmatically generate that pattern for you. For even more flexibility, it could accept a word like "audio" as input and use that as a template to infer "VVCVV", and from that, the long pattern above. It sounds complicated, but really isn't, because we'll let the program generate the pattern for us. Here's a simple cvmap program that does all of that:

=end text
=cut

$vowels = 'aeiouy';
$cons   = 'cbdfghjklmnpqrstvwxzy';
%map = (C => $cons, V => $vowels);  # init map for C and V

for $class ($vowels, $cons) {       # now for each type
    for (split //, $class) {        # get each letter of that type
        $map{$_} .= $class;         # and map the letter back to the type
    }
}

#for my $key (keys %map){
#my $val = $map{$key};
#print "$key => $val\n";
#}

for $char (split //, shift) {       # for each letter in template word
    $pat .= "[$map{$char}]";        # add appropriate character class
}

$re = qr/^${pat}$/i;                # compile the pattern
print "REGEX is $re\n";             # debugging output
@ARGV = ('/usr/dict/words')         # pick a default dictionary
    if -t && !@ARGV;

while (<>) {                        # and now blaze through the input
    print if /$re/;                 # printing any line that matches
}


=begin text
The %map variable holds all the interesting bits. Its keys are each letter of the alphabet, and the corresponding value is all the letters of its type. We throw in C and V, too, so you can specify either "VVCVV" or "audio", and still get out "eerie". Each character in the argument supplied to the program is used to pull out the right character class to add to the pattern. Once the pattern is created and compiled up with qr//, the match (even a very long one) will run quickly. Here's why you might get if you run this program on "fortuitously":

% cvmap fortuitously /usr/dict/wordses
REGEX is (?i-xsm:^[cbdfghjklmnpqrstvwxzy][aeiouy][cbdfghjklmnpqrstvwxzy][cbd
fghjklmnpqrstvwxzy][aeiouy][aeiouy][cbdfghjklmnpqrstvwxzy][aeiouy][aeiouy][c
bdfghjklmnpqrstvwxzy][cbdfghjklmnpqrstvwxzy][aeiouycbdfghjklmnpqrstvwxzy]$)
carriageable
circuitously
fortuitously
languorously
marriageable
milquetoasts
sesquiquarta
sesquiquinta
villainously

Looking at that REGEX, you can see just how much villainous typing you saved by programming languorously, albeit circuitously.

=end text
=cut
