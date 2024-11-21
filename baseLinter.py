class BaseLinter:
    def __init__(self):
        self.errors = []

    def print_report(self):
        if not self.errors:
            print("Замечаний не найдено!")
        else:
            print("Замечания по коду:")
            for lineno, message in self.errors:
                print(f"Строка {lineno}: {message}")

    def get_report(self):
        message_errors = []
        for lineno, message in self.errors:
            message_errors.append((lineno, f"Строка {lineno}: {message}"))
        return message_errors
