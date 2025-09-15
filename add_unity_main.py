import re

TEST_FILE = "test_calculator.c"

def add_unity_main(filename):
    with open(filename, "r") as f:
        code = f.read()

    # Find all test function names: void test_funcname(void)
    test_funcs = re.findall(r'void\s+(test_\w+)\s*\(\s*void\s*\)', code)

    # Create main function with RUN_TEST for each test
    main_lines = [
        "int main(void) {",
        "    UNITY_BEGIN();"
    ]
    for func in test_funcs:
        main_lines.append(f"    RUN_TEST({func});")
    main_lines.append("    return UNITY_END();")
    main_lines.append("}")

    main_code = "\n".join(main_lines)

    # Remove any existing main function
    code = re.sub(r'int\s+main\s*\([^)]*\)\s*\{[^}]*\}', '', code, flags=re.DOTALL)

    # Append the new main function at the end
    if not code.endswith('\n'):
        code += '\n'
    code += '\n' + main_code + '\n'

    with open(filename, "w") as f:
        f.write(code)

    print(f"Added/updated Unity main function with RUN_TEST for: {', '.join(test_funcs)}")

if __name__ == "__main__":
    add_unity_main(TEST_FILE)