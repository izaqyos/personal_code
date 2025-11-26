class Solution {
public: 

      bool bDebug = false;
    void printMap(const unordered_map<int,vector<char> > & d2lMap)
    {

	    if (bDebug) cout<<"{ ";
	    for (auto ent : d2lMap)
	    {
		if (bDebug) cout<<"{"<<ent.first<<":[";
		for (auto c : ent.second)
		{
			if (bDebug) cout<<c<<",";
		}
		if (bDebug) cout<<"]}, ";
	    }
	    if (bDebug) cout<<" }"<<endl;
    }

    void printVec(string name, const vector<string> vStr)
    {
	if (bDebug) cout<<name<<" :";
	if (bDebug) copy(vStr.begin(), vStr.end(), ostream_iterator<string>(cout,", "));
	if (bDebug) cout<<endl;
    }

    void letCombRec(const unordered_map<int,vector<char> > & d2lMap, vector<string> & vRet,string digits)
    {
        
	if (bDebug) cout<<"letCombRec() called with:"<<endl;
	if (bDebug) cout<<"d2lMap: "<<endl;
	printMap(d2lMap);
	printVec("vRet", vRet);
	if (bDebug) cout<<"digits: "<<digits<<endl;
	if (bDebug) cout<<endl;

        if (digits.empty()) 
        {
            if (bDebug) cout<<"digits empty"<<endl;
            return;
        }
//        else if  (digits.size() == 1)
//        {
//            if (bDebug) cout<<"digits size 1. First char: '"<<digits[0]<<"'"<<endl;
//            for (auto c : d2lMap.at(stoi(digits.substr(0,1))))
//            {
//                if (bDebug) cout<<"Add str: "<<c<<endl;
//                vRet.push_back(string(1,c));
//            }
//            digits.erase(0,1); 
//            letCombRec(d2lMap,vRet,digits);
//            return;
//        }
        else
        {
	    if (bDebug) cout<<"---------------------------------"<<endl;
        //    if (bDebug) cout<<"digits size > 1"<<endl;
            //vRet.clear();
            
            //add to all vRet elements chars in d2lMap[digits[0]]
            //vector <char> vChars = d2lMap[digits[0]];
	    if (vRet.empty())
	    {
		if (bDebug) cout<<"vRet empty, adding first chars"<<endl;
                for (auto c : d2lMap.at(stoi(digits.substr(0,1))))
                {
                    if (bDebug) cout<<"Add str: "<<c<<endl;
                    vRet.push_back(string(1,c));
                }
                digits.erase(0,1); 
                letCombRec(d2lMap,vRet,digits);

	    }
	    else
	    {
		if (bDebug) cout<<"vRet not empty, adding chars"<<endl;
                vector<string> vsTemp,vsTemp1 ;
		int ivsTempAddIndex = 0;
		vsTemp1 = vRet;
	        printVec("vsTemp1", vsTemp1);
                for (auto c : d2lMap.at(stoi(digits.substr(0,1))))
                {
                    for (vector<string>::iterator it = vsTemp1.begin(); it != vsTemp1.end(); ++it )
                    {
                        (*it) += c;
                    }
	            printVec("vsTemp1 after adding chars", vsTemp1);
		    vsTemp.resize(vsTemp.size() + vsTemp1.size());
                    copy(vsTemp1.begin(), vsTemp1.end(), vsTemp.begin() + ivsTempAddIndex);
		    ivsTempAddIndex += vsTemp1.size();
	            printVec("vsTemp after adding chars", vsTemp);
		    vsTemp1 = vRet;
		}
		    vRet.clear();
		    vRet.resize(vsTemp.size());
                    copy(vsTemp.begin(), vsTemp.end(), vRet.begin());
	            printVec("vRet  after adding chars", vRet);

            digits.erase(0,1); 
            letCombRec(d2lMap,vRet,digits);

	    }
            return;
        }
        
    }
    
    vector<string> letterCombinations(string digits) {

            
    unordered_map<int,vector<char> > dig2let = 
	{
	{2,{'a','b','c'}},
	{3,{'d','e','f'}},
	{4,{'g','h','i'}},
	{5,{'j','k','l'}},
	{6,{'m','n','o'}},
	{7,{'p','q','r','s'}},
	{8,{'t','u','v'}},
	{9,{'w','x','y','z'}},
	{1,{}},
	{0,{}}
	};
    
    
    vector<string> vRet;
    
    letCombRec(dig2let, vRet, digits);
    //cout<<"Final vRet: ";
    //copy(vRet.begin(), vRet.end(), ostream_iterator<string>(cout,", "));
    //cout<<endl;
    return vRet;
    }
};