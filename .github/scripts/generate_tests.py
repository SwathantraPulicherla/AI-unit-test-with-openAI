import os
import re
import requests

# Hugging Face API setup
HF_API_TOKEN = os.getenv("HF_TOKEN")  # use GitHub secret HF_TOKEN
MODEL = "bigcode/starcoder"  # can change to codellama or others

def call_huggingface(prompt: str) -> str:
    url = f"https://api-inference.huggingface.co/models/{MODEL}"
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 300}}
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise RuntimeError(f"Hugging Face API error: {response.text}")
    
    data = response.json()
    if isinstance(data, list) and "generated_text" in data[0]:
        return data[0]["generated_text"]
    elif isinstance(data, dict) and "error" in data:
        raise RuntimeError(data["error"])
    else:
        return str(data)

def extract_functions(c_code: str):
    """Find all C function signatures from source code."""
    pattern = r"\b\w+\s+\**\w+\s*\([^)]*\)\s*{"
    return re.findall(pattern, c_code)

def generate_test_for_function(function_sig: str) -> str:
    prompt = f"""
Write a C unit test for the following function.
Only output compilable C code inside a test function (using Unity or a simple assert-based test).

Function:
{function_sig}
"""
    return call_huggingface(prompt)

if __name__ == "__main__":
    c_files = []
    for root, _, files in os.walk("."):
        for f in files:
            if f.endswith(".c"):
                c_files.append(os.path.join(root, f))

    for c_file in c_files:
        with open(c_file, "r") as f:
            code = f.read()

        functions = extract_functions(code)
        for func in functions:
            test_code = generate_test_for_function(func)
            test_filename = c_file.replace(".c", "_test.c")
            with open(test_filename, "a") as tf:
                tf.write("\n\n/* Test for: {} */\n".format(func))
                tf.write(test_code)
            
            print(f"✅ Generated test for {func} → {test_filename}")
