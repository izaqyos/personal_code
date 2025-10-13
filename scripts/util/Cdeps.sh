#!/bin/sh

# Cdeps 1.1rc1, June 2005

# Dirk van Deun, dirk at dinf.vub.ac.be, http://dirk.rave.org/

USAGE='
Summary: cdeps [-p] [-z] file...
  -p: prepare cdeps.db
  -z: zoom, i.e. show separate functions and macros
  -w: compute header file weights

Used without options, cdeps produces a graph of dependencies between the
named source and header files, with edges from files where functions or
macros are used, to the header files in which these are declared.
The output format of cdeps is the input format for dot, the tool from the
graphviz package that produces the actual drawing, e.g. in PostScript:

  cdeps *.c *.h > graph.dot ; dot -Tps graph.dot -o graph.ps

This will find all dependencies among the source and header files.  When
you are interested in the functions and macros used in some specific
files of a project only, you will still need all of the header files to
be considered as providers of function declarations and macros.
For this purpose you can prepare a lookup file cdeps.db:

  cdeps -p *.h ; cdeps file1.c file2.c > graph.dot ; dot -Tps ...

The option -z adds nodes for the functions and macros themselves to the
graph, which may produce big graphs.  Use it to zoom in on a small number
of files.

The option -w makes cdeps not output a graph, but compute weights per
header file that indicate how pervasive they are in the project.  Use it
to get a first impression of a large project.  (The broken down values
are the percentage of source files that contain at least one reference to
the header file, the percentage of the total number of counted
identifiers in the project refering to the header file, and the median
number of different references to the header per source file.)

  cdeps -p *.h ; cdeps -w *.c
'

PREP=false
ZOOM=false
WEIGHTS=false

GETOPT_COMPATIBLE=true set -- `getopt "pzw" $@`

while test $1 != "--"
do
  case "$1" in
    -p) PREP=true ;;
    -z) ZOOM=true ;;
    -w) WEIGHTS=true ;;
  esac
  shift
done
shift

if test $# -eq 0; then
  echo "$USAGE" 2>&1
  exit
fi

# allow cdeps `gcc -MM *.c` by throwing away "--", "\", and names of .o-files

set -- `for f in $@; do
          echo $f
        done | sort | uniq | grep -v '^--$' | grep -v '^\\\\$' | grep -v '.o:$'`

# check whether the required programs are installed

if ! which cscope >/dev/null 2>&1; then
  cat 1>&2 <<--
Please install cscope, which should be available in a package or via the
ports collection for just about any unix-like operating system.
-
  exit
fi

CTAGS=ctags
if which ectags >/dev/null 2>&1; then CTAGS=ectags; fi

if ! $CTAGS --version 2>/dev/null | grep Exuberant >/dev/null; then
  cat 1>&2 <<--
Please install exuberant ctags, which should be available in a package or
via the ports collection for just about any unix-like operating system.
-
  exit
fi

# cdeps.db/.cdeps.db file format: FUNCTION HEADERFILE

if test $PREP = "true"; then
  $CTAGS -x --c-kinds=pd --file-scope=no $@ | awk '{ print $1 " " $4 }' |
    sort | uniq > cdeps.db
  exit
fi
  
if test -e cdeps.db; then
  ln -f cdeps.db .cdeps.db
else
  $CTAGS -x --c-kinds=pd --file-scope=no $@ | awk '{ print $1 " " $4 }' |
    sort | uniq > .cdeps.db
fi

# cscope databases are dirty, but we will only need the function/macro calls

extractprog='/^\t@/ { do { getline
                           if ($0 ~ /^\t`/) print substr($1,2)
                         } while ($0 !~ /^\t@/)
                      exit }'

# weights

if test $WEIGHTS = "true"; then

  # basic cross-reference: name of code file, function, header file
  # contains doubles: counting here does not seem more efficient (tried it)

  for cf in $@; do
    cscope -b -c -k -f .cdeps.cscope $cf
    awk "$extractprog" .cdeps.cscope |
    sort | join -o 2.1 2.2 - .cdeps.db |
    awk "{ print \"$cf \" \$1 \" \" \$2 }" | sort
  done >.cdeps.basic

  cfiles=`echo $@ | wc -w`
  ids=`wc -l <.cdeps.basic`

  # per header file, compute the amount of source files that refer to it;
  # the amount of identifiers that refer to it; and then per source
  # file that contains at least one, the amount of *different* identifiers
  # that refer to the header file, and take the median of these: these
  # three values go into the weight value for that header
  
  for hf in `cut -d " " -f 3 .cdeps.basic | sort | uniq`; do
    grep " $hf$" .cdeps.basic >.cdeps.part
    referers=`cut -d " " -f 1 .cdeps.part | uniq`

    HtoC=`echo $referers | wc -w`
    HtoCpct=`expr $HtoC \* 100 / $cfiles`
    HtoID=`wc -l <.cdeps.part`
    HtoIDpct=`expr $HtoID \* 100 / $ids`
    
    middle=`expr \( $HtoC + 1 \) / 2`
    medianUniqueRefs=`
      for cf in $referers; do
        grep "^$cf " .cdeps.part |
          cut -d " " -f 2 | uniq | wc -l
      done | sort -n | tail +$middle | head -1 | awk '{ print $1 }'`
    
    weight=`expr \( $HtoCpct + $HtoIDpct \) \* $medianUniqueRefs`
    echo "$weight $hf ($HtoCpct%, $HtoIDpct%, $medianUniqueRefs)"
  done | sort -nr

  rm .cdeps.* ; exit
fi

# print header for .dot file

echo 'digraph test { node [fontname = "Vera"] edge [fontname = "Vera"]' \
     'graph [ranksep = 3]'

if test $ZOOM = "false"

# non-zoom output format: SOURCEFILE -> HEADERFILE [ label = NUMMER ]

then
  for f in $@; do
    cscope -b -c -k -f .cdeps.cscope $f
    awk "$extractprog" .cdeps.cscope |
    sort | join -o 2.2 - .cdeps.db | sort | uniq -c |
    awk "{ print \"\\\"$f\\\" -> \\\"\" \$2 \"\\\" [ label = \" \$1 \" ]\" }"
  done
  
# .cdeps.calls file format: FUNCTION SOURCEFILE NUMBER

else
  for f in $@; do
    cscope -b -c -k -f .cdeps.cscope $f
    awk "$extractprog" .cdeps.cscope |
    sort | uniq -c |
    awk "{ print \$2 \" \" \"$f\" \" \" \$1 }" 
  done | sort > .cdeps.calls

# What follows merits a big comment.  It serves to condense the graph
# by combining nodes representing functions (and macros) that have the
# same incoming edges and the same outgoing edge.
# It converts a file of records: the name of a function, followed by the 
# name of the header file in which it is declared, followed by the name
# of a source code file in which it is used and a number indicating
# how many times it is used in that source code file, from the format
#    FUNCTION HEADERFILE SOURCEFILE NUMBER
# first to the format 
#    SOURCEFILE,SOURCEFILE,... HEADERFILE FUNCTION NUMBER,NUMBER,...
# to obtain lists of source code files that use the same function; so
# that after sorting the new list we can go on to easily find functions
# that are called from the same combination of source code files and
# declared in the same header file, and combine them in the format
#    SOURCEFILE,SOURCEFILE,... HEADERFILE FUNCTION,FUNCTION,...
#       [NUMBER,NUMBER,...]...
# So the numbers end up (conceptually) in a two-dimensional structure,
# indexed by source code file first and by function afterward.
# This third format, used internally in the second awk command only, is
# immediately taken apart again to write an input file for the dot
# graph drawing tool, each record giving birth to one or more lines of
# the format
#    SOURCEFILE -> FUNCTION,FUNCTION,... [ label NUMBER,NUMBER,... ] 
# and one line of the format
#    FUNCTION,FUNCTION,... -> HEADERFILE [ label NUMBER-OF-SOURCEFILES ]
# The label on the edge to the header file does not add any new
# information, but it makes the graph easier to read.

  join .cdeps.db .cdeps.calls |
  sort |
  awk 'function printout() { 
         if (functionname)
           print callers " " header " " functionname " " amounts
       }
       { if ($1==functionname && $2==header) {
           callers = callers "," $3; amounts = amounts "," $4
         } else {
           printout();
           functionname=$1; header=$2; callers=$3; amounts=$4
         } }
       END { printout() }' |
  sort |
  awk 'function printout() { 
         if (callers) {
           print ""
           arrlen = split(callers, arr, ",");
           for (count=1; count<=arrlen; count++)
             print "\"" arr[count] "\" -> \"" functions \
                   "\" [ label = \"" amounts[count] "\", style = solid ]";
           print "\"" functions "\" -> \"" header \
                 "\" [ label = \"" arrlen "\", style = dashed ]"
         }
       }
       { if ($1==callers && $2==header) { 
           functions = functions "\\n" $3;
           amountslen = split($4, addamounts, ",");
           for (count=1; count<=amountslen; count++)
             amounts[count] = amounts[count] "," addamounts[count]
         } else {
           printout();
           callers=$1; header=$2; functions=$3; split($4, amounts, ",")
         } }
       END { printout() }'

fi

# print footer for .dot file

echo "}"

rm .cdeps.*
