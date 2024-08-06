import pytest
from calculator import Calculator

@pytest.fixture
def calculator():
    return Calculator()

def test_add_numbers_returns_sum(calculator):
    result = calculator.add(20, 60)
    assert result == 20 + 60

    result = calculator.add(20.56, 60.89)
    assert result == 20.56 + 60.89

def test_add_non_numbers_raises_type_error(calculator):
    with pytest.raises(TypeError):
        calculator.add("Hello", "World")
    with pytest.raises(TypeError):
        calculator.add(20, "World")
    with pytest.raises(TypeError):
        calculator.add("Hello", 23)
    with pytest.raises(TypeError):
        calculator.add("60.10.20.3", "World")

def test_add_string_numbers_returns_sum(calculator):
    result = calculator.add("50", "60.7")
    assert result == 50 + 60.7

    result = calculator.add("50", 60.7)
    assert result == 50 + 60.7

    result = calculator.add(50, "60.7")
    assert result == 50 + 60.7