from itertools import product
from decimal import Decimal
import decimal
import string
import sys
import re


def processing_errors(expression): # Функция, валидирующая данные (Validation)
    """
    Accepts an expression;
    Terminates code with an error message if any issues arise, or returns 0 otherwise.
    """
    if any(symbol not in ' 0123456789-+*/()%.' for symbol in expression): # Обработка неизвестных для калькулятора символов
        print("Unknown symbol error", file=sys.stderr)
        sys.exit(2)

    if '()' in expression.replace(' ', ''):  # Если есть пустые скобки внутри самого выражения (само выражение не пустое)
        print("Empty brackets error", file=sys.stderr)
        sys.exit(2)

    if '..' in expression:
        print("Incorrect float value", file=sys.stderr)
        sys.exit(2)

    for p in product('0123456789', repeat=2): # Обработка пропущеного оператора между цифрами
        if ' '.join(p) in expression:
            print("No operator error", file=sys.stderr)
            sys.exit(2)

    for n in '0123456789': # Обработка пропущенного оператора между скобками и цифрами
        if any(x in expression for x in [f') {n}', f'{n} (', ') (']):
            print("No operator error", file=sys.stderr)
            sys.exit(2)

    double_symbols = ['* *', '* /', '/ *', '+ *', '- *', '- /', '+ /', '% %', '% /', '% *', '/ %', '* %', '- %', '+ %']
    if any(doubles in expression for doubles in double_symbols): # Обработка невозможных двойных операторов
        print("Double operator error", file=sys.stderr)
        sys.exit(2)

    if '/ 0 ' in expression or ('/ 0' in expression and expression.endswith('0')): # Обработка деления на 0
        print("Division by zero error", file=sys.stderr)
        sys.exit(2)

    if '% 0 ' in expression or ('% 0' in expression and expression.endswith('0')): # Обработка остатка от деления на 0
        print("Division by zero error", file=sys.stderr)
        sys.exit(2)

    if expression.count('(') != expression.count(')'): # Обработка ошибки в количестве скобок
        print("Bracket count error", file=sys.stderr)
        sys.exit(2)
    return 0


def rindex(li, symbol): # Функция для нахождения самого правого вхождения необходимого символа в список
    """
    Accepts list and a symbol to find;
    Returns the rightmost index of the symbol in the list.
    """
    res = ''
    for i in range(0, len(li)):
        if li[i] == symbol:
            res = i
    if res != '': return res
    raise ValueError


def basic_operations(expression): # Функция калькуляции выражения, с заранее обработанными скобками (Calculation)
    """
    Accepts an expression;
    Returns the result of calculating this expression.
    """
    expression = processing_brackets(expression) # Обрабатываем скобки в выражении
    while any(x in expression for x in ['*', '/', '//', '%']): # Цикл, повторяющийся пока есть операции с наивысшим приоритетом
        expression = process_negative_and_positive_numbers(expression) # Обрабатываем плюсы и минусы после знаков умножения и деления
        for i in range(0, len(expression)):
            if expression[i] in ['*', '/', '//', '%']:
                if i == 0 or i == len(expression) - 1: # Если оператор это первый или последний символ в выражении
                    raise SyntaxError('Incorrect syntaxis')
                else:
                    match expression[i]:
                        case '*':
                            expression = expression[:i - 1] + [str(Decimal(expression[i - 1]) * Decimal(expression[i + 1]))] + expression[i + 2:]
                            break
                        case '/':
                            expression = expression[:i - 1] + [str(Decimal(expression[i - 1]) / Decimal(expression[i + 1]))] + expression[i + 2:]
                            break
                        case '//':
                            expression = expression[:i - 1] + [str(Decimal(expression[i - 1]) // Decimal(expression[i + 1]))] + expression[i + 2:]
                            break
                        case '%':
                            expression = expression[:i - 1] + [str(Decimal(expression[i - 1]) % Decimal(expression[i + 1]))] + expression[i + 2:]
                            break
    while len(expression) > 1: # Цикл, повторяющийся пока выражение не досчитано до конца
        for i in range(0, len(expression)):
            if expression[i] in '+-':
                if i == 0 or i == len(expression) - 1: # Если оператор это первый или последний символ в выражении
                    raise SyntaxError('Incorrect syntaxis')
                else:
                    match expression[i]:
                        case '+':
                            expression = expression[:i - 1] + [str(Decimal(expression[i - 1]) + Decimal(expression[i + 1]))] + expression[i + 2:]
                            break
                        case '-':
                            expression = expression[:i - 1] + [str(Decimal(expression[i - 1]) - Decimal(expression[i + 1]))] + expression[i + 2:]
                            break
    if Decimal(expression[0]) == int(Decimal(expression[0])):  # Если число целое, возвращаем его без плавающей запятой
        return str(int(Decimal(expression[0])))
    return expression[0]


def process_negative_and_positive_numbers(expression): # Функция для обрабоки знаков вокруг умножения, деления и взятия остатка
    """
    Accepts an expression;
    Returns it with processed unary numbers near division, multiplication or modulo
    """
    for i in range(2, len(expression) - 1):
        if expression[i] == '/' or expression[i] == '*' or expression[i] == '//' or expression[i] == '%':
            if expression[i - 2] == '-' or expression[i - 2] == '+':
                if not((i - 3 >= 0) and (expression[i - 3][-1] in '1234567890)')):
                    expression[i - 1] = expression[i - 2] + expression[i - 1]
                    expression.pop(i - 2)
    for i in range(len(expression) - 2):
        if (expression[i] == '/' or expression[i] == '*' or expression[i] == '//' or expression[i] == '%') and expression[i + 2] != '(':
            if expression[i + 1] == '-' or expression[i + 1] == '+':
                expression[i + 2] = expression[i + 1] + expression[i + 2]
                expression.pop(i + 1)
    return expression


def process_input(input_expression): # Функция, токенизирующая введенного выражения (Tokenization)
    """
    Accepts an expression;
    Returns it in processed form (List of expression operands and operators, with unary operators processed)
    """
    input_expression = re.sub(r" +", " ", input_expression)
    input_expression = input_expression.replace('/ /', '//')
    input_expression = re.sub(r'\+\s*-', '-', input_expression) # Заменяем двойные знаки (знак, и потом унарный знак) на одинарные
    input_expression = re.sub(r'\-\s*\+', '-', input_expression)
    for n in '0987654321':
        input_expression = re.sub(r'\+\s*\+\s*({}|\()'.format(n), r'+\1', input_expression) # Если после двойного знака есть число либо открывающая скобка, значит обрабатываем это как один знак
        input_expression = re.sub(r'-\s*-\s*({}|\()'.format(n), r'+\1', input_expression)
    input_expression = re.sub(r'\+\s*\+', '+1', input_expression) # В ином случае это либо инкремент, либо декремент
    input_expression = re.sub(r'-\s*-', '-1', input_expression)
    processed_list = re.split(r'(//|[/|(|)|\+|\-|\*|%|\s])', input_expression) # Разделяем строчку по всем символам знаков и знаку пробела
    result_expression = [x for x in processed_list if x and x != ' '] # Очищаем разделенную строчку от None и пробелов
    if result_expression[0] == '-' or result_expression[0] == '+':
        result_expression[1] = result_expression[0] + result_expression[1]
        result_expression.pop(0)
    result_expression = process_negative_and_positive_numbers(result_expression) # Обрабатываем плюсы и минусы после знаков умножения и деления
    processing_errors(' '.join(result_expression)) # Запускаем функцию валидации
    return result_expression


def processing_brackets(processed_expression): # Функция для обработки скобок в выражении
    """
    Accepts an expression;
    Returns the expression processed by evaluating the expressions within the parentheses.
    """
    while '(' in processed_expression: # Пока есть скобки в выражении
        left_branch_index = rindex(processed_expression, '(') # Ищем самое правое вхождение левой скобки
        right_branch_index = processed_expression[left_branch_index:].index(')') + left_branch_index # Ищем индекс ближайшей к нужной скобке ее правой пары
        mini_expression = processed_expression[left_branch_index + 1: right_branch_index] # Выражение внутри найденных скобок
        processed_expression = processed_expression[:left_branch_index] + [str(basic_operations(mini_expression))] + processed_expression[right_branch_index + 1:] # Подсчитываем внутрискобочное выражение и записываем его результат вместо скобок
    return processed_expression


def setup_parser(subparsers):
    """
    Creates an argument parser
    """
    parser = subparsers.add_parser('calc', help='Basic calculator program')
    parser.add_argument("expression", nargs='?', type=str, default='0', help="Expression to calculate")


def main(expression):
    decimal.getcontext().prec = 28 # Устанавливаем точность на 28 значащих цифр
    decimal.getcontext().rounding = decimal.ROUND_HALF_UP # Устанавливаем округление чисел вверх
    input_expression = expression
    if not expression or not(any(x in expression for x in string.digits)): # Обработка пустого ввода или ввода без цифр
        return '0'
    processed_expression = process_input(input_expression)
    return basic_operations(processed_expression)
    