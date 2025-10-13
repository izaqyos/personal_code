#!/usr/bin/perl

# Description, create TOC for my kb files.
# Their format is (example):
# start new section                      ****************
# section number                         1. section1
# subsections                                   1.1 subsection1_1
#                                                             1.2 subsection1_2
#                                                             1.2.1 subsubsection 1_2_1
# end section                                   ****************

# Author Yosi Izaq

#Note that since most of the KB files are in the following format:
# 1. subject
# 1.1 example1
# 1.2 example2.
# ...
# 
# It makes more sense to build a TOC only based on the subjects. So for now that's what the script does.

# Future ideas.
# 1. update flag, remove old TOC and create a new one.
# 2. support multiple nesting levels.  with correct indentation.

use strict;


if (@ARGV < 1){
#print "# args: ". @ARGV ."\n";
  help();
  exit(-1);
}

# For cat:
#while (<>){
#print $_;
#}

for (@ARGV){
#print $_, '\n';
#open file for read and write
open(FH, "+< $_")                 or die "Opening $_:  $!";
my @ARRAY = <FH>;

# apply changes (to ARRAY)
tocify(\@ARRAY);

#print @ARRAY;

#save array to file, truncate all else and close file
seek(FH,0,0)                        or die "Seeking: $!";
print FH @ARRAY                     or die "Printing: $!";
truncate(FH,tell(FH))               or die "Truncating: $!";
close(FH)                           or die "Closing: $!";
}
sub help(){

my $message =
  "\n".
  "\tThis script create TOC for my kb files.\n".
  "\tTheir format is (example):\n".
   "\tstart new section                      ****************\n".
  "\t section number                         1. section1\n".
  " \tsubsections                                   1.1 subsection1_1\n".
  "\t                                                             1.2 subsection1_2\n".
  "\t                                                             1.2.1 subsubsection 1_2_1\n".
  "\t end section                                   ****************\n";

my $usage  = "usage: tocify.pl <file 1> <file 2> .... \n";

print $message, $usage;

}


#Description, receive an array of file lines.
# then add to this the 
# Array is passed by reference, since tocify modifies it.
sub tocify(){

  my $arr = @_[0];
  
  my $toc_pref = ".........................................Table Of Contents...............................................................\n";
  my $toc_suff  = ".................................................END TOC..............................................";
  my @toc = ();
push @toc, $toc_pref;
  
  my $skip_line = 0;
  my $old_toc_start = 0;
  my $old_toc_end = -1;
  my $i = 0;
#parse file.
  for (@$arr){

	  #print "processing line $_\n";
    # If there's an existing TOC delete it. A new one is created in its stead.
    if (/$toc_pref/){
#      print "Mark start of old TOC at $i\n";
      # raise flag to delete all TOC lines
      $old_toc_start = $i;
#      print "Found old TOC. Setting skip_line mode\n";
      $skip_line = 1;
    }
    
    if ($skip_line == 1){
		#print "skipping current line\n";
      if (/^${toc_suff}/){
#	print "Mark end of old TOC at $i. Removing skip_line mode\n";
	$old_toc_end = $i;
	$skip_line = 0;
      }
    }
    else{
      # a <num>. header.   zero or more whitespace, followd by 1 or more number. thingis
      if (/^(\s)*(\d+\.)+/){
		  #print "Add TOC line: $_\n";

	#For TOC without UTL links uncomment following line:
	#push @toc, $_;
	my $line = $_;
	chomp $line;
	push @toc, "$line <URL:#tn=$line>\n";
      }
    }
    
 $i = $i+1;
}#For loop
    
#remove old TOC if any
    for (my $j = $old_toc_start; $j <= $old_toc_end; $j++){
      my $rem = shift @$arr;
#      print "removed line $rem\n";
	}
    push @toc, "$toc_suff\n\n";
  
  # Add new TOC
  unshift @$arr,  @toc;
        
    #print @$arr;
}#tocify
  
