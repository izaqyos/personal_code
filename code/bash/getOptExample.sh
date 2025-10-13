#!/usr/bin/bash

usage()
{
        echo "Test getopt for parsing command line arguments in bash"
        echo " please provide -o (--opt1long) and/or -a (--aopt2long)"

}

if [ $# -eq 0 ] ; then
        usage
        exit 0
fi

args=$(getopt -l "aopt2long,opt1long:" -o "aho:" -- "$@")
eval set -- "$args"
while [ $# -ge 1 ]; do
        #echo "parse $1"
    case "$1" in
        -o|--opt1long)
        o1value="$2"
        shift
        ;;
        -a|--aopt2long)
        echo "got a option"
        ;;
        -h)
        echo "Display some help"
        exit 0
        ;;
       # --)
       # # No more options left.
       # shift
       # break
       # ;;
    * ) 
        break ;;
    esac
    shift
done
echo "oval: $o1value"
echo "remaining args: $*"

#####################################################################################################
##usage example
#[212680136@G9VK2GH2E:2018-04-03 11:00:14:/cygdrive/c/Users/212680136/Desktop/Yosi/Work/code/bash:]287$ ./getOptExample.sh --aopt2long -o "aaa"
#got a option
#oval: aaa
#remaining args: --
#[212680136@G9VK2GH2E:2018-04-03 11:00:42:/cygdrive/c/Users/212680136/Desktop/Yosi/Work/code/bash:]288$ ./getOptExample.sh --opt1long "aaa"
#oval: aaa
#remaining args: --
#[212680136@G9VK2GH2E:2018-04-03 11:00:57:/cygdrive/c/Users/212680136/Desktop/Yosi/Work/code/bash:]289$ ./getOptExample.sh --opt1long "aaa" -a
#got a option
#oval: aaa
#remaining args: --
#####################################################################################################
