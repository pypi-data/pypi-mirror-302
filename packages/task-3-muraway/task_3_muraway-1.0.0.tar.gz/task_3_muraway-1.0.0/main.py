import pandas as pd
import argparse

def load(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)

def gen(df: pd.DataFrame) -> pd.DataFrame:
    report = df.groupby('category').agg(
        sales=('sales', 'sum'),
        quantity=('quantity', 'sum')
    ).reset_index()
    return report

def sav(report: pd.DataFrame, output_file: str):
    report.to_csv(output_file, index=False)

def main():
    para = argparse.ArgumentParser(description="Генерация отчёта.")
    para.add_argument('--input-file', type=str, required=True, help='Путь к CSV-файлу.')
    para.add_argument('--output-file', type=str, required=True, help='Путь для сохранения в CSV.')

    args = para.parse
    df = load(args.input_file)


    rep = gen(df)


    sav(rep, args.output_file)

    print(f"Отчёт сохранён в {args.output_file}")


if __name__ == "__main__":
    main()
