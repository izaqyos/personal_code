#!/usr/bin/perl

print "Subroutines.\n";

print "1. parameters are passed and retruned as flat list. @_ holds all parameters by ref.\n";
@list = (14,2,3,5,20);
sub max {
    my $max = shift(@_);
    for my $item (@_) {
        $max = $item if $max < $item;
    }
    return $max;
}
print "routine to do max. list @list. max: ", max(@list), "\n";

print "2. for long lists are complex data types (hashes, heirarchy of lists etc) pass by ref. \@ for list and \% for hash.\n";


sub sum {
    my ($aref)  = @_;
    my ($total) = 0;
    foreach (@$aref) { $total += $_ }
    return $total;
}

print "sum of @list = ", sum(\@list), "\n";
