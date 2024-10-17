import pandas as pd
import argparse

def load_customer_data(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)

def generate_report(df: pd.DataFrame) -> str:
    report_lines = []
    total_customers = len(df)
    report_lines.append(f"Общее количество клиентов: {total_customers}\n")

    age_groups = pd.cut(df['age'], bins=[17, 25, 35, 45, 60, 100], right=True, labels=['18-25', '26-35', '36-45', '46-60', '60+'])
    age_distribution = age_groups.value_counts().sort_index()
    report_lines.append("Количество клиентов по возрастным группам:")
    for age_group, count in age_distribution.items():
        report_lines.append(f"{age_group}: {count}")

    city_distribution = df['city'].value_counts()
    report_lines.append("Распределение клиентов по городам:")
    for city, count in city_distribution.items():
        report_lines.append(f"{city}: {count}")

    return '\n'.join(report_lines)

def save_report(report: str, output_file: str):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

def main():
    parser = argparse.ArgumentParser(description="Генерация отчёта о клиентах.")
    parser.add_argument('--input-file', type=str, required=True, help='Путь к входному CSV-файлу с данными о клиентах.')
    parser.add_argument('--output-file', type=str, required=True, help='Путь для сохранения текстового файла с отчётом.')

    args = parser.parse_args()

    df = load_customer_data(args.input_file)

    report = generate_report(df)

    save_report(report, args.output_file)

    print(f"Отчёт успешно сохранён в {args.output_file}")

if __name__ == "__main__":
    main()
