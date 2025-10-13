/*
 We have defined our own markup language HRML. In HRML, each element consists of a starting and ending tag, and there are attributes associated with each tag. Only starting tags can have attributes. We can call an attribute by referencing the tag, followed by a tilde, '~' and the name of the attribute. The tags may also be nested.
The opening tags follow the format:
<tag-name attribute1-name = "value1" attribute2-name = "value2" ...>
The closing tags follow the format:
</tag-name>
For example:
<tag1 value = "HelloWorld">
<tag2 name = "Name1">
</tag2>
</tag1>
The attributes are referenced as:
tag1~value  
tag1.tag2~name
You are given the source code in HRML format consisting of  lines. You have to answer  queries. Each query asks you to print the value of the attribute specified. Print "Not Found!" if there isn't any such attribute.
Input Format
The first line consists of two space separated integers,  and .  specifies the number of lines in the HRML source program.  specifies the number of queries.
The following  lines consist of either an opening tag with zero or more attributes or a closing tag.There is a space after the tag-name, attribute-name, '=' and value.There is no space after the last value. If there are no attributes there is no space after tag name.
 queries follow. Each query consists of string that references an attribute in the source program.More formally, each query is of the form  ~ where  and  are valid tags in the input.
Constraints


Each line in the source program contains, at max,  characters.
Every reference to the attributes in the  queries contains at max  characters.
All tag names are unique and the HRML source program is logically correct.
A tag can have no attributes as well.
Output Format
Print the value of the attribute for each query. Print "Not Found!" without quotes if there is no such attribute in the source program.

Sample Input
4 3
<tag1 value = "HelloWorld">
<tag2 name = "Name1">
</tag2>
</tag1>
tag1.tag2~name
tag1~name
tag1~value

Sample Output
Name1
Not Found!
HelloWorld
 

Tests logs
[i500695@C02X632CJGH6:2019-02-28 11:48:05:~/work/code/CPP/hackerRank:]523$ g++ -std=c++11 AttributeParserSTD2.cpp  -o AttributeParserSTD2
[i500695@C02X632CJGH6:2019-02-28 11:48:18:~/work/code/CPP/hackerRank:]524$ g++ -std=c++11 AttributeParserSTD.cpp  -o AttributeParserSTD
[i500695@C02X632CJGH6:2019-02-28 11:48:29:~/work/code/CPP/hackerRank:]525$ ./AttributeParserSTD < AttributeParserTestInput.txt 
Name1
Not Found!
HelloWorld
[i500695@C02X632CJGH6:2019-02-28 11:48:39:~/work/code/CPP/hackerRank:]526$ ./AttributeParserSTD2 < AttributeParserTestInput.txt 
Name1
Not Found!
HelloWorld
 */

#include <string>
#include <vector>
#include <iostream>
#include <algorithm>
#include <sstream>
#include <unordered_map>
#include <iterator>

using namespace std;

int main()
{
        bool bDebug = true;
        //bool bDebug = false;
        int n, q;
        cin >> n >> q;
        if (bDebug)
                cout << "n=" << n << ", q=" << q << endl;
        cin.ignore();
        const char openTag = '<';
        const char closeTag = '>';
        const char fwdSlash = '/';
        const char quote = '"';
        const char equals = '=';
        const string strNotFound = "Not Found!";

        unordered_map<string, string> attrDict;
        vector<string> tags;

        for (int i = 0; i < n; ++i)
        {
                string line, token, attr, value;
                getline(cin, line);
                if (bDebug)
                        cout << "got line: " << line << endl;

                istringstream ssline(line); //stream to getline, which has a delim param so we can tokenize by ' '
                while (getline(ssline, token, ' '))
                {
                        if (bDebug)
                                cout << "line[" << i << "]"
                                     << " read token " << token << endl;
                        if (token[0] == openTag)
                        {
                                if (bDebug)
                                        cout << "found tag. token[1]=" << token[1] << endl;
                                if (token[1] == fwdSlash)
                                {
                                        if (bDebug)
                                                cout << "found closing tag" << endl;
                                        tags.pop_back();
                                }
                                else
                                {
                                        if (bDebug) cout << "found opening tag: " << token.substr(1, token.length()-2) << endl;
                                        tags.push_back(token.substr(1, token.length()-2));
                                        //tags.push_back(token.substr(1, token.size()-1));
                                        if (bDebug){
                                                cout << "current tags stack: "<<endl;
                                                std::copy(tags.begin(), tags.end(), ostream_iterator<string>(cout, "."));
                                                cout<<endl;
                                        }
                                }
                        }
                        else
                        {
                                //if (bDebug) cout<<"expecting attr = value "<<endl;
                                if (token[0] == quote)
                                {
                                        value = token.substr(1, token.find_last_of('"') - 1);
                                        //This will copy the tags in tags vector
                                        //std::ostringstream os_tagStr;
                                        //std::copy( tags.begin(), tags.end(), ostream_iterator<string>( os_tagStr ) );
                                        //attrDict[os_tagStr.str()] = value;
                                        //if (bDebug) cout<<"got value "<<value<<", updating map key "<<os_tagStr.str()<<endl;
                                        string tagsConcat = "";
                                        //c++-14 only. hacker rank doesn't support
                                        //std::for_each(tags.begin(), tags.end() - 1, [&tagsConcat](const auto tag) {

                                        if (bDebug){
                                                cout<<"Tags Vector: "<<endl;
                                                std::copy(tags.begin(), tags.end(), ostream_iterator<string>(cout, "."));
                                                cout<<endl;
                                        }
                                        std::for_each(tags.begin(), tags.end() - 1, [&tagsConcat](const string & tag) {
                                                tagsConcat += tag;
                                                tagsConcat.append(1, '.');
                                        });
                                        tagsConcat += tags.back();
                                        tagsConcat += '~';
                                        tagsConcat += attr;
                                        attrDict[tagsConcat] = value;
                                        if (bDebug)
                                                cout << "got value " << value << ", updating map key " << tagsConcat << endl;
                                } //value
                                else if (token[0] == equals)
                                {
                                        if (bDebug)
                                                cout << "read = char " << endl;
                                }
                                else
                                {
                                        attr = token;
                                        if (bDebug)
                                                cout << "reading attribute name= " << attr << endl;

                                } //attribute
                        }
                }
        }

        for (int i = 0; i < q; ++i)
        {
                string line, token, attr, value;
                getline(cin, line);
                if (bDebug)
                        cout << "got query line: " << line << endl;
                if (attrDict.find(line) == attrDict.end())
                {
                        cout << strNotFound << endl;
                }
                else
                {
                        cout << attrDict[line] << endl;
                }
        }
}
