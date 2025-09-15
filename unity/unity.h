/*
 * Unity - A Test Framework for C
 * https://github.com/ThrowTheSwitch/Unity
 * This is a minimal Unity runner for single test file usage.
 */
#ifndef UNITY_H
#define UNITY_H

void UnityBegin(const char* name);
void UnityEnd(void);
void UnityAssertEqualNumber(int expected, int actual, const char* msg, int line);
#define TEST_ASSERT_EQUAL_INT(expected, actual) UnityAssertEqualNumber((expected), (actual), #actual, __LINE__)
#define TEST_ASSERT_TRUE(condition) UnityAssertEqualNumber(1, (condition) ? 1 : 0, #condition, __LINE__)
#define TEST_ASSERT_FALSE(condition) UnityAssertEqualNumber(0, (condition) ? 1 : 0, #condition, __LINE__)
#define TEST_CASE(name) void name(void)
#define RUN_TEST(test) do { \
    test(); \
} while(0)

#endif // UNITY_H
