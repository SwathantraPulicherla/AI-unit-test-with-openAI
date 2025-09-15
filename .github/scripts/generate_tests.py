import os
import re
import subprocess
import requests

HF_API_URL = "https://api-inference.huggingface.co/models/bigcode/starcoder"
HF_HEADERS = {"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"}

def hf_generate(prompt):
    try:
        response = requests.post(HF_API_URL, headers=HF_HEADERS, json={"inputs": prompt})
        response.raise_for_status()
        data = response.json()

        # Handle both dict and list formats
        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"]
        elif isinstance(data, dict) and "generated_text" in data:
            return data["generated_text"]
        else:
            print("Unexpected HF API response:", data)
            return None
    except Exception as e:
        print("Hugging Face API error:", e)
        return None

def get_changed_files():
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
        stdout=subprocess.PIPE, text=True
    )
    return [f.strip() for f in result.stdout.splitlines() if f.endswith('.c')]

def extract_functions(filepath):
    with open(filepath) as f:
        content = f.read()
    pattern = r'\b(?:[A-Za-z_][A-Za-z0-9_\s\*]*?)\s+(\w+)\s*\([^;{]*\)\s*{'
    return set(re.findall(pattern, content))

def append_tests_to_file(test_file, tests):
    with open(test_file, "a") as f:
        for test in tests:
            f.write("\n" + test + "\n")

def main():
    changed_files = get_changed_files()
    if not changed_files:
        print("No .c files changed in the last commit.")
        return

    test_file = "tests/test_calculator.c"
    generated = 0

    for file in changed_files:
        funcs = extract_functions(file)
        for func in funcs:
            prompt = f"""Write a Unity C unit test function named test_{func} 
for the C function: int {func}(int a, int b);
Use TEST_ASSERT macros."""
            
            test_code = hf_generate(prompt)
            if test_code:
                print(f"Generated test for {func}:\n{test_code}\n")
                append_tests_to_file(test_file, [test_code])
                generated += 1

    print(f"\nGenerated {generated} new test(s).")

if __name__ == "__main__":
    main()
