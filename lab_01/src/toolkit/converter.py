import json
import sys
from decimal import Decimal
import decimal
from pathlib import Path


current_dir = Path(__file__).parent # Получаем путь к папке, в которой лежит текущий файл
table_path = current_dir / 'convertion_table.json' # Формируем точный путь к таблице конвертаций
with open(table_path, 'r', encoding='utf-8') as file: # Считываем таблицу конвертаций из json файла
    convertion_table = json.load(file)


def get_category(unit): 
    """
    Accepts a single unit of measurement as input;
    Returns its category.
    """
    for category in convertion_table.keys(): # Цикл по категориям
        if unit in convertion_table[category]['units'].keys(): # Если еденица измерения в категории то возвращаем эту категорию
            return category
    print("Unknown unit of measurement", file=sys.stderr) # Если еденица измерения не найдена в данных
    sys.exit(2)


def processing_errors(input_value, unit_from, category_from, category_to): # Функция обработки ошибок (Валидация данных)
    """
    Accepts a value, an initial unit of measurement, and the categories of the initial and target units of measurement;
    Terminates code with an error message if any issues arise, or returns 0 otherwise.
    """
    if not any(x in input_value for x in '0987654321'):
        print("Empty input", file=sys.stderr) # Если ввод пуст
        sys.exit(2)
    input_value = Decimal(input_value)
    if category_to != category_from: # Если не совпадают категории едениц измерения
        print("Mismatched unit categories", file=sys.stderr) # Если категории едениц измерения не совпадают
        sys.exit(2)
    if category_from == 'temperature':
        value_cel = (input_value + Decimal(convertion_table[category_from]['units'][unit_from]['addition'])) / Decimal(convertion_table[category_from]['units'][unit_from]['divisor']) # Для удобства переводим температуру в цельсии
        if value_cel < Decimal(str(-273.15)): # Если температура ниже абсолютного нуля возвращаем ошибку
            print("Temperature is below absolute zero", file=sys.stderr)
            sys.exit(2)
    if not convertion_table[category_from]['can_be_negative'] and input_value < 0: # Если значение не может быть отрицательным, но пользователь ввел отрицательное число, выводим ошибку
        print("Impossible value", file=sys.stderr)
        sys.exit(2)
    return 0


def convert_units(input_value, unit_from, unit_to, category): # Функция перевода между еденицами измерения
    """
    Accepts a value, an initial unit of measurement, target unit of measurement and category; 
    Returns the value converted from the initial to the target unit.
    """
    if category == 'temperature': # Отдельно обрабатываем температуру
        value_cel = (input_value + Decimal(convertion_table[category]['units'][unit_from]['addition'])) / Decimal(convertion_table[category]['units'][unit_from]['divisor']) # Переводим температуру в градусы цельсия
        res_value = value_cel * Decimal(convertion_table[category]['units'][unit_to]['divisor']) - Decimal(convertion_table[category]['units'][unit_to]['addition']) # Итоговое значение
    else: # Любые категории кроме температуры
        si_value = input_value * Decimal(convertion_table[category]['units'][unit_from]) # Значение в СИ
        res_value = si_value / Decimal(convertion_table[category]['units'][unit_to]) # Результат
    if Decimal(res_value) == int(Decimal(res_value)):  # Если число целое, возвращаем его без плавающей запятой
        return str(int(Decimal(res_value)))
    return res_value
        

def setup_parser(subparsers):
    """
    Creates an argument parser
    """
    parser = subparsers.add_parser('converter', help='Converter program')
    parser.add_argument("value", type=str, help="Value to convert")
    parser.add_argument("--from", dest='unit_from', required=True, type=str, help="Unit from which the value is to be converted")
    parser.add_argument("--to", dest='unit_to', type=str, required=True, help="Unit to which the value is to be converted")


def main(value, unit_from, unit_to):
    decimal.getcontext().prec = 10 # Устанавливаем точность на 10 значащих цифры
    decimal.getcontext().rounding = decimal.ROUND_HALF_UP # Устанавливаем округление вверх 
    input_value = value # Значение для перевода
    unit_from = unit_from.lower() # Начальная еденица измерения
    unit_to = unit_to.lower() # Конечная еденица измерения
    category_from = get_category(unit_from) # Получаем категорию начальной еденицы измерения
    category_to = get_category(unit_to) # Получаем категорию начальной еденицы измерения
    processing_errors(input_value, unit_from, category_from, category_to) # Валидируем данные
    input_value = Decimal(input_value)
    return str(convert_units(input_value, unit_from, unit_to, category_from))
    