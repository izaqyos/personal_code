#!/usr/bin/perl

# Author: Yosi Izaq
# Description: This utiilty recieves as parameters a flag, string, two numbers that form a range and a file name. 
#  The flag is 'c' or 'u'. 'c' is for commenting and 'u' is for uncommenting.
# The string is the line prefix to make comment. like "\\" in C++, java, "#" in shells and "%" in tex.
# The range specify the lines to be commented.
# File name is file to be modified.

# usage example. note \# to protect the # from being iterepeted by the shell.
# comment_code.pl  c \# 81 97 save_dom.pl

use strict;

#print "argument ", $#ARGV+1, "\n";
#print "arguments @ARGV\n";

if (@ARGV != 5){
  help();
}
else{
#  print $ARGV[0], "\n";
  if (( $ARGV[0] eq 'c') || ($ARGV[0] eq 'u') ){
#    shift;
    comment_code(@ARGV);
  }
  else{
    help();
  }
}
sub help{

print "usage comment_code.pl [c|u] [comment] [line start] [line end] [file name]\n";
print " Description: This utiilty recieves as parameters a flag, string, two numbers that form a range and a file name.\n";
print "The flag is 'c' or 'u'. 'c' is for commenting and 'u' is for uncommenting.\n";
print "The string is the line prefix to make comment. like \"\\\\\" in C++, java, \"#\" in shells and \"%\" in tex.\n";
print "The range specify the lines to be commented.\n";
print " File name is file to be modified.\n";
print " Please note that the comment can be protected from shell expression by \' or \". For example \'#\'.";
}


sub comment_code{
#print @_, "\n";
my $flag = "$_[0]";
my $comment_string = "$_[1]";
(my $line_start, my $line_end) = ($_[2]-1, $_[3]-1);
my $file_name = "$_[4]";
#print "Arguments. flag, $flag; comment, $comment_string; range, ($line_start, $line_end); file, $file_name.\n";

verify($line_start, $line_end);

#open for update
open(FILE, "+< $file_name") or die "can't open file $file_name. $!";
my @lines = <FILE>;

my $line_num = 0;
foreach  (@lines){
#  print " [${line_num}] $_\n";

#make the comment
  if ( ($line_num >= $line_start) && ($line_num <= $line_end) ){
#print "bingo $line_num is in range ($line_start, $line_end).\n";

#comment
    if ($flag eq 'c'){
    $lines[$line_num] = "${comment_string}$_";
  }

#uncomment
    elsif ($flag eq 'u'){
      $_ =~ /^($comment_string)(.*)/;
#      print "comment $1, line $2\n";
      $lines[$line_num] = "$2\n";
    }
  }
 $line_num++;
}

#write modified buffer to file
seek(FILE, 0, 0) or die "can't seek to file $file_name start. $!";
print FILE @lines  or die "can't print to file $file_name start. $!";
#remove any tails.
truncate(FILE, tell(FILE)) or die "can't truncate file $file_name start. $!";
close(FILE);

}

#Verify arguemnts
sub verify{
  if ( ($_[0] > $_[1]) || ($_[0] < 0) ){
    print "Range is not legal ($_[0], $_[1]).\n";
    exit (-1);
  }

}
