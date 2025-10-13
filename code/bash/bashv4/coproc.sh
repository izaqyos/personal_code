coproc { cat coproc.sh; sleep 3; } #sleep is required since this process runs asyn and we don't want it to finish
#before reading its output 

while read -u ${COPROC[0]} line
do
    echo "read line: $line"
done

kill $COPROC_PID