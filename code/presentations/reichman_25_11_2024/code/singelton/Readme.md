Singelton

# install google test
brew install googletest

# compile 
g++ -std=c++11 -o singleton_test singleton.cpp singleton_test.cpp -lgtest -lgtest_main -lpthread

# run
./singleton_test
