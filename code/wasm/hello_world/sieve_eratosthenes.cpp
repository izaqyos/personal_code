#include <iostream>
#include <vector>

using namespace std;

sieve_of_eratosthenes(vector<uint>&& primes, uint limit) {
    bool is_prime[limit+1];
    std::fill_n(is_prime, limit+1, true);

    for (int i=2; i*i<=limit; i++) { //loop over all nums until sqr(limit). 0,1 are not primes so we start at 2
        if (is_prime[i]) { //assume all are true, then cross over multiples of a prime
            for (int j= i*i; j<=limit; j+=i) { // we can safely assume all primes <i^2 are already marked by prev prime marking
                is_prime[j] = false;
            }
        }
    }

    for (size_t i = 2; i < limit; i++)
    {
        if (is_prime[i])
        {
            primes.push_back(is_prime[i]);
        }
    }
    return primes;
}

int main(int argc, char const *argv[])
{
    cout<<"Please provide a positive number. All prime numbers <= this number will be printed"<<endl;
    uint limit;
    cin<<limit;
    vector<uint> primes;
    sieve_of_eratosthenes(primes, limit)
    for (size_t i = 0; i < primes.size(); i++)
    {
        /* code */
    }
    
    return 0;
}
