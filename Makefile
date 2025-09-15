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
	gcov calculator.c test_calculator.c unity/unity.c
	lcov --capture --directory . --output-file coverage.info
	genhtml coverage.info --output-directory coverage_html

clean:
	rm -f *.o *.gcda *.gcno *.gcov test_calculator coverage.info
	rm -rf coverage_html
