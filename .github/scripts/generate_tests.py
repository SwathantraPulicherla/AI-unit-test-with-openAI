import os
import re
from huggingface_hub import InferenceClient

# Set your Hugging Face token as environment variable HF_TOKEN
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise RuntimeError("Please set the HF_TOKEN environment variable.")

client = InferenceClient(HF_TOKEN)

# Path to your main test file
TEST_FILE = "tests/test_calculator.c"

# Directory to scan for source files
SRC_DIR = "."

def find_c_files(src_dir):
    """Recursively find all .c files in the given directory."""
    c_files = []
    for root, _, files in os.walk(src_dir):
        for f in files:
            if f.endswith(".c"):
                c_files.append(os.path.join(root, f))
    return c_files

def extract_functions(file_path):
    """Extract all function signatures and names from a C source file."""
    pattern = r'([A-Za-z_][A-Za-z0-9_\s\*\(\)]*?\s+(\w+)\s*\([^;{]*\)\s*){'
    with open(file_path) as f:
        content = f.read()
    return [(m.group(1).strip(), m.group(2)) for m in re.finditer(pattern, content)]

def test_exists(func_name, test_file=TEST_FILE):
    """Check if a test for this function already exists."""
    if not os.path.exists(test_file):
        return False
    with open(test_file) as f:
        return f"test_{func_name}" in f.read()

def generate_test_for_function(func_signature, func_name):
    """Call Hugging Face to generate a unit test for the given function."""
    prompt = f"""
Write a C Unity unit test function named test_{func_name} for the following function:

{func_signature};

Use TEST_ASSERT macros and cover at least one typical use case.
"""
    try:
        response = client.text_generation(
            model="bigcode/starcoderbase",   # Change if you want a different code model
            prompt=prompt,
            max_new_tokens=200
        )
        return response.generated_text
    except Exception as e:
        print(f"Hugging Face API error: {e}")
        return None

def append_tests_to_file(tests):
    """Append generated tests to the test file."""
    os.makedirs(os.path.dirname(TEST_FILE), exist_ok=True)
    with open(TEST_FILE, "a") as f:
        for test in tests:
            f.write("\n" + test + "\n")

def main():
    c_files = find_c_files(SRC_DIR)
    generated_count = 0
    for c_file in c_files:
        for signature, func_name in extract_functions(c_file):
            if not test_exists(func_name):
                test_code = generate_test_for_function(signature, func_name)
                if test_code:
                    print(f"Generated test for {func_name}:\n{test_code}\n")
                    append_tests_to_file([test_code])
                    generated_count += 1
    print(f"\nGenerated {generated_count} new test(s).")

if __name__ == "__main__":
    main()
