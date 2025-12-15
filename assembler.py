from instructions import INSTRUCTIONS


def parse_line(line: str, line_no: int):
    """Парсит одну строку ассемблерного кода"""
    line = line.strip()

    if not line or line.startswith('#'):
        return None

    parts = [part.strip() for part in line.split(',')]

    if not parts:
        return None

    mnemonic = parts[0].strip().upper()

    if mnemonic not in INSTRUCTIONS:
        raise ValueError(f"Неизвестная команда '{mnemonic}' в строке {line_no}")

    spec = INSTRUCTIONS[mnemonic]

    if len(parts) - 1 != len(spec['fields']):
        raise ValueError(f"Команда '{mnemonic}' требует {len(spec['fields'])} аргументов")

    args = []
    for arg in parts[1:]:
        arg = arg.strip()
        try:
            if arg.startswith('0x'):
                args.append(int(arg[2:], 16))
            elif arg.startswith('Фx'):
                args.append(int(arg[2:], 16))
            else:
                args.append(int(arg))
        except ValueError:
            raise ValueError(f"Неверный аргумент: {arg}")

    instruction = {'mnemonic': mnemonic}

    # Добавляем поле A (опкод)
    instruction['A'] = spec['opcode']

    # Добавляем остальные поля
    for field, value in zip(spec['fields'], args):
        instruction[field] = value

    return instruction


def assemble(text: str):
    """Ассемблирует текст программы"""
    program = []

    for i, line in enumerate(text.split('\n'), 1):
        try:
            instr = parse_line(line, i)
            if instr is not None:
                program.append(instr)
        except ValueError as e:
            print(f"Ошибка в строке {i}: {e}")
            return None

    return program


def format_program_for_test(program):
    """Форматирует программу для вывода как в тестах спецификации"""
    if not program:
        return ""

    output = []
    for i, instr in enumerate(program, 1):
        fields = [f"A={instr['A']}"]

        # Добавляем поля в порядке B, C, D
        for field in ['B', 'C', 'D']:
            if field in instr:
                fields.append(f"{field}={instr[field]}")

        output.append(f"Инструкция {i}: {', '.join(fields)}")

    return '\n'.join(output)