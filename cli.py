import argparse
import sys
from assembler import assemble, format_program_for_test


def main():
    parser = argparse.ArgumentParser(
        description="Ассемблер Учебной Виртуальной Машины (УВМ) - Этап 1"
    )
    parser.add_argument(
        "source",
        help="Путь к исходному файлу с текстом программы"
    )
    parser.add_argument(
        "output",
        nargs='?',
        help="Путь к двоичному файлу-результату (опционально для этапа 1)"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Режим тестирования"
    )

    args = parser.parse_args()

    try:
        with open(args.source, 'r', encoding='utf-8') as f:
            source_code = f.read()

        program = assemble(source_code)

        if program is None:
            print("Ошибка ассемблирования!", file=sys.stderr)
            sys.exit(1)

        if args.test:
            print("=" * 60)
            print("РЕЖИМ ТЕСТИРОВАНИЯ")
            print("Промежуточное представление ассемблированной программы:")
            print("=" * 60)
            print()

            formatted = format_program_for_test(program)
            if formatted:
                print(formatted)
            else:
                print("Программа пуста")

            print()
            print("=" * 60)
            print(f"Всего инструкций: {len(program)}")
            print("=" * 60)

            # Вывод примеров из спецификации
            print("\n" + "=" * 60)
            print("ПРИМЕРЫ ИЗ СПЕЦИФИКАЦИИ:")
            print("=" * 60)
            print("\n1. LOAD_CONST (A=17, B=104, C=564):")
            print("   LOAD_CONST, 104, 564")
            print("\n2. LOAD_MEM (A=16, B=350, C=145):")
            print("   LOAD_MEM, 350, 145")
            print("\n3. STORE (A=20, B=38, C=973, D=133):")
            print("   STORE, 38, 973, 133")
            print("\n4. GE (A=13, B=389, C=744, D=174):")
            print("   GE, 389, 744, 174")

        else:
            print(f"Программа успешно ассемблирована!")
            print(f"Количество инструкций: {len(program)}")

            if args.output:
                print(f"Бинарный файл будет сохранен как: {args.output}")
                # Здесь будет код для сохранения бинарного файла на этапе 2

    except FileNotFoundError:
        print(f"Ошибка: файл '{args.source}' не найден", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()