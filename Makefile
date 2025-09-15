CC=gcc
CFLAGS=-Wall -Wextra -fprofile-arcs -ftest-coverage -O0
LDFLAGS=-lgcov
SRC=calculator.c unity/unity.c test_calculator.c
OBJ=$(SRC:.c=.o)

all: test_calculator

test_calculator: $(SRC)
	$(CC) $(CFLAGS) -o $@ $(SRC) $(LDFLAGS)

run-tests: test_calculator
	./test_calculator

coverage: test_calculator
	./test_calculator
	gcov test_calculator-calculator.gcno test_calculator-test_calculator.gcno test_calculator-unity.gcno -o . || true
	mv calculator.c.gcov test_calculator-calculator.c.gcov || true
	mv test_calculator.c.gcov test_calculator-test_calculator.c.gcov || true
	mv unity.c.gcov test_calculator-unity.c.gcov || true
	lcov --capture --directory . --output-file coverage.info --ignore-errors source
	# Only include calculator.c in the final coverage report
	lcov --remove coverage.info '*/unity/*' '*/test_*' --output-file coverage.info
	genhtml coverage.info --output-directory coverage_html --ignore-errors source --substitute /workspaces/AI-unit-test-with-openAI/ .

clean:
	rm -f *.o *.gcda *.gcno *.gcov test_calculator coverage.info
	rm -rf coverage_html
