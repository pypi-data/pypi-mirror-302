import pandas as pd
import argparse


def load(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)


def gen(df: pd.DataFrame) -> dict:
    report = {
        "Доход": df[df['category'] == 'income']['amount'].sum(),
        "Расход": df[df['category'] == 'expense']['amount'].sum()
    }
    return report


def sav(report: dict, output_file: str):
    with open(output_file, 'w') as f:
        for category, total in report.items():
            f.write(f"{category}: {total} руб.\n")


def main():
    para = argparse.ArgumentParser(description="Генерация отчёта.")
    para.add_argument('--input-file', type=str, required=True, help='Путь к CSV-файлу.')
    para.add_argument('--output-file', type=str, required=True, help='Путь для сохранения отчёта.')

    args = para.parse_args()

    df = load(args.input_file)

    rep = gen(df)

    sav(rep, args.output_file)

    print(f"Отчёт сохранён в {args.output_file}")


if __name__ == "__main__":
    main()

