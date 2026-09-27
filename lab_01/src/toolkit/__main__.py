import argparse
from . import calculator, converter


def main():
    parser = argparse.ArgumentParser(description='Набор базовых инструментов')
    subparsers = parser.add_subparsers(dest='program', help='Доступные подпрограммы')
    subparsers.required = True
    calculator.setup_parser(subparsers)
    converter.setup_parser(subparsers)
    args = parser.parse_args()
    if args.program == 'calc':
        print(calculator.main(' ' + args.expression))
    elif args.program == 'converter':
        print(converter.main(args.value, args.unit_from, args.unit_to))


if __name__ == "__main__":
    main()