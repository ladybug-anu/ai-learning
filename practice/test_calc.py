
# file: test_calc.py
from practice.calc import *

def test_double_positive():
    assert double(5) == 10

def test_double_zero():
    assert double(0) == 0

def test_is_even_zero():
    assert is_even(0) == True

def test_is_even_odd():
    assert is_even(9) == False


def test_is_even_even():
    assert is_even(24) == True

def test_is_even_negative():
    assert is_even(-1) == False

def test_safe_divide():
    assert safe_divide(10,0) == "Trying to divide by zero, are we?"