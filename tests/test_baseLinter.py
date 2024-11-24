import unittest
from baseLinter import BaseLinter
from io import StringIO
import sys


class TestBaseLinter(unittest.TestCase):

    def test_print_report_no_errors(self):
        linter = BaseLinter()
        captured_output = StringIO()
        sys.stdout = captured_output
        linter.print_report()
        sys.stdout = sys.__stdout__
        expected_output = "Замечаний не найдено!"
        self.assertEqual(captured_output.getvalue().strip(), expected_output)

    def test_print_report_with_errors(self):
        linter = BaseLinter()
        linter.errors = [
            (1, "Ошибка 1"),
            (2, "Ошибка 2"),
            (3, "Ошибка 3")
        ]
        captured_output = StringIO()
        sys.stdout = captured_output
        linter.print_report()
        sys.stdout = sys.__stdout__
        expected_output = (
            "Замечания по коду:\n"
            "Строка 1: Ошибка 1\n"
            "Строка 2: Ошибка 2\n"
            "Строка 3: Ошибка 3"
        )
        self.assertEqual(captured_output.getvalue().strip(), expected_output)

    def test_get_report_no_errors(self):
        linter = BaseLinter()
        report = linter.get_report()
        self.assertEqual(report, [])

    def test_get_report_with_errors(self):
        linter = BaseLinter()
        linter.errors = [
            (1, "Ошибка 1"),
            (2, "Ошибка 2")
        ]
        expected_report = [
            (1, "Строка 1: Ошибка 1"),
            (2, "Строка 2: Ошибка 2")
        ]
        report = linter.get_report()
        self.assertEqual(report, expected_report)

    def test_print_report_output_format(self):
        linter = BaseLinter()
        linter.errors = [
            (42, "Нестандартная ошибка")
        ]
        captured_output = StringIO()
        sys.stdout = captured_output
        linter.print_report()
        sys.stdout = sys.__stdout__
        expected_output = (
            "Замечания по коду:\n"
            "Строка 42: Нестандартная ошибка"
        )
        self.assertEqual(captured_output.getvalue().strip(), expected_output)

    def test_print_report_order(self):
        """
        Проверяет, что метод print_report() выводит ошибки в порядке их добавления.
        """
        linter = BaseLinter()
        linter.errors = [
            (3, "Ошибка B"),
            (1, "Ошибка A"),
            (2, "Ошибка C")
        ]
        captured_output = StringIO()
        sys.stdout = captured_output
        linter.print_report()
        sys.stdout = sys.__stdout__
        expected_output = (
            "Замечания по коду:\n"
            "Строка 3: Ошибка B\n"
            "Строка 1: Ошибка A\n"
            "Строка 2: Ошибка C"
        )
        self.assertEqual(captured_output.getvalue().strip(), expected_output)


if __name__ == '__main__':
    unittest.main()
