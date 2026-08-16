# file: calc.py
def double(n):
    return n * 2

def is_even(num):
    return num % 2 == 0

def safe_divide(a, b):
    try:
        return a/b
    except ZeroDivisionError:
        return ("Trying to divide by zero, are we?")