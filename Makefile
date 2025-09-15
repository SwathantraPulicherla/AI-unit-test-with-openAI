MakefileCC=gcc
CFLAGS=-Wall -Wextra -fprofile-arcs -ftest-coverage -O0
LDFLAGS=-lgcov
SRC=calculator.c unity/unity.c test_calculator.c
OBJ=$(SRC:.c=.o)
CC = gcc
CFLAGS = -Wall -Wextra -fprofile-arcs -ftest-coverage -O0
LDFLAGS = -lgcov
SRC = calculator.c unity/unity.c test_calculator.c
TARGET = test_calculator

all: test_calculator
.PHONY: all clean run-tests coverage

test_calculator: $(SRC)
all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $@ $(SRC) $(LDFLAGS)

run-tests: test_calculator
	./test_calculator
run-tests: $(TARGET)
	./$(TARGET)

coverage: test_calculator
	./test_calculator
	gcov test_calculator-calculator.gcno test_calculator-test_calculator.gcno test_calculator-unity.gcno -o . || true
	mv calculator.c.gcov test_calculator-calculator.c.gcov || true
	mv test_calculator.c.gcov test_calculator-test_calculator.c.gcov || true
	mv unity.c.gcov test_calculator-unity.c.gcov || true
coverage: $(TARGET)
	./$(TARGET)
	# Generate gcov files
	gcov calculator.c -o . || true
	gcov test_calculator.c -o . || true
	gcov unity/unity.c -o . || true
	# Capture coverage data
	lcov --capture --directory . --output-file coverage.info --ignore-errors source
	# Only include calculator.c in the final coverage report
	lcov --remove coverage.info '*/unity/*' '*/test_*' '*/unity.c' '*/test_calculator.c' --output-file coverage.info
	genhtml coverage.info --output-directory coverage_html
	# Generate HTML report
	genhtml coverage.info --output-directory coverage_html --ignore-errors source

clean:
	rm -f *.o *.gcda *.gcno *.gcov test_calculator coverage.info
	rm -f *.o *.gcda *.gcno *.gcov $(TARGET) coverage.info
	rm -rf coverage_html