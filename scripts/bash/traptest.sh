#!/bin/bash
#===============================================================================
#
#          FILE:  traptest.sh
# 
#         USAGE:  ./traptest.sh 
# 
#   DESCRIPTION:  
# 
#       OPTIONS:  ---
#  REQUIREMENTS:  ---
#          BUGS:  ---
#         NOTES:  ---
#        AUTHOR:   (), 
#       COMPANY:  
#       VERSION:  1.0
#       CREATED:  06/13/11 17:07:27 JDT
#      REVISION:  ---
#===============================================================================

#!/bin/bash
# traptest.sh

trap "echo Booh!" SIGINT SIGTERM SIGHUP
echo "pid is $$"

while :			# This is the same as "while true".
do
        sleep 60	# This script is not really doing anything.
done
