#include <stdio.h>
#include "unity.h"

static int tests_run = 0;
static int tests_failed = 0;

void UnityBegin(const char* name) {
    printf("==== Unity Test: %s ===\n", name);
    tests_run = 0;
    tests_failed = 0;
}

void UnityEnd(void) {
    printf("==== Tests Run: %d, Failures: %d ===\n", tests_run, tests_failed);
    if (tests_failed == 0) {
        printf("ALL TESTS PASSED\n");
    }
}

void UnityAssertEqualNumber(int expected, int actual, const char* msg, int line) {
    tests_run++;
    if (expected != actual) {
        printf("FAIL: %s (line %d): expected %d, got %d\n", msg, line, expected, actual);
        tests_failed++;
    }
}
