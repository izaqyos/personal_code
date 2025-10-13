# Author Yosi Izaq
# Description: Used in order to extract the user name and password from cisco directory

BEGIN { FS = "([\r\n]+)"; RS= "" }

/mailto/ {
	for ( i = 1; i <= NF; i++ )
		if ( $i ~ /mailto/ )	print $i,$(i+1)
}
