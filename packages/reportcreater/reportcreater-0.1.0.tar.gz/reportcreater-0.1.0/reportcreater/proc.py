import csv

def create_report(input,output):
    with open(input, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)

        report = {}
        for row in reader:
            if row['category'] in report.keys():
                report[row['category']] += int(row['amount'])
            else:
                report[row['category']] = int(row['amount'])


    with open(output, 'a', encoding='utf-8') as txt_file:
        for key, value in report.items():
            txt_file.write(f'{key}: {value} руб.\n')
