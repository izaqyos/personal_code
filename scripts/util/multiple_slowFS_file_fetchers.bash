#!/bin/bash
#===============================================================================
#
#          FILE:  multiple_slowFS_file_fetchers.bash
#       
#         USAGE:  multiple_slowFS_file_fetchers.bash
# 
#   DESCRIPTION:  Go to IPCentral and extract all ACS 5.1 libs
#   Must be done MT since the archive is extremely slow
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

ARCHIVE_LOC="/auto/ipcentral-vault-1/ipcentral-prod/unpacked/projects/ACS 5.1"
TRG_LOC="/users/yizaq/temp"
ARCHIVE_NAME="acs_5_1_src_publication_"

cd "$ARCHIVE_LOC"

ArchiveLibs(){


        echo "archiving libs starting with letter $1"
        echo "exec: tar cvhz ${TRG_LOC}/${ARCHIVE_NAME}$1.tarz $1*"
        #touch ${TRG_LOC}/${ARCHIVE_NAME}$1.tarz
        tar -zcvhf ${TRG_LOC}/${ARCHIVE_NAME}$1.tarz $1*
}

for let in {a..z} ; do
        ArchiveLibs "$let" &
        sleep 1
done

wait $!
echo "Terminated all archive threads"
