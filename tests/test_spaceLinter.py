import unittest
from SpaceLinter import SpaceLinter


class TestSpaceLinter(unittest.TestCase):
    def test_trailing_spaces(self):
        code_lines = [
            "print('Hello, World!')  ",
            "a = 1",
            "b = 2  ",
            "c = 3"
        ]
        linter = SpaceLinter(code_lines)
        linter.run()
        expected_errors = [(1, 'Строка 1: В конце строки есть лишние пробелы.'),
                           (3, 'Строка 3: В конце строки есть лишние пробелы.')]
        self.assertEqual(linter.get_report(), expected_errors)

    def test_line_length(self):
        code_lines = [
            "a = 'This is a short line.'",
            "b = 'This line is exactly seventy-nine characters long. " +
            "It should not cause an error.'",
            "c = 'This line is eighty characters long. It should cause an error " +
            "because it is too long.'"
        ]
        linter = SpaceLinter(code_lines)
        linter.run()
        expected_errors = [
            (2, 'Строка 2: У меня монитор не в километр'),
            (3, "Строка 3: У меня монитор не в километр")
        ]
        self.assertEqual(linter.get_report(), expected_errors)

    def test_extra_spaces_within_line(self):
        code_lines = [
            "a  = 1",
            "if  a == 1:",
            "    print('a is one')",
            "b =  2",
            "print(  'Hello'  )"
        ]
        linter = SpaceLinter(code_lines)
        linter.run()
        expected_errors = [
            (1, "Строка 1: В строке есть лишние пробелы между словами."),
            (2, "Строка 2: В строке есть лишние пробелы между словами."),
            (4, "Строка 4: В строке есть лишние пробелы между словами."),
            (5, "Строка 5: В строке есть лишние пробелы между словами.")
        ]
        self.assertEqual(linter.get_report(), expected_errors)

    def test_block_indentation_correct(self):
        code_lines = [
            "def function():",
            "    if True:",
            "        print('Correct Indentation')",
            "    else:",
            "        print('Still Correct')",
            "    print('Back to function level')",
            "print('Top level')"
        ]
        linter = SpaceLinter(code_lines)
        linter.run()
        expected_errors = []
        self.assertEqual(linter.get_report(), expected_errors)

    def test_block_indentation_incorrect(self):
        code_lines = [
            "def function():",
            "    if True:",
            "      print('Incorrect Indentation')",  # Incorrect indentation
            "    else:",
            "        print('Correct')",
            "  print('Incorrect function level indentation')",  # Incorrect
            "print('Top level')"
        ]
        linter = SpaceLinter(code_lines)
        linter.run()
        expected_errors = [
            (3, "Строка 3: Ожидался отступ 8 пробелов, но было 6."),
            (6,
             "Строка 6: Некорректный отступ: ожидалось 0 пробелов, но было 2.")
        ]
        self.assertEqual(linter.get_report(), expected_errors)

    def test_multiple_issues(self):
        code_lines = [
            "def function():  ",
            "    a  = 1"
            "    if a == 1:",
            "        print('Value is one')",
            "    return a  ",  # Trailing space
            "b = function()    ",  # Trailing space
            "print('Result:', b)"
        ]
        linter = SpaceLinter(code_lines)
        linter.run()
        expected_errors = [(1, 'Строка 1: В конце строки есть лишние пробелы.'),
                           (4, 'Строка 4: В конце строки есть лишние пробелы.'),
                           (5, 'Строка 5: В конце строки есть лишние пробелы.'),
                           (2,
                            'Строка 2: В строке есть лишние пробелы между словами.')]
        self.assertEqual(linter.get_report(), expected_errors)

    def test_no_issues(self):
        code_lines = [
            "def function():",
            "    a = 1",
            "    if a == 1:",
            "        print('No issues here')",
            "    return a",
            "b = function()",
            "print('Result:', b)"
        ]
        linter = SpaceLinter(code_lines)
        linter.run()
        expected_errors = []
        self.assertEqual(linter.get_report(), expected_errors)

    def test_long_line_with_trailing_space_and_extra_spaces(self):
        code_lines = [
            "a = 'This is a very long line that definitely exceeds seventy-nine characters in length.'  ",
            "b  = 2"
        ]
        linter = SpaceLinter(code_lines)
        linter.run()
        expected_errors = [
            (1, "Строка 1: У меня монитор не в километр"),
            (1, "Строка 1: В конце строки есть лишние пробелы."),
            (2, "Строка 2: В строке есть лишние пробелы между словами.")
        ]
        self.assertEqual(linter.get_report(), expected_errors)

    def test_incorrect_indentation_with_colon(self):
        code_lines = [
            "if True:",
            "  print('Incorrect Indentation')",  # Incorrect indentation
            "else:",
            "    print('Correct Indentation')"
        ]
        linter = SpaceLinter(code_lines)
        linter.run()
        expected_errors = [
            (2, 'Строка 2: Ожидался отступ 4 пробелов, но было 2.')
        ]
        self.assertEqual(linter.get_report(), expected_errors)

    def test_empty_lines(self):
        code_lines = [
            "",
            "    ",
            "def function():",
            "    pass  ",
            ""
        ]
        linter = SpaceLinter(code_lines)
        linter.run()
        expected_errors = [
            (2, "Строка 2: В конце строки есть лишние пробелы."),
            (4, 'Строка 4: В конце строки есть лишние пробелы.')
        ]
        self.assertEqual(linter.get_report(), expected_errors)

    def test_tabs_instead_of_spaces(self):
        code_lines = [
            "def function():",
            "\tprint('Using tabs')",  # Tab character
            "    print('Using spaces')",
            "if True:",
            "\t\tprint('Nested with tabs')"
        ]
        linter = SpaceLinter(code_lines)
        linter.run()
        expected_errors = [(3, 'Строка 3: Неожиданная срань, 4 пробелов.')]
        self.assertEqual(linter.get_report(), expected_errors)

    def test_mixed_indentation_levels(self):
        code_lines = [
            "def function():",
            "    if True:",
            "        if False:",
            "          print('Incorrect Indentation')",  # Incorrect indentation
            "        else:",
            "            print('Correct')",
            "    print('Back to function level')",
            "print('Top level')"
        ]
        linter = SpaceLinter(code_lines)
        linter.run()
        expected_errors = [
            (4, "Строка 4: Ожидался отступ 12 пробелов, но было 10.")
        ]
        self.assertEqual(linter.get_report(), expected_errors)

    def test_no_errors_in_empty_file(self):
        code_lines = []
        linter = SpaceLinter(code_lines)
        linter.run()
        expected_errors = []
        self.assertEqual(linter.get_report(), expected_errors)


if __name__ == '__main__':
    unittest.main()
