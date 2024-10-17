import pandas as pd
import argparse

def load_sales_data(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)

def generate_sales_report(df: pd.DataFrame) -> pd.DataFrame:
    report = df.groupby('category').agg(
        sales=('sales', 'sum'),
        quantity=('quantity', 'sum')
    ).reset_index()
    return report

def save_report(report: pd.DataFrame, output_file: str):
    report.to_csv(output_file, index=False)

def main():
    parser = argparse.ArgumentParser(description="Генерация отчёта по продажам.")
    parser.add_argument('--input-file', type=str, required=True, help='Путь к входному CSV-файлу с данными о продажах.')
    parser.add_argument('--output-file', type=str, required=True, help='Путь для сохранения отчёта в CSV.')

    args = parser.parse
    df = load_sales_data(args.input_file)


    report = generate_sales_report(df)


    save_report(report, args.output_file)

    print(f"Отчёт успешно сохранён в {args.output_file}")


if __name__ == "__main__":
    main()
