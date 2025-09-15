import os
import re
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")  # Or Hugging Face if you want later

SRC_DIR = "."  # root folder containing your .c files
TEST_FILE = "tests/test_calculator.c"

# Regex for function definitions (skip forward declarations & comments)
FUNC_PATTERN = re.compile(
    r'^\s*(?:[A-Za-z_][A-Za-z0-9_\s\*]*?)\s+(\w+)\s*\([^;{]*\)\s*{',
    re.MULTILINE
)


def extract_functions_from_c(filepath):
    with open(filepath) as f:
        content = f.read()
    return set(FUNC_PATTERN.findall(content))


def get_all_c_functions(src_dir):
    functions = set()
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".c") and "test" not in file:  # skip test files
                functions |= extract_functions_from_c(os.path.join(root, file))
    return functions


def test_exists(test_file, func_name):
    if not os.path.exists(test_file):
        return False
    with open(test_file) as f:
        return f"test_{func_name}" in f.read()


def generate_test(func_name):
    # Keep it simple: generate placeholder test, not real AI code
    return f"""
// TODO: Write real test for {func_name}
void test_{func_name}() {{
    // Copilot/AI can expand this
}}
"""


def append_tests_to_file(test_file, tests):
    os.makedirs(os.path.dirname(test_file), exist_ok=True)
    with open(test_file, "a") as f:
        for test in tests:
            f.write("\n" + test + "\n")


def main():
    all_funcs = get_all_c_functions(SRC_DIR)
    print(f"Found {len(all_funcs)} function(s) in project.")

    new_tests = []
    for func in sorted(all_funcs):
        if not test_exists(TEST_FILE, func):
            print(f"Generating test stub for: {func}")
            new_tests.append(generate_test(func))

    if new_tests:
        append_tests_to_file(TEST_FILE, new_tests)
        print(f"\n✅ Added {len(new_tests)} new test stub(s) to {TEST_FILE}.")
    else:
        print("\n🎉 All functions already have test stubs!")


if __name__ == "__main__":
    main()
