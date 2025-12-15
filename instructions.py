INSTRUCTIONS = {
    "LOAD_CONST": {
        "opcode": 17,
        "fields": ["B", "C"],
        "size": 4,
        "description": "Загрузка константы"
    },
    "LOAD_MEM": {
        "opcode": 16,
        "fields": ["B", "C"],
        "size": 5,
        "description": "Чтение значения из памяти"
    },
    "STORE": {
        "opcode": 20,
        "fields": ["B", "C", "D"],
        "size": 7,
        "description": "Запись значения в память"
    },
    "GE": {
        "opcode": 13,
        "fields": ["B", "C", "D"],
        "size": 7,
        "description": "Бинарная операция '>='"
    }
}