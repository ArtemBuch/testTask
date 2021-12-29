import subprocess
import sys
import xml.etree.ElementTree
import sqlite_req

try:
	import requests
except ImportError:
	print("Установка зависимостей...\n")
	subprocess.check_call([sys.executable, "-m", "pip", "install", 'requests'])
finally:
	import requests
try:
	from datetime import datetime, timedelta
except ImportError:
	print("Установка зависимостей...\n")
	subprocess.check_call([sys.executable, "-m", "pip", "install", 'DateTime'])
finally:
	from datetime import datetime, timedelta

number_of_days = 90
number_of_sql_records_per_day = 34
number_of_sql_records = 3060
 

def insert_data_to_sql(number_of_days, number_of_sql_records_per_day, number_of_sql_records):
	print("Загрузка данных по переводу валют в рубли...\n")
	number_of_sql_records_sql = sqlite_req.check_num()
	if number_of_sql_records_sql[0][0] > number_of_sql_records:
		sqlite_req.delete_data()
	while number_of_days > 0:
		date = datetime.now() - timedelta(days = number_of_days)
		date = date.strftime('%d/%m/%Y')
		number_of_sql_records_per_day_sql = sqlite_req.check_date(date)
		if number_of_sql_records_per_day_sql[0][0] != number_of_sql_records_per_day:
			print(f"Загрузка данных за {date.replace('/', '.')}...")
			res = requests.get(f'http://www.cbr.ru/scripts/XML_daily_eng.asp?date_req={date}')
			tree = xml.etree.ElementTree.fromstring(res.content)
			val = ''
			for elem in tree:
				tmp = []
				for el in elem:
					tmp.append(el.text)
				tmp.append(date)
				sqlite_req.insert_data(tuple(tmp))
		number_of_days -= 1
	print('\n')


def max_min():
	values_dict = {}
	values = sqlite_req.read_values()
	for val in values:
		tmp = (float(val[2].replace(',', '.')) / int(val[1]))
		values_dict[val[0]] = round(tmp, 4)
	return values_dict


def max_value():
	print('Максимальное значение курса валюты:')
	values_dict = max_min()
	max_val = max(values_dict.values())
	final_dict = {k:v for k, v in values_dict.items() if v == max_val}
	values = sqlite_req.read_name(list(final_dict)[0])
	for val in values:
		values = f"Название валюты: {val[0]}, дата: {val[1].replace('/', '.')}, значение: {round(float(val[2].replace(',', '.')) / int(val[3]), 4)}\n"
	print(values)


def min_value():
	print('Минимальное значение курса валюты:')
	values_dict = max_min()
	min_val = min(values_dict.values())
	final_dict = {k:v for k, v in values_dict.items() if v == min_val}
	values = sqlite_req.read_name(list(final_dict)[0])
	for val in values:
		values = f"Название валюты: {val[0]}, дата: {val[1].replace('/', '.')}, значение: {round(float(val[2].replace(',', '.')) / int(val[3]), 4)}\n"
	print(values)


def avg_value():
	avg = 0
	values = sqlite_req.read_values()
	for val in values:
		tmp = (float(val[2].replace(',', '.')) / int(val[1]))
		avg += round(tmp, 4)
	avg = round(avg/len(values), 4)
	print(f"Cреднее значение курса рубля за весь период по всем валютам: {avg}")


insert_data_to_sql(number_of_days, number_of_sql_records_per_day, number_of_sql_records)
max_value()
min_value()
avg_value()
