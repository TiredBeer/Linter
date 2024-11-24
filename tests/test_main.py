import unittest
from main import Linter


class TestLinter(unittest.TestCase):
    def test_no_errors(self):
        """
        Тестирует работу Linter, когда код не содержит ошибок.
        """
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
        linter = Linter(code_lines)
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output
        linter.get_corrections()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip()
        self.assertEqual(output, "Замечаний не найдено!")

    def test_with_errors(self):
        """
        Тестирует работу Linter, когда код содержит ошибки.
        """
        code_lines = [
            "def function_one():",
            "    pass",
            "def function_two():",
            "    pass",
            "",
            "",
            "class 1MyClass:",
            "    def method_one(self):",
            "     pass",
            "",
            "",
            "def function_three():",
            "    pass"
        ]
        linter = Linter(code_lines)
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output
        linter.get_corrections()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("Замечания по коду:", output)
        self.assertIn(
            "Имя класса '1MyClass' не должно начинаться с цифры или недопустимого символа.",
            output)
        self.assertIn("Ожидался отступ", output)


if __name__ == '__main__':
    unittest.main()
