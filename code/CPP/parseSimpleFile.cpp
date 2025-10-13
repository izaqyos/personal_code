/*
 * =====================================================================================
 *
 *       Filename:  parseSimpleFile.cpp
 *
 *    Description:  parse simple text file - diskQuotas.cfg example
 *
 *        Version:  1.0
 *        Created:  01/10/12 14:24:06
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Yosi Izaq (), yizaq@cisco.com
 *        Company:  CISCO
 *
 * =====================================================================================
 */
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <assert.h>

using namespace std;


//split for single length 1 delimiter
int split( vector<string> & theStringVector,  /* Altered/returned value */ const  string  & theString, const  string  & theDelimiter )
{
  assert( (theDelimiter.size() > 0 ) &&  "Delimiter must be longer than 0" ); 

  size_t  start = 0, end = 0;

  while ( end != string::npos )
  {
    end = theString.find( theDelimiter, start );

      // If at end, use length=maxLength.  Else use length=end-start.
    theStringVector.push_back( theString.substr( start,
                   (end == string::npos) ? string::npos : end - start ) );

      // If at end, use start=maxSize.  Else use start=end+delimiter.
    start = (   ( end > (string::npos - theDelimiter.size()) )
              ?  string::npos  :  end + theDelimiter.size()    );
  }
}

/* 
//--------------------------------------------------------------------------------
//tokenizer for multiple delimiters, like all whitespace
//Header file
class Tokenizer 
{
    public:
        static const std::string DELIMITERS;
        Tokenizer(const std::string& str);
        Tokenizer(const std::string& str, const std::string& delimiters);
        bool NextToken();
        bool NextToken(const std::string& delimiters);
        const std::string GetToken() const;
        void Reset();
    protected:
        size_t m_offset;
        const std::string m_string;
        std::string m_token;
        std::string m_delimiters;
}

//CPP file
const string Tokenizer::DELIMITERS(" \t\n\r");

Tokenizer::Tokenizer(const std::string& s) :
    m_string(s), 
    m_offset(0), 
    m_delimiters(DELIMITERS) {}

Tokenizer::Tokenizer(const std::string& s, const std::string& delimiters) :
    m_string(s), 
    m_offset(0), 
    m_delimiters(delimiters) {}

bool Tokenizer::NextToken() 
{
    return NextToken(m_delimiters);
}

bool Tokenizer::NextToken(const std::string& delimiters) 
{
    size_t i = m_string.find_first_not_of(delimiters, m_offset);
    if (string::npos == i) 
    {
        m_offset = m_string.length();
        return false;
    }

    size_t j = m_string.find_first_of(delimiters, i);
    if (string::npos == j) 
    {
        m_token = m_string.substr(i);
        m_offset = m_string.length();
        return true;
    }

    m_token = m_string.substr(i, j - i);
    m_offset = j;
    return true;
}

//--------------------------------------------------------------------------------
 */

int main()
{
	cout << "Starting Parser\n";
	const string fname = "diskQuotas.cfg";
	string word1, word2, line;
	int num;
	//
  //check to see if the file is opened:
	ifstream myfile(fname.c_str());
  if (myfile.is_open())
  {
    //while there are still lines in the
    //file, keep reading:
    while (! myfile.eof() )
    {
      //place the line from myfile into the
      //line variable:
      getline (myfile,line);

      if (line[0] == '#') // ~='^#'
      {
	      cout <<"found comment line: "<<endl<<line<<endl;
      }
      else
      {

	//ToDo, if not start # then sscanf %s %s %d
      	//display the line we gathered:
      	cout << line << endl;

	 vector<string> v;

	 // using split - work 4 single space
	  //split( v, line , " " );

//      //using tokenizer
//	Tokenizer s(line);
//	while (s.NextToken())
//	{
//		v.push_back(s.GetToken());
//	}
//
//
//#define SHOW(I,X)   cout << "[" << (I) << "]\t " # X " = \"" << (X) << "\"" << endl
//	  for( unsigned int i = 0;  i < v.size();   i++ )
//	    SHOW( i, v[i] );

	 int length = 0;
	 char buffer[256];
	 int token_num = 0;
	 string LOCAL_STORE_KEYWORD="local-store";
	 length = line.copy(buffer, line.length());
	char *p = strtok(buffer, " \t\n\r");
	if ( ! LOCAL_STORE_KEYWORD.compare(p) )
	{
		printf ("Found local store configuration line");

		while (p) {
		    printf ("Token: %s\n", p);
		    token_num++;
		    if (token_num == 3){
			    printf ("Local store quota is %d \n", atoi(p));
		    }
		    p = strtok(NULL, " ");
		}
	}

// Print all words in all lines
//	while (p) {
//	    printf ("Token: %s\n", p);
//	    p = strtok(NULL, " ");
//	}
      }
    }

    //close the stream:
    myfile.close();
  }

  else cout << "Unable to open file";

	//ifstream ifs(fname.c_str());
	/*
	if (!ifs){
		cout<< "can't open file "<< fname <<" \n";
		return 1;
	}

	// read a line using the extraction operator
	if(ifs >> word1 >> word2 >> num) {
		cout << "reading content line\n";

		cout << "[ "
		<< word1 << ' '
		<< word2 << ' '
		<< num << " ]"
		<< endl;
	}
	else {

		char line_s [255];
		cout << "reading line\n";
		ifs.getline(line_s, 255) ;
		if (ifs) cout << "[ " << line_s << " ]" << endl;
	
	}
	// discard whitespace
	//ifs.ignore(10000,'\n');
	// read a line using getline
	if(getline(ifs,line)) {
		cout << "[ " << line << " ]" << endl;
	}
  */
	return 0;
}
