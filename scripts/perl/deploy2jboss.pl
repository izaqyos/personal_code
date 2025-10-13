# Author Yosi Izaq
# Description. This small utility script searched for .ear files and deployes them for jboss.

use File::Copy;

sub main{
	$projects_path = "D:/work/java/jsp";
	
my @earList = getEarList();
	#print "deployment files: @earList\n";
	print "Please choose a file to deploy (enter # from list)\n";
	$i = 0;
	for (@earList){
		$i++; 
		print "$i. $_ \n";
	}
	
	$ans = <STDIN>;
	chomp($ans);
	if ($ans !~ /\d+/){
		die "must specify file #.\n";
	}
	print "you have chosen file $earList[$ans-1].\n";
	deploy2jboss($earList[$ans-1]);	
}

sub getEarList{
	my @earList;
#	chdir("D:/eclipse/workspace") || die "couldn't change dir $!" ;
#	print "changed dir\n";
	opendir(DIR, $projects_path);
	@files = readdir(DIR);
	
	for  (@files){
		if (/^\w/) {
				print "subdir $_\n";

				my $subdir = "$projects_path/$_";
				opendir(SUBDIR, $subdir) || die "couldn't open dir $subdir. $! \n" ;
				@sub_files = readdir(SUBDIR);
				for (@sub_files){
					if (/$.ear/){
						#print "found deployment file: $_\n";
						push(@earList,"$subdir/$_");
					}
				}
		
		# glob will return a list .ear files, need 2 append the path prefix.				
		#chdir($subdir) || die "$!";
		#push(@earList, glob("*.ear") );				
		};
		 
	}
	#print "deployment files: @earList\n";
	return @earList;
}

sub deploy2jboss{
	$file = shift;
	$file =~ /(\w+.ear)/;
	#$` holds the path while $1 the file name.
	#print "found $` $1\n";
	my $j2boss_deploy_path = "D:/Program Files/jboss-4.0.2/server/default/deploy/"; 
	
	copy($file, "$j2boss_deploy_path/$1") || die "file can't be copied, $!";
	print "$file deployed successfuly\n";
}

main();