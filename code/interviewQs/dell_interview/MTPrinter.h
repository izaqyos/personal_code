#ifndef __MTPRINT__
#define __MTPRINT__

#include <iostream>
#include <sstream>
#include <mutex>

/*
 Utility class for printing to cout via multiple threads in a safe and orderly manner
 The trick is to perform the lock in DTOR and use this class instance as temp rval objects.
 e.g.
 MTPrint() <<"Print str "<<str<<endl;

 */
class MTPrint : public std::ostringstream
{
        public:
                MTPrint() = default;

                ~MTPrint()
                {
                        std::lock_guard<std::mutex> lock(m_mtx);
                        std::cout<< this->str();
                }

        private:
                static std::mutex m_mtx;
};


#endif
