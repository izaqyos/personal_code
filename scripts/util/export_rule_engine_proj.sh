#!/bin/sh 

proj="first_integration"

echo "cleaning project $proj"
rm -fr  /cygdrive/d/temp/$proj
rm -f  /cygdrive/d/temp/$proj.zip

echo "creating swap dir"
cp -r /cygdrive/d/work/projects/$proj  /cygdrive/d/temp/

#echo "removing redundent files of total size:"
#find  /cygdrive/d/temp/$proj  \( -name "*.obj" -o -name "*.pch" \) -exec ls -l '{}' \; | awk ' {size+= $5}  END {print "size: " size "kb" }'

echo "Removing redundent files..."
rm -fr /cygdrive/d/temp/$proj/ACS_CPP_Mockup_files/Debug
rm -fr /cygdrive/d/temp/$proj/ACS_CPP_Mockup_files/generated/DebugDLL
find  /cygdrive/d/temp/$proj  \( -name "*.obj" -o -name "*.pch" \) -exec rm -f  '{}' \;

echo "creating project archive."
cd /cygdrive/d/temp/
zip -r $proj.zip $proj 

echo "cleaning swap"
rm -fr  /cygdrive/d/temp/$proj
echo "archive created at /cygdrive/d/temp/$proj.zip size `ls -lsa    /cygdrive/d/temp/$proj.zip | awk '{print $6}'`"

