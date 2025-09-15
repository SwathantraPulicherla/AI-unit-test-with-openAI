import re

SRC_FILE = "calculator.c"
TEST_FILE = "test_calculator.c"

def extract_function_names_from_source(filename):
    with open(filename, "r") as f:
        code = f.read()
    # Matches: return_type func_name(args) {
    pattern = re.compile(r'^\s*\w[\w\s\*]*\s+(\w+)\s*\([^)]*\)\s*\{', re.MULTILINE)
    return set(pattern.findall(code))

def extract_tested_functions_from_testfile(filename):
    try:
        with open(filename, "r") as f:
            code = f.read()
    except FileNotFoundError:
        return set()
    # Find all TEST_CASE(test_funcname) and void test_funcname(void)
    pattern = re.compile(r'TEST_CASE\s*\(\s*test_(\w+)', re.MULTILINE)
    test_funcs = pattern.findall(code)
    return set(test_funcs)

def insert_stubs_above_main(test_file, stubs):
    with open(test_file, "r") as f:
        lines = f.readlines()

    # Find the line number where main starts
    main_idx = None
    for idx, line in enumerate(lines):
        if re.match(r'\s*int\s+main\s*\(', line):
            main_idx = idx
            break

    if main_idx is None:
        # If main is not found, append at the end
        main_idx = len(lines)

    # Insert stubs above main
    new_lines = lines[:main_idx] + stubs + ["\n"] + lines[main_idx:]
    with open(test_file, "w") as f:
        f.writelines(new_lines)

def make_stub(funcname):
    return f"""void test_{funcname}(void) {{
    // TODO: Implement test for {funcname}
}}

"""

if __name__ == "__main__":
    src_funcs = extract_function_names_from_source(SRC_FILE)
    tested_funcs = extract_tested_functions_from_testfile(TEST_FILE)
    missing = [func for func in src_funcs if func not in tested_funcs]

    if not missing:
        print("All functions already have test stubs.")
    else:
        stubs = [make_stub(func) for func in missing]
        insert_stubs_above_main(TEST_FILE, stubs)
        for func in missing:
            print(f"Added test stub for: {func}")