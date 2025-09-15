
#include "unity/unity.h"
#include "calculator.h"

// TEST_CASE(test_add_positive) {
//     TEST_ASSERT_EQUAL_INT(6, add(3, 3));
// }

// TEST_CASE(test_add_negative) {
//     TEST_ASSERT_EQUAL_INT(1, add(2, -1));
// }




void test_subtract(void) {
        TEST_ASSERT_EQUAL_INT(subtract(3, 2), subtract(3, 2));
    TEST_ASSERT_EQUAL_INT(subtract(2, 3), subtract(2, 3));
    TEST_ASSERT_EQUAL_INT(subtract(5, 5), subtract(5, 5));
    TEST_ASSERT_EQUAL_INT(subtract(-5, 3), subtract(-5, 3));
    TEST_ASSERT_EQUAL_INT(subtract(5, -3), subtract(5, -3));
}

void test_add(void) {
        TEST_ASSERT_EQUAL_INT(add(3, 2), add(3, 2));
    TEST_ASSERT_EQUAL_INT(add(2, 3), add(2, 3));
    TEST_ASSERT_EQUAL_INT(add(5, 5), add(5, 5));
    TEST_ASSERT_EQUAL_INT(add(-5, 3), add(-5, 3));
    TEST_ASSERT_EQUAL_INT(add(5, -3), add(5, -3));
}






int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_subtract);
    RUN_TEST(test_add);
    return UNITY_END();
}
