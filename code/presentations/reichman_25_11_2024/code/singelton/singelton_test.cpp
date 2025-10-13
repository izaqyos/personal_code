// singleton_test.cpp
#include "gtest/gtest.h"
#include "singleton.h"

TEST(SingletonTest, UniqueInstance) {
  // Get two instances of the singleton
  Singleton* s1 = Singleton::getInstance();
  Singleton* s2 = Singleton::getInstance();

  // Verify that both pointers point to the same memory address
  EXPECT_EQ(s1, s2);
}

int main(int argc, char **argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
