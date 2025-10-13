/*
 * =====================================================================================
 *
 *       Filename:  ProcShutDownMarkerFile.c
 *
 *    Description:  Setup a marker file to indicate Process was shutdown rather than crashed
 *
 *        Version:  1.0
 *        Created:  01/07/2014 10:55:40
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Yosi Izaq
 *   Organization:  
 *
 * =====================================================================================
 */
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <stdio.h>
#include <sys/stat.h>
#include <time.h>
#include <unistd.h>

/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  main
 *  Description:  
 * =====================================================================================
 */
	int
main ( int argc, char *argv[] )
{
        time_t rawtime;
        struct tm * p_timeinfo;
	FILE	*p_marker;										/* input-file pointer */
	char	*p_marker_file_name = ".lwsmd_maker";		/* input-file name    */

	struct stat   stat_buffer;   
	if (stat (p_marker_file_name , &stat_buffer) )
	{
		printf(" Marker file %s doesn't exist. Process was shutdown correctly. Creting now... \n ", p_marker_file_name);

	        p_marker	= fopen( p_marker_file_name, "a+" );
	        if ( p_marker == NULL ) {
	        	fprintf ( stderr, "couldn't open file '%s'; %s\n", p_marker_file_name, strerror(errno) );
	        	exit (EXIT_FAILURE);
	        }
	        if( fclose(p_marker) == EOF ) {			/* close input file   */ fprintf ( stderr, "couldn't close file '%s'; %s\n", p_marker_file_name, strerror(errno) );
	        	exit (EXIT_FAILURE);
	        }
	}
	else
	{
		printf(" Marker file %s exist. Process was not shutdown correctly!  \n ", p_marker_file_name);
	}


	for (int i=20; i>0; --i) // 20 sec
	{
		time ( &rawtime );
                p_timeinfo = localtime ( &rawtime );
		printf(" Simulate daemon, time - %s\n ", asctime(p_timeinfo));
		sleep(1);

	}

	//proper shutdown, delete marker
	if( remove( p_marker_file_name) != 0 ) perror( "Error deleting marker file" );
	else printf( "Marker file successfully deleted\n" );

	return EXIT_SUCCESS;
}				/* ----------  end of function main  ---------- */

