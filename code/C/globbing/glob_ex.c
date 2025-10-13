/*
 * =====================================================================================
 *
 *       Filename:  glob_ex.c
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  02/23/12 16:10:26
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Yosi Izaq (), yizaq@cisco.com
 *        Company:  CISCO
 *
 * =====================================================================================
 */
#include <dirent.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <inttypes.h>

  typedef unsigned long long	uint64_t;

int  main()
{
	DIR *dir;
	struct dirent *ent;
	dir = opendir (".");
	if (dir != NULL) {

	  /* print all the files and directories within directory */
	  while ((ent = readdir (dir)) != NULL) {
	    printf ("%s: len %d, type: %s.\n", ent->d_name, strlen(ent->d_name) , (ent->d_name+strlen(ent->d_name) -3)  );
	    if (!strcmp ((const char *)( ent->d_name+strlen(ent->d_name) -3) , "txt") )
	    {
		    int result = 0;
		    struct stat64 statbuff;
		    result = stat64 (ent->d_name, &statbuff);
		    uint64_t size = statbuff.st_size;

		    printf("Found txt file. Size: %llu \n",size); 
	    }

	  }
	  closedir (dir);
	} else {
	  /* could not open directory */
	  perror ("");
	  return 1;
	}

	return 0;
}
