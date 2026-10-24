import re

def validate_display_id(display_id:str) -> bool:
    "Valida se um ID da entidade Obras no formato de display tem o formato correto."
    return re.fullmatch(r'O-(?:(?!0000)[0-9]{4}|[1-9][0-9]{4,})', display_id) != None

def convert_numeric_to_display_id(id:int) -> str:
    "Converte um id puramente numérico a um ID de display para a entidade Obras. E.g. 23 > 'O-0023'"
    if not isinstance(id, int):
        raise ValueError("Erro ao converter ID: por favor, use um inteiro.")
    if id < 0:
        raise ValueError("Erro ao converter ID: Número negativo.")
    padding_zeroes = max(4 - len(str(id)), 0)
    return 'O-' + padding_zeroes*'0' + str(id)

def convert_display_to_numeric_id(display_id:str) -> int:
    "Converte um id de display em um id numérico para a entidade Obras. E.g. 'O-0023' > 23"
    is_valid_id = validate_display_id(display_id)
    if not is_valid_id:
        raise ValueError("Erro ao converter ID: ID inválido.")
    return int(display_id[2:])

def test_util_functions():
    print('Testando o validador de ID de display')
    print(f'{validate_display_id("O-0001")} - esperado True')
    print(f'{validate_display_id("O-001")} - esperado False')
    print(f'{validate_display_id("O-99229")} - esperado True')

    print('#'*50)
    print('Testando o conversor numérico > display')
    id1, id2, id3, id4 = 0, 20, 2983, 928823
    print(f'{convert_numeric_to_display_id(id1)} - esperado O-0000')
    print(f'{convert_numeric_to_display_id(id2)} - esperado O-0020')
    print(f'{convert_numeric_to_display_id(id3)} - esperado O-2983')
    print(f'{convert_numeric_to_display_id(id4)} - esperado O-928823')

    print('#'*50)
    print('Testando o conversor display > numérico')
    id1, id2, id3, id4 = 'O-0020', 'O-0101', 'O-0293', 'O-283732'
    print(f'{convert_display_to_numeric_id(id1)} - esperado 20')
    print(f'{convert_display_to_numeric_id(id2)} - esperado 101')
    print(f'{convert_display_to_numeric_id(id3)} - esperado 293')
    print(f'{convert_display_to_numeric_id(id4)} - esperado 283732')

if __name__ == "__main__":
    test_util_functions()