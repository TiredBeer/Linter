from baseLinter import BaseLinter


class SpaceLinter(BaseLinter):
    def __init__(self, code_lines):
        super().__init__()
        self.lines = code_lines

    def check_trailing_spaces(self):
        """
        Проверяет строки на наличие пробелов в конце.
        """
        for lineno, line in enumerate(self.lines, start=1):
            if line.endswith(" "):
                self.errors.append(
                    (lineno, "В конце строки есть лишние пробелы."))

    def check_len_lines(self):
        """
        Проверяет длину строки.
        """
        for lineno, line in enumerate(self.lines, start=1):
            if len(line) > 79:
                self.errors.append(
                    (lineno, "У меня монитор не в километр"))

    def check_extra_spaces_within_line(self):
        """
        Проверяет строки на наличие лишних пробелов между словами или символами.
        """
        for lineno, line in enumerate(self.lines, start=1):
            if "  " in line.strip():
                self.errors.append((lineno,
                                    "В строке есть лишние пробелы между словами."))

    def check_block_indentation(self):
        """
        Проверяет все строки внутри блоков на корректность отступов.
        """
        expected_indents = [
            0]  # Список ожидаемых отступов для каждого уровня вложенности
        skip_check = False  # Флаг для пропуска проверки текущей строки
        for lineno, line in enumerate(self.lines, start=1):
            stripped = line.strip()
            if not stripped:
                continue  # Пропускаем пустые строки
            leading_spaces = len(line) - len(line.lstrip(" "))
            # Проверяем, если текущий отступ соответствует ожидаемому
            if leading_spaces != expected_indents[-1]:
                if leading_spaces > expected_indents[-1]:
                    if skip_check:
                        # Ожидаем увеличение отступа на 4 пробела
                        if leading_spaces == expected_indents[-1] + 4:
                            expected_indents.append(leading_spaces)
                        else:
                            self.errors.append(
                                (lineno,
                                 f"Ожидался отступ {expected_indents[-1] + 4} пробелов, но было {leading_spaces}.")
                            )
                        skip_check = False
                    else:
                        self.errors.append(
                            (lineno,
                             f"Неожиданная срань, {leading_spaces} пробелов.")
                        )
                else:
                    # Отступ уменьшился или равен предыдущему уровню
                    while expected_indents and leading_spaces < \
                            expected_indents[-1]:
                        expected_indents.pop()
                    if leading_spaces != expected_indents[-1]:
                        self.errors.append(
                            (lineno,
                             f"Некорректный отступ: ожидалось {expected_indents[-1]} пробелов, но было {leading_spaces}.")
                        )
            else:
                # Отступ соответствует ожидаемому
                skip_check = False
            # Проверяем, заканчивается ли строка двоеточием (начало блока)
            if stripped.endswith(":"):
                skip_check = True

    def run(self):
        """
        Запускает все проверки.
        """
        self.check_len_lines()
        self.check_trailing_spaces()
        self.check_extra_spaces_within_line()
        self.check_block_indentation()


# Пример использования
if __name__ == "__main__":
    code = """a =  1
"""
    linter = SpaceLinter(code)
    linter.run()
    linter.print_report()
