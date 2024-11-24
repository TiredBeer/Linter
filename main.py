import argparse
from SpaceLinter import SpaceLinter
from EmptyLineLinter import EmptyLineLinter
from IdentifierLinter import IdentifierLinter


class Linter:
    def __init__(self, code):
        self.code = code
        self.sub_linters = [
            SpaceLinter(code),
            EmptyLineLinter(code),
            IdentifierLinter(code)]

    def run(self):
        for sub_linter in self.sub_linters:
            sub_linter.run()

    def get_corrections(self):
        self.run()
        all_corrections = []
        for linter in self.sub_linters:
            all_corrections += linter.get_report()
        all_corrections = sorted(all_corrections, key=lambda x: x[0])
        if len(all_corrections) == 0:
            print("Замечаний не найдено!")
        else:
            print("Замечания по коду:")
            for typle in all_corrections:
                print(typle[1])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Linter для анализа кода.")
    parser.add_argument(
        'file',
        type=str,
        help="Путь к файлу, который нужно проанализировать."
    )
    args = parser.parse_args()
    file_path = args.file
    try:
        with open(file_path, 'r') as f:
            code = [i for i in f.readlines()]
            linter = Linter(code)
            linter.get_corrections()
    except FileNotFoundError:
        print(f"Ошибка: Файл '{file_path}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

