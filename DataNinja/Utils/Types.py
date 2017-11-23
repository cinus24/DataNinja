import re


def represents_int(s):
    regex = "^[0-9]+$"
    regex_test = re.compile(regex)
    if regex_test.match(s):
        return True
    return False


def represents_float(s):
    regex = "[-+]?[0-9]*\.?[0-9]+"
    regex_test = re.compile(regex)
    if regex_test.match(s):
        return True
    return False
