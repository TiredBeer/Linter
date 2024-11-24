import unittest
from IdentifierLinter import IdentifierLinter


class TestIdentifierLinter(unittest.TestCase):
    def test_variable_starts_with_digit(self):
        code_lines = ["1variable = 10"]
        linter = IdentifierLinter(code_lines)
        linter.run()
        expected_errors = [
            (1,
             "Строка 1: Имя переменной '1variable' не должно начинаться с цифры или недопустимого символа.")
        ]
        self.assertEqual(linter.get_report(), expected_errors)

    def test_variable_starts_with_invalid_char(self):
        code_lines = ["$variable = 20"]
        linter = IdentifierLinter(code_lines)
        linter.run()
        expected_errors = [
            (1,
             "Строка 1: Имя переменной '$variable' не должно начинаться с цифры или недопустимого символа.")
        ]
        self.assertEqual(linter.get_report(), expected_errors)

    def test_function_starts_with_digit(self):
        code_lines = ["def 2function():", "    pass"]
        linter = IdentifierLinter(code_lines)
        linter.run()
        expected_errors = [
            (1,
             "Строка 1: Имя функции '2function' не должно начинаться с цифры или недопустимого символа.")
        ]
        self.assertEqual(linter.get_report(), expected_errors)

    def test_function_starts_with_invalid_char(self):
        code_lines = ["def @function():", "    pass"]
        linter = IdentifierLinter(code_lines)
        linter.run()
        expected_errors = [
            (1,
             "Строка 1: Имя функции '@function' не должно начинаться с цифры или недопустимого символа.")
        ]
        self.assertEqual(linter.get_report(), expected_errors)

    def test_class_starts_with_digit(self):
        code_lines = ["class 3Class:", "    pass"]
        linter = IdentifierLinter(code_lines)
        linter.run()
        expected_errors = [
            (1,
             "Строка 1: Имя класса '3Class' не должно начинаться с цифры или недопустимого символа.")
        ]
        self.assertEqual(linter.get_report(), expected_errors)

    def test_class_starts_with_invalid_char(self):
        code_lines = ["class %Class:", "    pass"]
        linter = IdentifierLinter(code_lines)
        linter.run()
        expected_errors = [
            (1,
             "Строка 1: Имя класса '%Class' не должно начинаться с цифры или недопустимого символа.")
        ]
        self.assertEqual(linter.get_report(), expected_errors)

    def test_valid_variable(self):
        code_lines = ["variable1 = 10"]
        linter = IdentifierLinter(code_lines)
        linter.run()
        expected_errors = []
        self.assertEqual(linter.get_report(), expected_errors)

    def test_valid_function(self):
        code_lines = ["def function_1():", "    pass"]
        linter = IdentifierLinter(code_lines)
        linter.run()
        expected_errors = []
        self.assertEqual(linter.get_report(), expected_errors)

    def test_valid_class(self):
        code_lines = ["class MyClass:", "    pass"]
        linter = IdentifierLinter(code_lines)
        linter.run()
        expected_errors = []
        self.assertEqual(linter.get_report(), expected_errors)

    def test_multiple_errors(self):
        code_lines = [
            "1var = 5",
            "def 2func():",
            "class 3Class:",
            "    pass",
            "valid_var = 10",
            "def valid_func():",
            "    pass",
            "class ValidClass:",
            "    pass"
        ]
        linter = IdentifierLinter(code_lines)
        linter.run()
        expected_errors = [
            (1,
             "Строка 1: Имя переменной '1var' не должно начинаться с цифры или недопустимого символа."),
            (2,
             "Строка 2: Имя функции '2func' не должно начинаться с цифры или недопустимого символа."),
            (3,
             "Строка 3: Имя класса '3Class' не должно начинаться с цифры или недопустимого символа.")
        ]
        self.assertEqual(linter.get_report(), expected_errors)

    def test_ignores_comments_and_empty_lines(self):
        code_lines = [
            "",
            "# This is a comment",
            "    # Indented comment",
            "   ",
            "\t",
            "def valid_function():",
            "    pass"
        ]
        linter = IdentifierLinter(code_lines)
        linter.run()
        expected_errors = []
        self.assertEqual(linter.get_report(), expected_errors)

    def test_assignment_in_expression(self):
        code_lines = ["result = a + b"]
        linter = IdentifierLinter(code_lines)
        linter.run()
        expected_errors = []
        self.assertEqual(linter.get_report(), expected_errors)

    def test_variable_with_spaces(self):
        code_lines = ["var iable = 10"]
        linter = IdentifierLinter(code_lines)
        linter.run()
        expected_errors = []
        self.assertEqual(linter.get_report(), expected_errors)

    def test_non_assignment_lines(self):
        code_lines = [
            "if condition:",
            "    do_something()",
            "else:",
            "    do_something_else()"
        ]
        linter = IdentifierLinter(code_lines)
        linter.run()
        expected_errors = []
        self.assertEqual(linter.get_report(), expected_errors)


if __name__ == '__main__':
    unittest.main()
