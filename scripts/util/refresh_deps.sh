#!/bin/bash
#===============================================================================
#
#          FILE:  refresh_deps.sh
# 
#         USAGE:  ./ci_all.sh  -c "chek in comment"
# 
#   DESCRIPTION:  Automate annoying procedure with maven that sometimes after rebase if new dependencies are introduced it will not refresh them automatically.
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

#Yosi Izaq (4:57:09 PM):  1. delete repository
#Yosi Izaq (4:57:13 PM):  2. clean
#Yosi Izaq (4:57:16 PM):  3.?
#Mehdi Bouzouina (mbouzoui) (4:57:21 PM):  mvn install
#Yosi Izaq (4:57:28 PM):  in RT?
#Mehdi Bouzouina (mbouzoui) (4:57:44 PM):  well, it depends what your building
#Mehdi Bouzouina (mbouzoui) (4:57:50 PM):  but generally, you do it from acs
#
#To extract the local repository do:  grep localRepository ~/.m2/settings.xml  | awk -F">" '{print $2}' | awk -F"<" '{print $1}'
#ToDo
#
# 1. use ct lscheckout -r -user yizaq instead of ct lscheckout -r | grep yizaq

# Scripts assumes its being run in a view...
#alias to setview to current working view
#sv

#alias to cd to acs directory
#cdacs_5_0; cd ..
cd /view/`cleartool pwv | awk '/Set view/ {print $3}'`/vob/nm_acs/acs/

#remove current local repository 
rm -rf ` grep localRepository ~/.m2/settings.xml  | awk -F">" '{print \$2}' | awk -F"<" '{print $1}'`

ls -l ` grep localRepository ~/.m2/settings.xml  | awk -F">" '{print \$2}' | awk -F"<" '{print $1}'`

#check exit status
if [ $? -eq 0 ]
then
        echo "Error deleting old local repository"
else
        echo "Successfully removed local repository"
fi

sleep 3

echo "running clean install from: `pwd`"
sleep 3

mvn clean install

exit 0
#ToDo, test, probably need to protect delimiters from shell expansion.expansion
