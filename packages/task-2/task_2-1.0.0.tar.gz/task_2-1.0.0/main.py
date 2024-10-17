import pandas as pd
import argparse


def load_transactions(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)


def generate_report(df: pd.DataFrame) -> dict:
    report = {
        "Доход": df[df['Category'] == 'income']['Amount'].sum(),
        "Расход": df[df['Category'] == 'expense']['Amount'].sum()
    }
    return report


def save_report(report: dict, output_file: str):
    with open(output_file, 'w') as f:
        for category, total in report.items():
            f.write(f"{category}: {total} руб.\n")


def main():
    parser = argparse.ArgumentParser(description="Генерация отчёта по транзакциям.")
    parser.add_argument('--input-file', type=str, required=True, help='Путь к входному CSV-файлу с транзакциями.')
    parser.add_argument('--output-file', type=str, required=True, help='Путь для сохранения текстового отчёта.')

    args = parser.parse_args()

    df = load_transactions(args.input_file)

    report = generate_report(df)

    save_report(report, args.output_file)

    print(f"Отчёт успешно сохранён в {args.output_file}")


if __name__ == "__main__":
    main()

