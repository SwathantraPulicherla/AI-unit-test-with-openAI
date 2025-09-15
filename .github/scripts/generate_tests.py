import os
import re
from huggingface_hub import InferenceClient

def get_hf_token():
    token = os.getenv("HF_TOKEN")
    if not token:
        raise RuntimeError("Hugging Face token not set. Please set HF_TOKEN environment variable.")
    return token

MODEL = "codellama/CodeLlama-7b-hf"

def safe_open(filename, mode="r"):
    # Only allow files in the current directory, no path traversal or absolute paths
    if os.path.isabs(filename) or ".." in filename or filename.startswith("/"):
        raise ValueError("Invalid filename or path.")
    safe_path = os.path.join(os.getcwd(), filename)
    if not os.path.isfile(safe_path):
        raise FileNotFoundError(f"{filename} does not exist.")
    return open(safe_path, mode)

def extract_functions(filepath):
    with safe_open(filepath) as f:
        content = f.read()
    pattern = r'([A-Za-z_][A-Za-z0-9_\s\*\(\)]*?\s+(\w+)\s*\([^;{]*\)\s*;)'
    return list(re.finditer(pattern, content))

def test_exists(test_file, func_name):
    if not os.path.exists(test_file):
        return False
    with safe_open(test_file) as f:
        return f"test_{func_name}" in f.read()

def generate_test(signature, func_name, client):
    prompt = f"""Write a Unity C unit test function named test_{func_name} for the following C function:
{signature}
The test should use TEST_ASSERT macros and cover at least one typical use case. Only output the test function, no explanation."""
    try:
        response = client.text_generation(prompt, max_new_tokens=200, temperature=0.2)
        return response.strip()
    except Exception as e:
        print(f"Hugging Face API error: {e}")
        return None

def append_tests_to_file(test_file, tests):
    with open(test_file, "a") as f:
        for test in tests:
            f.write("\n" + test + "\n")

def main():
    test_file = "test_calculator.c"
    generated = 0

    hf_token = get_hf_token()
    client = InferenceClient(MODEL, token=hf_token)

    files = [f for f in os.listdir(".") if f.endswith(".c") or f.endswith(".h")]
    for file in files:
        matches = extract_functions(file)
        for match in matches:
            signature, func_name = match.groups()
            if not test_exists(test_file, func_name):
                test_code = generate_test(signature, func_name, client)
                if test_code:
                    print(f"Generated test for {func_name}:\n{test_code}\n")
                    append_tests_to_file(test_file, [test_code])
                    generated += 1
    print(f"\nGenerated {generated} new test(s).")

if __name__ == "__main__":
    main()
