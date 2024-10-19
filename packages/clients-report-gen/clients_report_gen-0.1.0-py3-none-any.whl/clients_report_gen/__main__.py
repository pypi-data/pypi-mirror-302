import argparse
import pandas as pd
def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--input-file', help="Путь к csv")
    parser.add_argument('--output-file', help="Выходной путь")
    args = parser.parse_args()

    if args.input_file and args.output_file:
        df = pd.read_csv(args.input_file)
        bins = [18, 25, 35, 45, 60, 100]
        labels = ['18-25', '26-35', '36-45', '46-60','60+']
        df['age_group'] = pd.cut(df['age'],bins=bins,labels=labels,right=True,include_lowest=True)
        age_groups_dict = df['age_group'].value_counts().sort_index().to_dict()
        city_groups_dict = df['city'].value_counts().to_dict()
        string = f'Общее количество клиентов: {len(df)}\n\nКоличество клиентов по возрастным группам:\n'
        for group, count in age_groups_dict.items():
            string += f'{group}: {count}\n'
        string += f'\nРаспределение клиентов по городам:\n'
        for group, count in city_groups_dict.items():
            string += f'{group}: {count}\n'
        with open(args.output_file,'w',encoding='UTF-8') as file:
            file.write(string.strip())
if __name__ == '__main__':
    main()