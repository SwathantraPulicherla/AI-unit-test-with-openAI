
#include "unity/unity.h"
#include "calculator.h"

TEST_CASE(test_add_positive) {
    TEST_ASSERT_EQUAL_INT(5, add(2, 3));
}

TEST_CASE(test_add_negative) {
    TEST_ASSERT_EQUAL_INT(1, add(2, -1));
}

int main(void) {
    UnityBegin("test_calculator.c");
    RUN_TEST(test_add_positive);
    RUN_TEST(test_add_negative);
    UnityEnd();
    return 0;
}
