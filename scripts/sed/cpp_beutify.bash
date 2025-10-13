#!/usr/bin/bash

# Author Yosi Izaq
# Description: make modifications to CPP source code files to adher to ACS 5.0 coding conventions

for x
do
	rm -f temp_file

	echo "Beutifying file $x"

	# Remove @author comment which is against the convention 
	# Replace tabs with four spaces
	sed '/@author/d; s/\t/    /' $x >> temp_file

	mv -f temp_file $x

done

