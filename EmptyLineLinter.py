from baseLinter import BaseLinter


class EmptyLineLinter(BaseLinter):
    def __init__(self, code):
        super().__init__()
        self.code = code
        self.lines = self.code.split('\n')
        self.previous_structure = None  # 'class', 'function', 'method', None
        self.previous_lineno = 0
        self.in_class = False
        self.class_indent = 0
        self.first_structure = True

    def check_empty_lines(self):
        for lineno, line in enumerate(self.lines, start=1):
            stripped_line = line.strip()
            if not stripped_line:
                continue
            current_indent = len(line) - len(line.lstrip(' '))

            if stripped_line.startswith('class '):
                if self.first_structure:
                    if lineno > 1:
                        # Если перед первым классом есть код, проверяем количество пустых строк
                        self.check_blank_lines(lineno, 2, 'класс')
                    self.first_structure = False
                else:
                    # Проверяем количество пустых строк перед классом
                    self.check_blank_lines(lineno, 2, 'класс')

                self.previous_structure = 'class'
                self.previous_lineno = lineno
                self.in_class = True
                self.class_indent = current_indent

            elif stripped_line.startswith('def '):
                if self.in_class and current_indent > self.class_indent:
                    if self.previous_structure == 'method':
                        self.check_blank_lines(lineno, 1, 'метод класса')
                    self.previous_structure = 'method'
                    self.previous_lineno = lineno
                else:
                    # Это функция верхнего уровня
                    if self.first_structure:
                        if lineno > 1:
                            self.check_blank_lines(lineno, 2, 'функция')
                        self.first_structure = False
                    else:
                        self.check_blank_lines(lineno, 2, 'функция')
                    self.previous_structure = 'function'
                    self.previous_lineno = lineno
                    self.in_class = False
            else:
                # Если это не объявление класса или функции
                self.previous_lineno = lineno
                if self.first_structure:
                    self.first_structure = False
                if self.in_class and current_indent <= self.class_indent:
                    self.in_class = False

    def check_blank_lines(self, current_lineno, max_blank_lines,
                          structure_type):
        """
        Проверяет количество пустых строк перед текущей структурой.
        """
        actual_blank_lines = self.count_blank_lines(self.previous_lineno,
                                                    current_lineno)
        if actual_blank_lines < max_blank_lines:
            self.errors.append(
                (current_lineno,
                 f"Недостаточно пустых строк перед {structure_type}. Ожидалось {max_blank_lines}, найдено {actual_blank_lines}.")
            )
        # Проверка превышения количества пустых строк
        elif actual_blank_lines > max_blank_lines:
            self.errors.append(
                (current_lineno,
                 f"Слишком много пустых строк перед {structure_type}. Максимум {max_blank_lines}, найдено {actual_blank_lines}.")
            )

    def count_blank_lines(self, previous_lineno, current_lineno):
        blank_lines = 0
        for i in range(previous_lineno, current_lineno - 1):
            if not self.lines[i].strip():
                blank_lines += 1
        return blank_lines

    def run(self):
        self.check_empty_lines()


# Пример использования
if __name__ == "__main__":
    code = """class A:
    def method_a(self):
        pass
    def method_b(self):
        pass
"""
    linter = EmptyLineLinter(code)
    linter.run()
    linter.print_report()
