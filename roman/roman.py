MIN_INT: int = 1
MAX_INT: int = 3_999
CHARS: dict[int, str] = {
    1_000: 'M',
    500: 'D',
    100: 'C',
    50: 'L',
    10: 'X',
    5: 'V',
    1: 'I',
}


def to_roman(number: int) -> str:
    """ Convert an integer to a Roman numeral. """
    if number < MIN_INT:
        raise ValueError(f'Number less that minimum permissible ({MIN_INT})')

    if number > MAX_INT:
        raise ValueError(f'Number greater than maximum permissible ({MAX_INT})')

    roman_num: str = ''

    for integer, string in CHARS.items():
        while number >= integer:
            roman_num += string
            number -= integer

    roman_num = (
        roman_num.replace('VIIII', 'IX')  # 9
                 .replace('IIII', 'IV')   # 4
                 .replace('LXXXX', 'XC')  # 90
                 .replace('XXXX', 'XL')   # 40
                 .replace('DCCCC', 'CM')  # 900
                 .replace('CCCC', 'CD')   # 400
    )

    return roman_num


def from_roman(roman_num: str) -> int:
    """ Convert a Roman numeral to an integer. """
    if not roman_num:
        raise ValueError('Provide a roman numeral string')

    invalid_chars: list[str] = [c for c in roman_num if c not in CHARS.values()]

    if invalid_chars:
        raise ValueError(f'Invalid character(s): {",".join(invalid_chars)}')

    # Reverse the keys and values for fast lookups
    char_values: dict = {v: k for k, v in CHARS.items()}

    roman_len: int = len(roman_num)
    integer: int = 0

    for ix, char in enumerate(roman_num):
        char_val: int = char_values[char]

        # If we are at the last character OR the value of the
        # current character is greater or equal to the value
        # of the next character, we don't need subtraction
        if ix + 1 == roman_len or char_val >= char_values[roman_num[ix + 1]]:
            integer += char_val
        else:
            integer -= char_val

    return integer


if __name__ == '__main__':
    tests: dict[int, str] = {
        3_999: 'MMMCMXCIX',
        1_776: 'MDCCLXXVI',
        1_918: 'MCMXVIII',
        1_944: 'MCMXLIV',
        2_023: 'MMXXIII',
    }

    for integer, roman in tests.items():
        assert to_roman(integer) == roman, AssertionError(f'{integer}: {to_roman(integer)} != {roman}')
        assert from_roman(roman) == integer, AssertionError(f'{roman}: {from_roman(roman)} != {integer}')
