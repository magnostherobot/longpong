_bitfont_0 = [ True, True, True,
        True, False, True,
        True, False, True,
        True, False, True,
        True, True, True ]

_bitfont_1 = [ False, False, True,
        False, True, True,
        False, False, True,
        False, False, True,
        False, False, True ]

_bitfont_2 = [ True, True, True,
        False, False, True,
        True, True, True,
        True, False, False,
        True, True, True ]

_bitfont_3 = [ True, True, True,
        False, False, True,
        False, True, True,
        False, False, True,
        True, True, True ]

_bitfont_4 = [ True, False, False,
        True, False, True,
        True, True, True,
        False, False, True,
        False, False, True ]

_bitfont_5 = [ True, True, True,
        True, False, False,
        True, True, True,
        False, False, True,
        True, True, True ]

_bitfont_6 = [ True, True, True,
        True, False, False,
        True, True, True,
        True, False, True,
        True, True, True ]

_bitfont_7 = [ True, True, True,
        False, False, True,
        False, True, True,
        False, False, True,
        False, False, True ]

_bitfont_8 = [ True, True, True,
        True, False, True,
        True, True, True,
        True, False, True,
        True, True, True ]

_bitfont_9 = [ True, True, True,
        True, False, True,
        True, True, True,
        False, False, True,
        True, True, True ]

_bitfonts = [ _bitfont_0, _bitfont_1, _bitfont_2, _bitfont_3, _bitfont_4, _bitfont_5, _bitfont_6, _bitfont_7, _bitfont_8, _bitfont_9 ]

def bitfont(number):
    # Create the fonts
    # Generate the digits
    result = []
    number = add_digit(result, number)
    while number > 0:
        number = add_digit(result, number)
    # Reverse the list
    return result[::-1]

def add_digit(result, number):
    # The rightmost digit is (number - (number / 10 * 10))
    # assuming integer division
    value = int(number / 10) * 10
    result.append(_bitfonts[number - value])
    return int(number / 10)
