import re

def day01(inp, part2=False):
    lines = inp.strip().splitlines()

    replacements = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
    }

    if part2:
        # also match letters (replacement doesn't work due to overlapping words)
        patt_first = re.compile(fr'\d|{"|".join(replacements)}')
        # last digit: match reversed string with reversed words
        reversed_words = [word[::-1] for word in replacements]
        patt_last = re.compile(fr'\d|{"|".join(reversed_words)}')
    else:
        # only match actual digits
        patt_first = patt_last = re.compile(r'\d')

    calibration = 0
    for line in lines:
        digits = patt_first.search(line).group(), patt_last.search(line[::-1]).group()[::-1]

        if part2:
            digits = [
                str(replacements[digit]) if digit in replacements else digit
                for digit in digits
            ]

        calibration += int(''.join(digits))

    return calibration


if __name__ == "__main__":
    testinp = open('day01.testinp').read()
    testinp2 = open('day01.testinp2').read()
    print(day01(testinp), day01(testinp2, part2=True))
    inp = open('day01.inp').read()
    print(day01(inp), day01(inp, part2=True))
