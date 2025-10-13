/*
 * =====================================================================================
 *
 *       Filename:  auto.cpp
 *
 *    Description:  Demo auto C11 keyword 
 *
 *        Version:  1.0
 *        Created:  12/31/14 18:38:09
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Yosi Izaq
 *   Organization:  
 *
[yizaq@YIZAQ-M-D1BW:Sun Jan 04:~/Desktop/Work/code/C11:]$ clang++ -std=c++11 -stdlib=libc++ -Weverything auto.cpp 
auto.cpp:27:23: warning: consecutive right angle brackets are incompatible with C++98 (use '> >') [-Wc++98-compat]
map<string, vector<int>> my_map = { {"1st", {1,2,3}} , {"2nd", {9,2,3,10}}, {"3rd", {2,2,2,1,2,3}}};
                      ^~
                      > >
auto.cpp:27:37: warning: constructor call from initializer list is incompatible with C++98 [-Wc++98-compat]
map<string, vector<int>> my_map = { {"1st", {1,2,3}} , {"2nd", {9,2,3,10}}, {"3rd", {2,2,2,1,2,3}}};
                                    ^~~~~~~~~~~~~~~~
auto.cpp:27:45: warning: initialization of initializer_list object is incompatible with C++98 [-Wc++98-compat]
map<string, vector<int>> my_map = { {"1st", {1,2,3}} , {"2nd", {9,2,3,10}}, {"3rd", {2,2,2,1,2,3}}};
                                            ^~~~~~~
auto.cpp:27:56: warning: constructor call from initializer list is incompatible with C++98 [-Wc++98-compat]
map<string, vector<int>> my_map = { {"1st", {1,2,3}} , {"2nd", {9,2,3,10}}, {"3rd", {2,2,2,1,2,3}}};
                                                       ^~~~~~~~~~~~~~~~~~~
auto.cpp:27:64: warning: initialization of initializer_list object is incompatible with C++98 [-Wc++98-compat]
map<string, vector<int>> my_map = { {"1st", {1,2,3}} , {"2nd", {9,2,3,10}}, {"3rd", {2,2,2,1,2,3}}};
                                                               ^~~~~~~~~~
auto.cpp:27:77: warning: constructor call from initializer list is incompatible with C++98 [-Wc++98-compat]
map<string, vector<int>> my_map = { {"1st", {1,2,3}} , {"2nd", {9,2,3,10}}, {"3rd", {2,2,2,1,2,3}}};
                                                                            ^~~~~~~~~~~~~~~~~~~~~~
auto.cpp:27:85: warning: initialization of initializer_list object is incompatible with C++98 [-Wc++98-compat]
map<string, vector<int>> my_map = { {"1st", {1,2,3}} , {"2nd", {9,2,3,10}}, {"3rd", {2,2,2,1,2,3}}};
                                                                                    ^~~~~~~~~~~~~
auto.cpp:27:35: warning: initialization of initializer_list object is incompatible with C++98 [-Wc++98-compat]
map<string, vector<int>> my_map = { {"1st", {1,2,3}} , {"2nd", {9,2,3,10}}, {"3rd", {2,2,2,1,2,3}}};
                                  ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
auto.cpp:27:26: warning: no previous extern declaration for non-static variable 'my_map' [-Wmissing-variable-declarations]
map<string, vector<int>> my_map = { {"1st", {1,2,3}} , {"2nd", {9,2,3,10}}, {"3rd", {2,2,2,1,2,3}}};
                         ^
auto.cpp:27:26: warning: declaration requires an exit-time destructor [-Wexit-time-destructors]
auto.cpp:27:26: warning: declaration requires a global destructor [-Wglobal-constructors]
auto.cpp:31:10: warning: 'auto' type specifier is incompatible with C++98 [-Wc++98-compat]
    for (auto itr = begin(my_map) ; itr != end(my_map) ; ++itr)
         ^~~~
auto.cpp:35:18: warning: 'auto' type specifier is incompatible with C++98 [-Wc++98-compat]
            for (auto vitr = begin(itr->second) ; vitr != end(itr->second) ; ++vitr)
                 ^~~~
13 warnings generated.
[yizaq@YIZAQ-M-D1BW:Sun Jan 04:~/Desktop/Work/code/C11:]$ a.out 
{{"1st",{1,2,3,},{"2nd",{9,2,3,10,},{"3rd",{2,2,2,1,2,3,},}
 * =====================================================================================
 */
#include <stdlib.h>
#include <stdlib.h>
#include <map>
#include <vector>
#include <string>

using namespace std;

// init in this form is available in C11
map<string, vector<int>> my_map = { {"1st", {1,2,3}} , {"2nd", {9,2,3,10}}, {"3rd", {2,2,2,1,2,3}}};
 
template <typename T1, typename T2>
auto compose(T1 t1, T2 t2) -> decltype(t1 + t2)
{
	   return t1+t2;
}

int main(){
    printf("{");
    for (auto itr = begin(my_map) ; itr != end(my_map) ; ++itr)
    {
    	printf("{\"%s\",", (itr->first).c_str());
    	printf("{");
            for (auto vitr = begin(itr->second) ; vitr != end(itr->second) ; ++vitr)
    	{
    		printf("%d,", *vitr);
    	}
            printf("},");
    }
    
    printf("}\n");

    auto v = compose(2, 3.14); // v's type is double
    printf("Result: %f\n",v);

    printf("using foreach...\n");
    printf("{");
    for (auto fitr : my_map)
    {
    	printf("{\"%s\",", (fitr.first).c_str());
    	printf("{");
        for (auto fvitr : fitr.second)
    	{
    		printf("%d,", fvitr);
    	}
            printf("},");

    }
    printf("}\n");

    return 0;
}


