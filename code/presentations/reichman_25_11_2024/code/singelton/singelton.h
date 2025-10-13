// singleton.h
#ifndef SINGLETON_H
#define SINGLETON_H

class Singleton {
public:
  static Singleton* getInstance();

  // Example method
  void doSomething();

private:
  Singleton() {}  // Private constructor to prevent direct instantiation
  static Singleton* instance;
};

#endif // SINGLETON_H
