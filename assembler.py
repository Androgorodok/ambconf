from instructions import INSTRUCTIONS


def parse_line(line: str, line_no: int):
    parts = [p.strip() for p in line.split(",")]

    if not parts:
        raise ValueError(f"Пустая строка {line_no}")

    mnemonic = parts[0].upper()

    if mnemonic not in INSTRUCTIONS:
        raise ValueError(f"Неизвестная команда '{mnemonic}' (строка {line_no})")

    spec = INSTRUCTIONS[mnemonic]
    fields = spec["fields"]

    if len(parts) - 1 != len(fields):
        raise ValueError(
            f"{mnemonic}: ожидалось {len(fields)} аргументов, "
            f"получено {len(parts) - 1} (строка {line_no})"
        )

    values = []
    for i, part in enumerate(parts[1:], start=1):
        try:
            # Поддержка разных форматов чисел: десятичный, шестнадцатеричный
            if part.startswith("0x"):
                values.append(int(part[2:], 16))
            elif part.startswith("Фx"):  # Поддержка формата из спецификации
                values.append(int(part[2:], 16))
            else:
                values.append(int(part))
        except ValueError:
            raise ValueError(f"Неверный аргумент '{part}' (строка {line_no}, аргумент {i})")

    instr = {
        "mnemonic": mnemonic,
        "opcode": spec["opcode"],
        "A": spec["opcode"],
    }

    for name, value in zip(fields, values):
        instr[name] = value

    return instr


def assemble(text: str):
    program = []

    for i, line in enumerate(text.splitlines(), start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            program.append(parse_line(line, i))
        except ValueError as e:
            print(f"Ошибка в строке {i}: {e}")
            raise

    return program


def format_instruction_for_test(instr):
    """Форматирование инструкции для тестового вывода как в спецификации"""
    spec = INSTRUCTIONS[instr["mnemonic"]]

    result = f"{instr['mnemonic']}: "
    fields = []

    # Всегда начинаем с поля A (опкод)
    fields.append(f"A={instr['A']}")

    # Добавляем остальные поля
    for field in spec["fields"]:
        if field in instr:
            fields.append(f"{field}={instr[field]}")

    return result + ", ".join(fields)