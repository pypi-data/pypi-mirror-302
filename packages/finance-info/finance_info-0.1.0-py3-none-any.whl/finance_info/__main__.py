import argparse
import pandas as pd
def main():
    parser = argparse.ArgumentParser(description="Создание отчета по данным о транзакциях")
    parser.add_argument('--input-file', help="Путь к таблице")
    parser.add_argument('--output-file', help="Выходной путь")
    args = parser.parse_args()
    if args.input_file and args.output_file:
        df = pd.read_csv(args.input_file)
        grouped = df.groupby('category')['amount'].sum()
        with open(args.output_file,'w',encoding='UTF-8') as file:
            string = f"Доход: {grouped.iloc[0]}\nРасход: {grouped.iloc[1]}"
            file.write(string)
if __name__ == '__main__':
    main()