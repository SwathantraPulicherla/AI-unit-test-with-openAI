CC = gcc
CFLAGS = -Wall -Wextra -fprofile-arcs -ftest-coverage -O0
LDFLAGS = -lgcov
SRC = calculator.c unity/unity.c test_calculator.c
TARGET = test_calculator

.PHONY: all clean run-tests coverage

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $@ $(SRC) $(LDFLAGS)

run-tests: $(TARGET)
	./$(TARGET)

coverage: $(TARGET)
	./$(TARGET)
	gcov calculator.c -o . || true
	gcov test_calculator.c -o . || true
	gcov unity/unity.c -o . || true
	lcov --capture --directory . --output-file coverage.info --ignore-errors source
	lcov --remove coverage.info '*/unity/*' '*/test_*' --output-file coverage.info
	genhtml coverage.info --output-directory coverage_html --ignore-errors source --synthesize-missing

clean:
	rm -f *.o *.gcda *.gcno *.gcov $(TARGET) coverage.info
	rm -rf coverage_html