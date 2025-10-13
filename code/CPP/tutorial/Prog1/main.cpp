#include <iostream>
using namespace std;

// oneline comment
void printMyName(unsigned int times)
{
    /*
    multi
    line
    comment
    */
    const string name("yosi");

    for (size_t i = 0; i < times; i++)
    {
        cout << name << endl;
    }
}

void io_demo_string_w_spaces(){
//to read string containing spaces use getline. e.g.
    string favoriteGOTCharacter;
    cout<<"Please enter name of your favorite GoT character"<<endl;
    getline(std::cin, favoriteGOTCharacter);
    cout<<"your favorite GoT character is "<<favoriteGOTCharacter<<endl;
}

void io_demo() {
    int age {46};
    cout<<"age is "<<age<<endl;
    cerr<<"error msg"<<endl;
    clog<<"log msg"<<endl;

    char name[200];
    cout<<"what is your name?"<<endl;
    cin>>name;

    string lastname;
    cout<<"what is your last name?"<<endl;
    cin>>lastname;
    cout<<"name: "<<name<<" "<<lastname<<endl;

    string profession;
    int yearsOfExperience;
    cout<<"Please enter your profession and years of experience separated by spaces"<<endl;
    cin>>profession>>yearsOfExperience;
    cout<<"profession: "<<profession<<", years of experience "<<yearsOfExperience<<endl;

}

void numberSystemsFourteen(){
    int n1 = 14; //decimal
    int n2 = 016; //octal
    int n3 = 0x0e; //hexadecimal
    int n4 = 0b00001110; //c++-14 binary
    cout<<"14 as decimal "<<n1<<endl;
    cout<<"14 as octal "<<n2<<endl;
    cout<<"14 as hexadecimal "<<n3<<endl;
    cout<<"14 as binary "<<n4<<endl;
}

void floatingPoint() {
    float n1{1.101101101101101101101101101101101101101101f};
    double n2{1.1012354};
    long double n3{1.101234234234234234234234234234234234234234234234234234234234234234234234L};
    // cout<<std::setprecision(20); //set precision to 20 digits
    cout<<"sizeof float "<<sizeof(float)<<endl; // can handle max 7 digits
    cout<<"sizeof double "<<sizeof(double)<<endl; // can handle max 15 digits
    cout<<"sizeof long double "<<sizeof(long double)<<endl;
    cout<<"can divide float by zero. ex: "<<n1/0<<endl;
    cout<<"can divide negative float by zero. ex: "<<-n1/0<<endl;
    cout<<"can divide zero by zero. ex: "<<0.0/0.0<<endl;
}

void bracedInit() {
    int garbageVal;
    int initToZero{};
    int initToTen{10};
    int initFromExpression{initToTen+initToZero};
    // wontCompileBCInitFromUndeclared{foo+bar};
    // int initWithNarrowingConversion{3.2}; //  warning: implicit conversion from 'double' to 'int' changes value from 3.2 to 3 [-Wliteral-conversion]
}

void asciiEncoding(){
    char a = 'a';
    char b{'b'};
    char A = 65;
    cout<<"char a "<<a<<", A "<<A<<", values: a="<<static_cast<int>(a)<<", A="<<static_cast<int>(A)<<endl;
}

int main()
{
    auto res = (10 <=> 20) > 0;
    std::cout << res << endl;
    // printMyName(10);
    // io_demo_string_w_spaces();
    // io_demo();
    numberSystemsFourteen();
    asciiEncoding();
    floatingPoint();

}