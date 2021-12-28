import subprocess
import sys
import xml.etree.ElementTree
import sqlite_req

try:
    import requests
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'requests'])
finally:
    import requests
try:
    from datetime import datetime, timedelta
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'DateTime'])
finally:
    from datetime import datetime, timedelta

def insertDataToSQL():
	test = sqlite_req.checkNum() #[(3060,)]
	if test[0][0] > 3060:
		sqlite_req.deleteData()
	x = 90
	while x > 0:
		date = datetime.now() - timedelta(days=x)
		date = date.strftime('%d/%m/%Y')
		check = sqlite_req.checkDate(date)
		if check != [(34,)]:
			res = requests.get(f'http://www.cbr.ru/scripts/XML_daily_eng.asp?date_req={date}')
			tree = xml.etree.ElementTree.fromstring(res.content)
			val = ''
			for elem in tree:
				tmp = []
				for el in elem:
					tmp.append(el.text)
				tmp.append(date)
				sqlite_req.insertData(tuple(tmp))
		x -= 1


def maxMin(max_min, flag = 0):
	Values = {}
	values = sqlite_req.readValues()
	if flag:
		for val in values:
			Values[val[0]] = float(val[2].replace(',', '.'))
	else:
		for val in values:
			tmp = (float(val[2].replace(',', '.')) / int(val[1]))
			Values[val[0]] = round(tmp, 4)
	if max_min == 'max':
		maxMin_val = max(Values.values())
	else:
		maxMin_val = min(Values.values())
	final_dict = {k:v for k, v in Values.items() if v == maxMin_val}
	return sqlite_req.readName(list(final_dict)[0])

def maxValue():
	print('Максимальное значение курса валюты:')
	Values = maxMin('max')
	for val in Values:
		Values = f"Название валюты: {val[0]}, дата: {val[1].replace('/', '.')}, значение: {val[2]}"
	print(Values)


def minValue(flag):
	print('Минимальное значение курса валюты:')
	Values = maxMin('min', flag)
	for val in Values:
		Values = f"Название валюты: {val[0]}, дата: {val[1].replace('/', '.')}, значение: {val[2]}"
	print(Values)


def avgValue():
	avg = 0
	values = sqlite_req.readValues()
	for val in values:
		avg += float(val[2].replace(',', '.'))
	avg = round(avg/len(values), 4)
	print(f"Cреднее значение курса рубля за весь период по всем валютам: {avg}")

flag = int(input('Для рассчета минимума с учетом наминала введите 1 и нажмите Enter, иначе введите 0: '))
date = datetime.now() - timedelta(days=90)
date = date.strftime('%d/%m/%Y')
insertDataToSQL()
maxValue()
minValue(flag)
avgValue()
