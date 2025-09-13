import chardet
import csv
import pandas

with open('test/email_logs.csv', 'rb') as file:
    print('Detected: ', chardet.detect(file.read()))

print(csv.list_dialects())
with open('test/email_logs.csv', encoding='utf-8-sig') as file:
    email_data = csv.DictReader(file, delimiter=',')
    for row in email_data:
        print(row)

df = pandas.read_csv('test/email_logs.csv')