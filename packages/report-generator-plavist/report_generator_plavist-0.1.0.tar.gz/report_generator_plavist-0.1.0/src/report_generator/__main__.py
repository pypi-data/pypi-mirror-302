import argparse
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description="Создание отчета по данным о продажах")
    parser.add_argument('--input-file', help="Путь к таблице")
    parser.add_argument('--output-file', help="Выходной путь")

    args = parser.parse_args()
    if args.input_file and args.output_file:
        df = pd.read_csv(args.input_file)
        grouped = df.groupby('category').sum()
        grouped.to_csv(args.output_file)
if __name__ == "__main__":
    main()