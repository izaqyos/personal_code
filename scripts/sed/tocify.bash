#!/usr/bin/bash

# Author Yosi Izaq
# Description: Create a TOC for my KB files. Its meant more as a proof of concept than to be really used
# since tocify.py is much more efficient (works in memory as opposed to using temp file).

#sedscr="/cygdrive/c/work/scripts/sed/sed_create_toc"

for x
do
	rm -f temp_file

	echo ".........................................Table Of Contents..............................................................." >> temp_file

	# Enter TOC content:
	#
	# Following directive is to create a simple TOC
	#sed -n '/Table Of Contents/,/TOC/d; /^\s*\([0-9]\.\)\+/p' $x >> temp_file

	# Following directive is to create a  TOC that uses VIMs UTL plugin for hyper reference.
	sed -n '/Table Of Contents/,/TOC/d; s/^\s*\([0-9]\.\)\+.*$/& <URL:#tn=&>/p' $x >> temp_file

	#sed -nf $sedscr $x  > temp_file

	echo ".................................................END TOC..............................................  " >> temp_file
	# Enter file content and remove old TOC if exists
	sed  '/Table Of Contents/,/TOC/d' $x >> temp_file 

	mv -f temp_file $x

done
