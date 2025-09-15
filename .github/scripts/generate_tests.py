import os
import re
import subprocess
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_changed_files():
    """Get .c files changed in the last commit."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
        stdout=subprocess.PIPE, text=True
    )
    return [f.strip() for f in result.stdout.splitlines() if f.endswith('.c')]

def extract_functions(filepath):
    """Extract all function signatures and names from a C source file."""
    with open(filepath) as f:
        content = f.read()
    # This regex matches most C function signatures (single-line)
    pattern = r'((?:[A-Za-z_][A-ZaZ0-9_\s\*\(\)]*?)\s+(\w+)\s*\([^;{]*\)\s*{)'
    return list(re.finditer(pattern, content))

def test_exists(test_file, func_name):
    """Check if a test for the function already exists in the test file."""
    if not os.path.exists(test_file):
        return False
    with open(test_file) as f:
        return f"test_{func_name}" in f.read()

def generate_test(signature, func_name):
    """Generate a Unity test function for the given function signature using OpenAI."""
    prompt = f"""Write a Unity C unit test function named test_{func_name} for the following C function:
{signature};

The test should use TEST_ASSERT macros and cover at least one typical use case."""
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=200,
            temperature=0.2,
            n=1,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return None

def append_tests_to_file(test_file, tests):
    """Append generated test functions to the test file."""
    with open(test_file, "a") as f:
        for test in tests:
            f.write("\n" + test + "\n")

def main():
    test_file = "test_calculator.c"
    # Scan all source/header files for functions
    source_files = [f for f in os.listdir(".") if f.endswith(".c") or f.endswith(".h")]
    generated = 0
    for file in source_files:
        for match in extract_functions(file):
            signature, func_name = match.groups()
            if not test_exists(test_file, func_name):
                test_code = generate_test(signature, func_name)
                if test_code:
                    print(f"Generated test for {func_name}:\n{test_code}\n")
                    append_tests_to_file(test_file, [test_code])
                    generated += 1
    print(f"\nGenerated {generated} new test(s).")

if __name__ == "__main__":
    main()
