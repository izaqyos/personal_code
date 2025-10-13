/*
 * =====================================================================================
 *
 *       Filename:  calculateFileSize.c
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  12/18/11 11:40:23
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Yosi Izaq (), yizaq@cisco.com
 *        Company:  CISCO
 *
 * =====================================================================================
 */
#include <stdio.h>
#include <sys/stat.h>

int main(void)
{

   FILE *fp;
   char filename[80];
   long length;

   printf("input file name:");
   gets(filename);
   fp=fopen(filename,"rb");

   if(fp==NULL) {
      printf("file not found!\n");
   }
   else {
      fseek(fp,0L,SEEK_END);
      length=ftell(fp);
      printf("the file's length using fseek is %1dB\n",length);
      fseek(fp,0L,SEEK_SET);
      fclose(fp);

	struct stat st;
	stat(filename, &st);
	unsigned int size = st.st_size;
       printf("the file's length using stat is %1dB\n",size);
   }

   return 0;
}


