# Author Yosi Izaq
# Description: Used in order to extract the user name and password from cisco directory

BEGIN { FS = "([\r\n]+)"; RS= "" }
/mailto/ {
	#print "matched mailto"
	for ( i = 1; i <= NF; i++ )
            #Match for result that contains multiple records
		if ( $i ~ /mailto/ )	
        {
                print "match against ", $(i+1)
                if ( $(i+1) ~ /\+[0-9]+/ ) print $i, "xxx", $(i+1)
        }

        #Match for unique ID result
        else if ($i ~ /Voice Mail/) print  $(i), $(i+2)
}

/Work/ {
	#print "matched work"
                for (i=1; i <= NF; i++)
                {
                        printf "Field %d value %s\n",i,$i
                        ##if ($i ~ /[0-9]+/) printf "ext: %s\n",$i
                        ##if ($i ~ /[0-9]+/) print "match phone ", $i
                        if ($i ~ /<strong>/) print "match phone ", $(i+2)
                }
        }
