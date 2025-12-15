import argparse
import sys
from assembler import assemble, format_instruction_for_test


def main():
    parser = argparse.ArgumentParser(description="UVM Assembler (Stage 1)")
    parser.add_argument("source", help="CSV файл с программой")
    parser.add_argument("-o", "--output", help="Файл результата (не используется на этапе 1)")
    parser.add_argument("--test", action="store_true", help="Режим тестирования")
    parser.add_argument("--format", choices=["json", "test"], default="test",
                        help="Формат вывода в тестовом режиме")

    args = parser.parse_args()

    try:
        with open(args.source, encoding="utf-8") as f:
            text = f.read()

        program = assemble(text)

        if args.test:
            print(f"Промежуточное представление ({len(program)} инструкций):")
            print("-" * 50)

            if args.format == "test":
                # Формат как в тестах спецификации
                for i, instr in enumerate(program, 1):
                    print(f"Инструкция {i}: {format_instruction_for_test(instr)}")
            else:
                # JSON формат
                import json
                print(json.dumps(program, indent=2, ensure_ascii=False))

        else:
            # В обычном режиме просто показываем статистику
            print(f"Программа успешно ассемблирована: {len(program)} инструкций")

    except FileNotFoundError:
        print(f"Ошибка: файл '{args.source}' не найден", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка ассемблирования: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()