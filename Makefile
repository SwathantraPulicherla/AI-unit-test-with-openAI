CC=gcc
CFLAGS=-Wall -Wextra -fprofile-arcs -ftest-coverage -O0
LDFLAGS=-lgcov
SRC=calculator.c unity/unity.c test_calculator.c
OBJ=$(SRC:.c=.o)
TARGET=test_calculator

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
	lcov --extract coverage.info '*/calculator.c' --output-file coverage.info
	genhtml coverage.info --output-directory coverage_html --ignore-errors source --substitute 's|/workspaces/AI-unit-test-with-openAI/|./|'

clean:
	rm -f *.o *.gcda *.gcno *.gcov $(TARGET) coverage.info
	rm -rf coverage_html
