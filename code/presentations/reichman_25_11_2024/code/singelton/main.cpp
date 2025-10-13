// main.cpp
#include "singleton.h"

int main() {
  // Get the singleton instance
  Singleton* s1 = Singleton::getInstance();
  s1->doSomething();

  // Try to create another instance (this will return the same instance)
  Singleton* s2 = Singleton::getInstance();
  s2->doSomething();

  return 0;
}
