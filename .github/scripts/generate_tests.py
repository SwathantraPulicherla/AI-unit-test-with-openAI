import os
import openai
import re

openai.api_key = os.getenv("OPENAI_API_KEY")

SRC_FILE = "calculator.c"
TEST_FILE = "test_calculator.c"
HEADER_FILE = "calculator.h"

# Extract function signatures from header
with open(HEADER_FILE) as f:
    header = f.read()
functions = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_\s\*\[\]]*)\s+(\w+)\s*\(([^)]*)\)\s*;', header)

print(f"Found functions: {functions}")

# Read existing test file
if os.path.exists(TEST_FILE):
    with open(TEST_FILE) as f:
        test_code = f.read()
else:
    test_code = ""

new_tests = []
for ret_type, func, args in functions:
    print(f"Function: {func}, Return type: {ret_type}, Args: {args}")
    # Check if a test for this function exists
    if f"{func}(" in test_code:
        continue
    # Generate a test case using OpenAI
    prompt = f"Write a Unity C test case for the function: int {func}({args}) in calculator.c. Use TEST_CASE and TEST_ASSERT macros. Only output the test function, no explanation."
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.2,
    )
    test_code = response.choices[0].message.content.strip()
    new_tests.append(test_code)

if new_tests:
    with open(TEST_FILE, "a") as f:
        for test in new_tests:
            f.write("\n" + test + "\n")
    print(f"Generated {len(new_tests)} new test case(s).")
else:
    print("No new test cases generated.")
