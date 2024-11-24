import unittest
from EmptyLineLinter import EmptyLineLinter


class TestEmptyLineLinter(unittest.TestCase):
    def test_no_empty_lines_before_class(self):
        code_lines = [
            "def some_function():",
            "    pass",
            "class MyClass:",
            "    pass"
        ]
        linter = EmptyLineLinter(code_lines)
        linter.run()
        expected_errors = [
            (3,
             "Строка 3: Недостаточно пустых строк перед классом. Ожидалось 2, найдено 0.")
        ]
        self.assertEqual(linter.get_report(), expected_errors)

    def test_correct_empty_lines_before_class(self):
        code_lines = [
            "def some_function():",
            "    pass",
            "",
            "",
            "class MyClass:",
            "    pass"
        ]
        linter = EmptyLineLinter(code_lines)
        linter.run()
        expected_errors = []
        self.assertEqual(linter.get_report(), expected_errors)

    def test_too_many_empty_lines_before_class(self):
        code_lines = [
            "def some_function():",
            "    pass",
            "",
            "",
            "",
            "class MyClass:",
            "    pass"
        ]
        linter = EmptyLineLinter(code_lines)
        linter.run()
        expected_errors = [
            (6,
             "Строка 6: Слишком много пустых строк перед классом. Максимум 2, найдено 3.")
        ]
        self.assertEqual(linter.get_report(), expected_errors)

    def test_no_empty_lines_before_function(self):
        code_lines = [
            "def function_one():",
            "    pass",
            "def function_two():",
            "    pass"
        ]
        linter = EmptyLineLinter(code_lines)
        linter.run()
        expected_errors = [
            (3,
             "Строка 3: Недостаточно пустых строк перед функцией. Ожидалось 2, найдено 0.")
        ]
        self.assertEqual(linter.get_report(), expected_errors)

    def test_correct_empty_lines_before_function(self):
        code_lines = [
            "def function_one():",
            "    pass",
            "",
            "",
            "def function_two():",
            "    pass"
        ]
        linter = EmptyLineLinter(code_lines)
        linter.run()
        expected_errors = []
        self.assertEqual(linter.get_report(), expected_errors)

    def test_too_many_empty_lines_before_function(self):
        code_lines = [
            "def function_one():",
            "    pass",
            "",
            "",
            "",
            "def function_two():",
            "    pass"
        ]
        linter = EmptyLineLinter(code_lines)
        linter.run()
        expected_errors = [
            (6,
             "Строка 6: Слишком много пустых строк перед функцией. Максимум 2, найдено 3.")
        ]
        self.assertEqual(linter.get_report(), expected_errors)

    def test_no_empty_line_before_method(self):
        code_lines = [
            "class MyClass:",
            "    def method_one(self):",
            "        pass",
            "    def method_two(self):",
            "        pass"
        ]
        linter = EmptyLineLinter(code_lines)
        linter.run()
        expected_errors = [
            (4,
             "Строка 4: Недостаточно пустых строк перед методом класса. Ожидалось 1, найдено 0.")
        ]
        self.assertEqual(linter.get_report(), expected_errors)

    def test_correct_empty_line_before_method(self):
        code_lines = [
            "class MyClass:",
            "    def method_one(self):",
            "        pass",
            "",
            "    def method_two(self):",
            "        pass"
        ]
        linter = EmptyLineLinter(code_lines)
        linter.run()
        expected_errors = []
        self.assertEqual(linter.get_report(), expected_errors)

    def test_too_many_empty_lines_before_method(self):
        code_lines = [
            "class MyClass:",
            "    def method_one(self):",
            "        pass",
            "",
            "",
            "    def method_two(self):",
            "        pass"
        ]
        linter = EmptyLineLinter(code_lines)
        linter.run()
        expected_errors = [
            (6,
             "Строка 6: Слишком много пустых строк перед методом класса. Максимум 1, найдено 2.")
        ]
        self.assertEqual(linter.get_report(), expected_errors)

    def test_mixed_structures(self):
        code_lines = [
            "def function_one():",
            "    pass",
            "",
            "",
            "class MyClass:",
            "    def method_one(self):",
            "        pass",
            "",
            "    def method_two(self):",
            "        pass",
            "",
            "",
            "def function_two():",
            "    pass"
        ]
        linter = EmptyLineLinter(code_lines)
        linter.run()
        self.assertEqual(linter.get_report(), [])

    def test_code_before_first_structure(self):
        code_lines = [
            "import os",
            "",
            "",
            "def function_one():",
            "    pass"
        ]
        linter = EmptyLineLinter(code_lines)
        linter.run()
        # Ожидается отсутствие ошибок, так как перед первой функцией есть 2 пустые строки
        expected_errors = []
        self.assertEqual(linter.get_report(), expected_errors)

    def test_no_errors_in_well_formatted_code(self):
        code_lines = [
            "",
            "",
            "def function_one():",
            "    pass",
            "",
            "",
            "class MyClass:",
            "    def method_one(self):",
            "        pass",
            "",
            "    def method_two(self):",
            "        pass",
            "",
            "",
            "def function_two():",
            "    pass"
        ]
        linter = EmptyLineLinter(code_lines)
        linter.run()
        expected_errors = []
        self.assertEqual(linter.get_report(), expected_errors)

    def test_incorrect_indentation(self):
        code_lines = [
            "def function_one():",
            "    pass",
            "",
            "",
            "def function_two():",
            "    pass",
            "   ",
            "class MyClass:",
            "     def method_one(self):",
            "         pass",
            "",
            "      def method_two(self):",
            "          pass"
        ]
        linter = EmptyLineLinter(code_lines)
        linter.run()
        # Линтер не проверяет отступы, поэтому ожидается только ошибка по пустым строкам
        expected_errors = [
            (8,
             "Строка 8: Недостаточно пустых строк перед классом. Ожидалось 2, найдено 1.")
        ]
        self.assertEqual(linter.get_report(), expected_errors)

    def test_code_with_comments_and_empty_lines(self):
        code_lines = [
            "",
            "",
            "def function_one():",
            "    pass",
            "",
            "",
            "def function_two():",
            "    pass",
            "",
            "",
            "class MyClass:",
            "    def method_one(self):",
            "        pass",
            "",
            "    def method_two(self):",
            "        pass"
        ]
        linter = EmptyLineLinter(code_lines)
        linter.run()
        expected_errors = []
        self.assertEqual(linter.get_report(), expected_errors)


if __name__ == '__main__':
    unittest.main()
