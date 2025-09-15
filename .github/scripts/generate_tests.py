import os
import re
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_functions(filepath):
    """Extract all function signatures and names from a C source or header file."""
    with open(filepath) as f:
        content = f.read()
    # Match most C function signatures (single-line)
    pattern = r'((?:[A-Za-z_][A-Za-z0-9_\s\*\(\)]*?)\s+(\w+)\s*\([^;{]*\)\s*{)'
    return list(re.finditer(pattern, content))

def extract_header_functions(filepath):
    """Extract all function signatures and names from a C header file."""
    with open(filepath) as f:
        content = f.read()
    # Match function prototypes in header files
    pattern = r'([A-Za-z_][A-Za-z0-9_\s\*\(\)]*?\s+(\w+)\s*\([^;{]*\)\s*;)'
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
{signature}

The test should use TEST_ASSERT macros and cover at least one typical use case. Only output the test function, no explanation."""
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that writes Unity C unit tests."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.2,
        )
        return response.choices[0].message.content.strip()
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
    generated = 0

    # Scan all .h and .c files in the workspace root for function signatures
    files = [f for f in os.listdir(".") if f.endswith(".c") or f.endswith(".h")]
    for file in files:
        if file.endswith(".h"):
            matches = extract_header_functions(file)
        else:
            matches = extract_functions(file)
        for match in matches:
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
