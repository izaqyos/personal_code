#!/bin/bash

#File surpress_valgring_acs_errors 
#Author Yosi Izaq
#Description surpress a list of unwanted valgrind errors. 
#Usage, Run surpress_valgring_acs_errors <valgrind_report_file>


SURPRESS_LIST=(  'vg_replace_malloc.c:342' )

if [ -z -ne "$2" ]
then 
        help
fi



function help(){
        echo "Usage surpress_valgring_acs_errors <valgrind_report_file>"
}

for symbol in ${SURPRESS_LIST[@]}
do
        echo "surpressing symbol: ${symbol}"
done
