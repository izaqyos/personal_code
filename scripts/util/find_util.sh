#!/bin/sh 
# ----------------------------------------------------------
# findfat file locator
#
# syntax:
#    findfat age bytes
# ----------------------------------------------------------
# if the number of arguments is not 2, then ask
# the user to enter the parameters.
# The parameters are number of days to use to consider a file
# old, and number of bytes to use to consider a file fat.
if  [ $# -ne 3  ]
      then
        echo "How many days make a file old?"
        read age
        echo "How many bytes make a file fat? (1k=1000bytes,1mb=1000000bytes)"
        read bytes
        echo "Enter the directory path for the check"
        read directory
else
        age=$1
        bytes=$2
	directory=$3
fi

echo Locating files older than $age days and larger than $bytes bytes from directory $directory
find $directory  -atime +${age} -size +${bytes}c -exec ls -l {} \;

echo "*************************************************************************"
echo Locating directories older than $age days and larger than $bytes bytes from directory $directory
find $directory  -type d -atime +${age} -size +${bytes}c -exec ls -l {} \;
