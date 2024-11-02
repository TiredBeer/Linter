
def fix_trailing_whitespace(line):
    return line.rstrip()


def fix_indentation(line):
    leading_spaces = len(line) - len(line.lstrip())
    corrected_indent = ' ' * ((leading_spaces + 3) // 4 * 4)
    return corrected_indent + line.lstrip()


def fix_code(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()
    fixed_lines = []
    for line in lines:
        line = fix_trailing_whitespace(line)
        line = fix_indentation(line)
        fixed_lines.append(line)
    return "\n".join(fixed_lines)





if __name__ == "__main__":
    filename = "example.txt"
    fixed_code = fix_code(filename)
    print(fixed_code)
