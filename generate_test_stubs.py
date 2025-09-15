import re

SRC_FILE = "calculator.c"
TEST_FILE = "test_calculator.c"

def extract_function_signatures(filename):
    with open(filename, "r") as f:
        code = f.read()
    # Matches: return_type func_name(args) {
    pattern = re.compile(r'^\s*([a-zA-Z_][\w\s\*\[\]]*)\s+(\w+)\s*\(([^)]*)\)\s*\{', re.MULTILINE)
    return {name: (ret_type.strip(), args.strip()) for ret_type, name, args in pattern.findall(code)}

def extract_tested_functions(filename):
    try:
        with open(filename, "r") as f:
            code = f.read()
    except FileNotFoundError:
        return set()
    # Matches: void test_funcname(void)
    pattern = re.compile(r'void\s+test_(\w+)\s*\(\s*void\s*\)', re.MULTILINE)
    return set(pattern.findall(code))

def append_test_stub(filename, funcname, signature):
    ret_type, args = signature
    stub = f"""
void test_{funcname}(void) {{
    // TODO: Implement test for {funcname}
    // Function signature: {ret_type} {funcname}({args})
}}
"""
    # Insert above main if possible
    with open(filename, "r") as f:
        lines = f.readlines()
    main_idx = next((i for i, line in enumerate(lines) if re.match(r'\s*int\s+main\s*\(', line)), len(lines))
    new_lines = lines[:main_idx] + [stub] + lines[main_idx:]
    with open(filename, "w") as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    src_funcs = extract_function_signatures(SRC_FILE)
    tested_funcs = extract_tested_functions(TEST_FILE)
    missing = [f for f in src_funcs if f not in tested_funcs]

    if not missing:
        print("All functions already have test stubs.")
    else:
        for func in missing:
            append_test_stub(TEST_FILE, func, src_funcs[func])
            print(f"Added test stub for: {func}")