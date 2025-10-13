package OsUtils;

# Author, yosi.
# Desc. do grep.

# To use by scripts put at @inc.
# see dir list of @inc by:
# perl -e 'print join("\n",@INC)."\n"'
# 
# On laptop its path is: /usr/lib/perl5/5.8/MyPkgs
# To Add to path, do something like
# $ mkdir /usr/lib/perl5/5.8/MyPkgs
# $ cp .//common/OsUtils.pm  /usr/lib/perl5/5.8/MyPkgs
# $ ls /usr/lib/perl5/5.8/MyPkgs/OsUtils.pm 
#
 

sub grep{
my $file = shift;
my $pattern = shift;

#print "grep $file for $pattern";

open (FILE, "< $file") || die "can't open $file. $!";

my @matches;
my $counter = 1;

while  (<FILE>){
	if ($_ =~ /$pattern/i){
		push @matches, "${counter}: $_";
		}
	$counter = $counter +1;
	}

return @matches;
}

1;

