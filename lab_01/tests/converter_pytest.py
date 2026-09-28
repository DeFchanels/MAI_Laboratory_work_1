import sys

import pytest

from toolkit import converter
from toolkit.__main__ import main


def test_cli_1(capsys, monkeypatch):
    cli_args = ["toolkit", "converter", "1", "--from", "g", "--to", "kg"] # Имитируем ввод в терминале: python -m toolkit converter "1" --from "g" --to "kg"
    monkeypatch.setattr(sys, "argv", cli_args)
    main()
    captured = capsys.readouterr() # Считываем вывод
    assert captured.out.strip() == '0.001'


def test_cli_empty(capsys, monkeypatch):
    cli_args = ["toolkit", "converter", "1", "--from", "", "--to", ""] # Имитируем ввод в терминале: python -m toolkit converter "1" --from='' --to=''
    monkeypatch.setattr(sys, "argv", cli_args)
    with pytest.raises(SystemExit) as exit_info:
        main()
    assert exit_info.value.code == 2
    captured = capsys.readouterr()
    assert captured.err.strip() == "Unknown unit of measurement"


def test_temperature_1():
   res = converter.main('273.15', 'k', 'c')
   assert res == '0'


def test_temperature_2():
   res = converter.main('-273.15', 'c', 'k')
   assert res == '0'


def test_temperature_3():
   res = converter.main('26', 'c', 'f')
   assert res == '78.8'


def test_temperature_4():
   res = converter.main('0', 'c', 'f')
   assert res == '32'


def test_mass_1():
   res = converter.main('1', 'g', 'kg')
   assert res == '0.001'


def test_mass_2():
   res = converter.main('1.5', 'kg', 'g')
   assert res == '1500'


def test_mass_3():
   res = converter.main('1.5', 't', 'kg')
   assert res == '1500'


def test_distance_1():
   res = converter.main('1', 'm', 'mm')
   assert res == '1000'


def test_distance_2():
   res = converter.main('1.52', 'km', 'm')
   assert res == '1520'


def test_distance_3():
   res = converter.main('1000', 'mm', 'm')
   assert res == '1'


def test_empty_input(capsys): # Проверяем пустой ввод
   with pytest.raises(SystemExit) as res: # Проверяем исключение SystemExit
      converter.main('', 'g', 'kg')
   assert res.value.code == 2 # Проверяем код ошибки
   captured = capsys.readouterr()
   assert captured.err.strip() == "Empty input" # Проверяем текст ошибки


def test_unmatched_units(capsys): # Проверяем несовпадающие категории едениц измерения
   with pytest.raises(SystemExit) as res: # Проверяем исключение SystemExit
      converter.main('1', 'g', 'm')
   assert res.value.code == 2 # Проверяем код ошибки
   captured = capsys.readouterr()
   assert captured.err.strip() == "Mismatched unit categories" # Проверяем текст ошибки


def test_temperature_below_absolute_zero(capsys): # Проверяем температуру ниже абсолютного нуля
   with pytest.raises(SystemExit) as res: # Проверяем исключение SystemExit
      converter.main('-273.16', 'c', 'k')
   assert res.value.code == 2 # Проверяем код ошибки
   captured = capsys.readouterr()
   assert captured.err.strip() == "Temperature is below absolute zero" # Проверяем текст ошибки


def test_wrong_value(capsys): # Проверяем значение меньше 0 для едениц измерения где это невозможно
   with pytest.raises(SystemExit) as res: # Проверяем исключение SystemExit
      converter.main('-1', 'g', 'kg')
   assert res.value.code == 2 # Проверяем код ошибки
   captured = capsys.readouterr()
   assert captured.err.strip() == "Impossible value" # Проверяем текст ошибки