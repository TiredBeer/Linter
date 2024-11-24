import re
from baseLinter import BaseLinter


class IdentifierLinter(BaseLinter):
    def __init__(self, code_lines):
        super().__init__()
        self.lines = code_lines
        self.invalid_start_chars = r'[^a-zA-Z_]'  # Разрешены только буквы и подчёркивание в начале имени

    def check_identifiers(self):
        """
        Проверяет, что идентификаторы (переменные, функции, классы) не начинаются с недопустимых символов.
        """
        for lineno, line in enumerate(self.lines, start=1):
            stripped_line = line.strip()
            if not stripped_line or stripped_line.startswith('#'):
                continue

            if stripped_line.startswith('class '):
                match = re.match(r'class\s+([^\s:]+)', stripped_line)
                if match:
                    class_name = match.group(1)
                    if re.match(self.invalid_start_chars, class_name):
                        self.errors.append(
                            (lineno,
                             f"Имя класса '{class_name}' не должно начинаться с цифры или недопустимого символа.")
                        )
                continue

            if stripped_line.startswith('def '):
                match = re.match(r'def\s+([^\s(]+)', stripped_line)
                if match:
                    func_name = match.group(1)
                    if re.match(self.invalid_start_chars, func_name):
                        self.errors.append(
                            (lineno,
                             f"Имя функции '{func_name}' не должно начинаться с цифры или недопустимого символа.")
                        )
                continue

            match = re.match(r'([^\s=]+)\s*=', stripped_line)
            if match:
                var_name = match.group(1)
                if re.match(self.invalid_start_chars, var_name):
                    self.errors.append(
                        (lineno,
                         f"Имя переменной '{var_name}' не должно начинаться с цифры или недопустимого символа.")
                    )

    def run(self):
        self.check_identifiers()


# Пример использования
if __name__ == "__main__":
    code = """
class InvalidClass:
    1a22 =2
    pass

class ValidClass:
    pass

def invalid_function():
    pass

def valid_function():
    pass

nvalid_variable = 10
_valid_variable = 20
"""
    linter = IdentifierLinter(code)
    linter.run()
    linter.print_report()
