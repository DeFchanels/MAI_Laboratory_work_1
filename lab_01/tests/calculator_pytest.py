import sys

import pytest

from toolkit import calculator
from toolkit.__main__ import main


def test_cli_1(capsys, monkeypatch):
    cli_args = ["toolkit", "calc", "2 + 1 * (5 - 2)"] # Имитируем ввод в терминале: python -m toolkit calc "2 + 1 * (5 - 2)"
    monkeypatch.setattr(sys, "argv", cli_args)
    main()
    captured = capsys.readouterr() # Считываем вывод
    assert captured.out.strip() == '5'


def test_cli_2(capsys, monkeypatch):
   cli_args = ["toolkit", "calc", "() + 1"]  # Имитируем ввод в терминале: python -m toolkit calc "() + 1"
   monkeypatch.setattr(sys, "argv", cli_args)
   with pytest.raises(SystemExit) as exit_info:
      main()
   captured = capsys.readouterr()  # Считываем вывод
   assert exit_info.value.code == 2
   assert captured.err.strip() == "Empty brackets error"


def test_negative_on_negative():
   res = calculator.main('-2 * -3')
   assert res == '6'

def test_default_priority():
   res = calculator.main('2 + 2 * 22')
   assert res == '46'

def test_difficult_expression():
   res = calculator.main('-2-1+(1*--(3+2)*-2)')
   assert res == '-13'

def test_many_spaces():
   res = calculator.main('2        +    2*22')
   assert res == '46'


def test_modulo():
   res = calculator.main('22 % 3')
   assert res == '1'


def test_no_spaces():
   res = calculator.main('2+2*22')
   assert res == '46'


def test_single_brackets():
   res = calculator.main('(7 - 5) * (5 + 1)')
   assert res == '12'


def test_bracket_in_bracket():
   res = calculator.main('((5 // 2) + (0.1 * 5))')
   assert res == '2.5'


def test_empty_input():
   res = calculator.main('') # Проверяем пустой ввод
   assert res == '0'


def test_empty_bracket():
   res = calculator.main('()') # Проверяем ввод пустых скобок
   assert res == '0'


def test_empty_bracket_in_expression(capsys): # Проверяем пустые скобки внутри выражения
   with pytest.raises(SystemExit) as res: # Проверяем исключение SystemExit
      calculator.main('(    )+1')
   assert res.value.code == 2 # Проверяем код ошибки
   captured = capsys.readouterr()
   assert captured.err.strip() == "Empty brackets error" # Проверяем текст ошибки


def test_unknown_symbol(capsys): # Проверяем неизвестный символ
   with pytest.raises(SystemExit) as res: # Проверяем исключение SystemExit
      calculator.main('1+a')
   assert res.value.code == 2 # Проверяем код ошибки
   captured = capsys.readouterr()
   assert captured.err.strip() == "Unknown symbol error" # Проверяем текст ошибки


def test_double_operator(capsys):  # Проверяем двойной оператор
   with pytest.raises(SystemExit) as res:  # Проверяем исключение SystemExit
      calculator.main('1 */ 1')
   assert res.value.code == 2  # Проверяем код ошибки
   captured = capsys.readouterr()
   assert captured.err.strip() == "Double operator error" # Проверяем текст ошибки


def test_no_operator_1(capsys):  # Проверяем пропущеный оператор
   with pytest.raises(SystemExit) as res:  # Проверяем исключение SystemExit
      calculator.main('1 1 + 1')
   assert res.value.code == 2  # Проверяем код ошибки
   captured = capsys.readouterr()
   assert captured.err.strip() == "No operator error" # Проверяем текст ошибки


def test_no_operator_2(capsys):  # Проверяем пропущеный оператор около скобки
   with pytest.raises(SystemExit) as res:  # Проверяем исключение SystemExit
      calculator.main('1 (1 + 1)')
   assert res.value.code == 2  # Проверяем код ошибки
   captured = capsys.readouterr()
   assert captured.err.strip() == "No operator error" # Проверяем текст ошибки


def test_division_by_zero_1(capsys):  # Проверяем деление на 0
   with pytest.raises(SystemExit) as res:  # Проверяем исключение SystemExit
      calculator.main('1 / 0')
   assert res.value.code == 2  # Проверяем код ошибки
   captured = capsys.readouterr()
   assert captured.err.strip() == "Division by zero error" # Проверяем текст ошибки


def test_division_by_zero_2(capsys):  # Проверяем целочисленное деление на 0
   with pytest.raises(SystemExit) as res:  # Проверяем исключение SystemExit
      calculator.main('1 // 0')
   assert res.value.code == 2  # Проверяем код ошибки
   captured = capsys.readouterr()
   assert captured.err.strip() == "Division by zero error" # Проверяем текст ошибки


def test_division_by_zero_3(capsys):  # Проверяем взятие остатка от деления на 0
   with pytest.raises(SystemExit) as res:  # Проверяем исключение SystemExit
      calculator.main('1 % 0')
   assert res.value.code == 2  # Проверяем код ошибки
   captured = capsys.readouterr()
   assert captured.err.strip() == "Division by zero error" # Проверяем текст ошибки


def test_incorrect_brackets(capsys):  # Проверяем неверное использование скобок
   with pytest.raises(SystemExit) as res:  # Проверяем исключение SystemExit
      calculator.main('(1 + 2 ) )')
   assert res.value.code == 2  # Проверяем код ошибки
   captured = capsys.readouterr()
   assert captured.err.strip() == "Bracket count error" # Проверяем текст ошибки
