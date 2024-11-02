def fix_trailing_whitespace(line):
    return line.rstrip()

def fix_code(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    fixed_lines = []
    for line in lines:
        line = fix_trailing_whitespace(line)
        fixed_lines.append(line)
    return "\n".join(fixed_lines)


if __name__ == "__main__":
    filename = "example.txt"
    fixed_code = fix_code(filename)
    print(fixed_code)
