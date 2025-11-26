class Solution {
public:

string sayNum(string str)
{
	//Get a str representing a number say 1211 ans "say" it. 
	// e.g. return 111221 (as in one 1, one 2, two 1)
	string ret;

	char lastSeen,c;
	unsigned int rep = 0;
	for (int i=0; i<str.length();++i)
	{
		c=str[i];
		if(i == 0) 
		{
			lastSeen = c;
		}

		if (c==lastSeen)
		{
			rep++;
		}
		else
		{
			ret+= to_string(rep) + lastSeen ;
			rep=1;
			lastSeen = c;
		}
	//	cout<<"sayNum(): c: "<<c<<", last: "<<lastSeen<<", rep: "<<rep<<", ret="<<ret<<endl;
	}

    ////for generating sequence...
	//ret+= to_string(rep) + lastSeen + ",";
	
	////for saying just one num
	ret+= to_string(rep) + lastSeen;
	return ret;


}

string takeLastField(string str) //get 1, 11, 21, 1211, etc , return last, e.g. 1211
{
    string lastField(str.substr(0, str.length()-1)); //peel off last ,
    if (lastField.find(',') != string::npos) 
    {
        lastField = lastField.substr(lastField.find_last_of(',', string::npos));    
    }
    return lastField;
}

    string countAndSay(int n) {

    if ( n <=0 ) return "1";
    string ret;  
    
    for (int i=n;i>0;--i )
        {
            if (ret.empty()) ret="1";
            else
            {
                /*
                //Thought they wanted whole sequence. turns out they only want last field...
                string lastField(ret.substr(0, ret.length()-1));
                if (lastField.find(',') != string::npos) 
                {
                    lastField = lastField.substr(lastField.find_last_of(',', string::npos));    
                }
                // else // //no more '' -> this is first "1," now "1"
	            
	            ret+=" "+sayNum(lastField);
                */ 
                
                ret = sayNum(ret);
            }
        }
        
        
        return ret;
    }
};