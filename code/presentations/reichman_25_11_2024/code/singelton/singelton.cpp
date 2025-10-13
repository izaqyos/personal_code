// singleton.cpp
#include "singleton.h"
#include <iostream>

Singleton* Singleton::instance = nullptr;

Singleton* Singleton::getInstance() {
  if (instance == nullptr) {
    instance = new Singleton();
  }
  return instance;
}

void Singleton::doSomething() {
  std::cout << "Singleton doing something...\n";
}
