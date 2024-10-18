import pandas as pd
import argparse


def analyze_transactions(input_file, output_file):
    """Функция для загрузки данных о транзакциях и их анализа."""
    # Чтение данных из CSV-файла
    data = pd.read_csv(input_file)

    # Группировка данных по категории и суммирование
    summary = data.groupby('category')['amount'].sum()

    # Формирование отчета
    with open(output_file, 'w') as f:
        for category, amount in summary.items():
            f.write(f"{category}: {amount:.2f} руб.\n")


def main():
    # Определение аргументов командной строки
    parser = argparse.ArgumentParser(description="Анализ транзакций по категориям.")
    parser.add_argument('--input-file', type=str, required=True, help="Путь к CSV-файлу с транзакциями")
    parser.add_argument('--output-file', type=str, required=True, help="Путь к файлу для сохранения отчета")

    args = parser.parse_args()

    # Запуск анализа транзакций
    analyze_transactions(args.input_file, args.output_file)


# Чтобы можно было запускать напрямую через командную строку
if __name__ == '__main__':
    main()
