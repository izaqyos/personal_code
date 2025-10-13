#!/usr/bin/bash

# Author Yosi Izaq
# Description: Translate files in KB VIM format to common HTML


for x
do
	echo "Translating file $x to $x.html"
	sed '
	# ToDo add specific title for dominions KB, like Wraithlords something...
	1i\<html>\n<head>\n<title>'"$x"'</title>\n<body>

	#In not using <pre> to preserve original line breaks and spaces add line breaks manually
	#1,$a\<br>

	$a\</pre></body>\n</html>

	#Put Nicely Table of contents line
	s/^.*Table Of Contents.*$/<hr>\n<p align=\"center\">\n<b>Table Of Contents<\/b>\n<\/p>\n<hr>\n<pre>/

	#Put Nicely End of Table of contents line
	s/^.*END TOC.*$/<\/pre><hr>\n<p align=\"center\">\n<b>END TOC<\/b>\n<\/p>\n<hr>\n<pre>/

	#Indentification
	#s/\t/    /

	# Conver ----- lines to <hr>
	s/^--------*$/<hr>\n/

	# Create named anchors for all article headers (from End of TOC to end of document)
	/^.*END TOC.*$/,${
	s/^\(\s*\)\([0-9].*\)$/<a name=\"\2\">&<\/a>\n/
	}

	# Plant links to above anchors from TOC
	/^.*Table Of Contents.*$/,/^.*END TOC.*$/{
	s/\(^\s*\)\([0-9].*\)\( <URL.*>\)/<a href=\"#\2\">\1\2<\/a>\n/
	}

	# Remove the | at the start of lines with numbers. I plant them so that tocify.pl dont get confused when building TOC
	s/^\(\s*\)|/\1/
	' $x > $x.html
	echo "Finished Translating file $x to $x.html"
done

