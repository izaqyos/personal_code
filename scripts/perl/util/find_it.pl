#!/usr/bin/perl

#Description. find class, function or string in ACS code
#Author. Yosi Izaq

#use strict;
use MyPkgs::OsUtils;

#@paths = (" /cygdrive/h/ismg_israel_acs/Acs/RuleEngine", "/cygdrive/h/ismg_israel_acs/Acs/PDE", "/cygdrive/h/ismg_israel_acs/Acs/" );

my $all_path = "/cygdrive/g/ismg_israel_acs/Acs";
my @paths = ("${all_path}/RuleEngine", "${all_path}/PDE", "${all_path}/PostureValidation");


sub main_menu{
print "This is a small search utility.\n";
print "Please choose search mode:\n";
print "\t1. search for method declaration\n";
print "\t2. search for method definition and usage\n";
print "\t3. search for class location\n";
print "\t4. search for pattern\n";
print "\t5. search for pattern in ALL ACS!\n";
print "\t6. View search path\n";
print "\th. display help\n";
print "\tq,Q. quit\n";

$ans = <STDIN>;
chomp($ans);
return $ans;
}

while (1)
{
$ans = main_menu();
	
	if ($ans eq "1"){
		print " you chose method declaration search.\n";
		$pattern = receive_pattern();
		search_method($pattern, 1);
		}
        if ($ans eq "2"){
                print " you chose method defenition and usage search.\n";
                $pattern = receive_pattern();
                search_method($pattern, 0);
                }
   	elsif ($ans eq "3"){
		print " you chose class location search.\n";
		$pattern = receive_pattern();
		search_class_location($pattern);
		}
   	elsif ($ans eq "4"){
		print " you chose broad search.\n";
		$pattern = receive_pattern();
		broad_search($pattern);
		}
   	elsif ($ans eq "5"){
		print " you chose to search all ACS.\n";
		$pattern = receive_pattern();
		broad_search_all($all_path, $pattern);
		}
   	elsif ($ans eq "6"){
		print " Search path.\n";
		for (@paths){
		  print $_, "\n";
		}
		}
	elsif ($ans eq "h"){		
		print " you chose to display help.\n";
		help();
			}
	elsif (($ans eq "q") || ($ans eq "Q")){
		print " you chose to quit.\n" ;
		exit 0;
		}
	else	{
		print "Invalid input.\n" ;
		}

}


sub help {
print " This is a search utility\n";
}

sub receive_pattern{
print "please enter search pattern\n";

$ans = <STDIN>;
chomp($ans);
return $ans;
}


sub search_method{
my $pattern = "$_[0]";
my $is_defenition  = $_[1];

for (@paths) {
  search_method_in_proj($_, $pattern, $is_defenition);
} 
}

sub search_method_in_proj{
my $proj_path = "$_[0]";
my $pattern = "$_[1]";
my $is_defenition = $_[2];

#chdir("$proj_path") || die "cannot cd to $proj_path ($!)";
print "\n****** METHOD SEARCH RESULTS IN $proj_path **************\n";
my $cmd;
if ($is_defenition  == 1){
	$cmd =  " grep -P \"${pattern}\\s?\\(.*\\)\" $proj_path/*.h ";
	}
else {
	$cmd =  " grep -P \"${pattern}\\s?\\(.*\\)\" $proj_path/*.cpp ";
	}

system($cmd);
print "\n";
}

sub search_class_location{
$pattern = "$_[0]";

for (@paths){
  search_class_location_in_proj($_, $pattern);
}
}

sub search_class_location_in_proj{
$proj_path = "$_[0]";
$pattern = "$_[1]";
print "\n****** CLASS SEARCH RESULTS IN $proj_path ****************\n";
my $cmd = " grep -P \"class\\s+.*${pattern}\(\\s?:\\s?[public|protected|private]?\)?\" $proj_path/*.h $proj_path/*.cpp";
#print ($cmd);
system ($cmd);
print "\n";

}

sub broad_search{
$pattern = "$_[0]";

for (@paths) {
  broad_search_in_proj($_, $pattern);
}
}


sub broad_search_in_proj{
$proj_path = "$_[0]";
$pattern = "$_[1]";

print "\n****** RESULTS OF BROAD SEARCH IN $proj_path ****************\n";
#print (" grep -i \"class $pattern\"  $proj_path/*/*/* | grep -v \\*  ");
system (" grep -in  \"$pattern\"  $proj_path/*.h  ");
system (" grep -in  \"$pattern\"  $proj_path/*.cpp   ");
print "\n";

}

sub broad_search_all{
$proj_path = "$_[0]";
$pattern = "$_[1]";

print "\n****** RESULTS OF BROAD SEARCH IN $proj_path ****************\n";
#system ("find $proj_path \\( -name \"*.h\" -o -name \"*.cpp\"  \\) -print  -exec grep -in $pattern  '{}' \\;");

chdir("$proj_path") or die "can't chdir to $|";

my @h_list = glob("*/*.h");
my @cpp_list = glob("*/*.cpp");
my @h_list_2nd = glob("*/*/*.h");
my @cpp_list_2nd = glob("*/*/*.cpp");
@file_list = (@h_list, @cpp_list, @h_list_2nd, @cpp_list_2nd);

foreach (@file_list){
	my $file = $_;
	my @matches = OsUtils::grep($_, $pattern);	
  	if (@matches > 0 ){
	print "Pattern was found in file $file at following lines: \n", @matches, "\n\n";
	}	
}

print "\n";

}
