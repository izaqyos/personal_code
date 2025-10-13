#!/bin/bash
#===============================================================================
#
#          FILE:  ci_all.sh
#       
#         USAGE:  ./ci_all.sh  -c "chek in comment"
# 
#   DESCRIPTION:  check in all files and or dirs that are currently checked out 
# 
#       OPTIONS:  ---
#  REQUIREMENTS:  ---
#          BUGS:  ---
#         NOTES:  ---
#        AUTHOR:   Yosi Izaq 
#       COMPANY:  
#       VERSION:  1.0
#       CREATED:  06/06/2007 11:38:08 AM IDT
#      REVISION:  ---
#===============================================================================


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
if  [ $# -ne 2  ]
      then
	      echo "Please enter check in comment."
        read comment
else
        comment=$2
fi

echo "comment for checkin is $comment."

stream_name=`cleartool lsstream -short`
echo "Searching for checkouts for user `whoami` on stream ${stream_name}"

echo "Checked out directories:"
declare -a co_dirs 
#co_dirs=( `cleartool lscheckout -r | grep \`whoami\` | grep directory | awk '{print \$6}'| sed -e 's_"__g' ` )
co_dirs=( `cleartool lscheckout -r -me | grep $stream_name |  grep "directory version" | awk '{print \$6}'| sed -e 's_"__g' ` )
echo ${co_dirs[@]}

echo "Checked out files:"
declare -a co_files 
#co_files=(` cleartool lscheckout -r | grep \`whoami\`  | awk '{print \$5}' | sed -e 's_\"__g' `)
co_files=(` cleartool lscheckout -r -me | grep $stream_name | grep -v "directory version" | awk '{print \$5}' | sed -e 's_\"__g' `)
echo ${co_files[@]}

echo "Check in ...."

for dir in ${co_dirs[@]}
do
	echo "executing cleartool ci -c \"$comment\" $dir "
	cleartool ci -c \\"$comment\\" $dir 
    if [ $? -eq 0 ] # test error condition of last command, 0 means check in was successful.
    then
            echo "checkin of $dir was successful"
        else
                echo "Attempting to uncheckout $dir"
	            echo "executing cleartool unco -keep $dir"
	            cleartool unco -keep $dir 
                if [ $? -eq 0 ] #unco successful
                then
                        echo "$dir was unchecked out successfuly"
                else
                        echo "Failed to uncheck out $dir"
                fi
        fi

done

for file in ${co_files[@]}
do
	echo "executing cleartool ci -c \"$comment\" $file "
	cleartool ci -c \\"$comment\\" $file 
    if [ $? -eq 0 ] # test error condition of last command, 0 means check in was successful.
    then
            echo "checkin of $file was successful"
        else
                echo "Attempting to uncheckout $file"
	            echo "executing cleartool unco -keep $file"
	            cleartool unco -keep $file 
                if [ $? -eq 0 ] #unco successful
                then
                        echo "$file was unchecked out successfuly"
                else
                        echo "Failed to uncheck out $file"
                fi
        fi
done

## At this stage only files or dirs that haven't changed are checked out. So uncheck out them:
#echo "Checking for identical files. Performing unco -keep"
#echo "Identical checked out directories:"
#declare -a unco_dirs 
#unco_dirs=( `cleartool lscheckout -r | grep \`whoami\` | grep directory | awk '{print \$6}'| sed -e 's_"__g' ` )
#echo ${unco_dirs[@]}
#
#echo "Identical checked out files:"
#declare -a unco_files 
#unco_files=(` cleartool lscheckout -r | grep \`whoami\`  | awk '{print \$5}' | sed -e 's_\"__g' `)
#echo ${unco_files[@]}
#
#echo "Uncheckout...."
#
#for dir in ${unco_dirs[@]}
#do
#	echo "executing cleartool unco -keep $dir"
#	cleartool unco -keep $dir 
#done
#
#for file in ${unco_files[@]}
#do
#	echo "executing cleartool unco -keep $file"
#    cleartool unco -keep $file 
#done
#
