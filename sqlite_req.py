import sqlite3
from sqlite3 import Error
import os

path = f'{os.path.abspath(__file__)[0:-13]}\sm_app.sqlite'


def create_connection(path):
    """
    Создаем подключение
    """
    connection = None
    try:
        connection = sqlite3.connect(path)
        #print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


connection = create_connection(path)


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_query(connection, query):
    """
    Запрос
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        #print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def insert_data(val):
    """
    Запись данных в sql
    """
    sql_query = f"""
    INSERT INTO
      Finance (NumCode, CharCode, Nominal, Name, Value, Date)
    VALUES
      {val};
    """
    execute_query(connection, sql_query)

def check_num():
    """
    Проверяем есть ли данные за этот день(Всего 34 записи в день)
    """
    sql_query = f"""
    SELECT 
    COUNT(*) 
    FROM 
      Finance 
    """
    check = execute_read_query(connection, sql_query)
    return check

def delete_data():
    """
    Запись данных в sql
    """
    sql_query = f"""
    Delete 
    from 
      Finance 
    where 
    rowid IN (Select rowid from Finance limit 34)
    """
    execute_query(connection, sql_query)


def check_date(val):
    """
    Проверяем есть ли данные за этот день(Всего 34 записи в день)
    """
    sql_query = f"""
    SELECT 
    COUNT(*) 
    FROM 
      Finance 
    WHERE 
      Date='{val}' 
    """
    check = execute_read_query(connection, sql_query)
    return check

def read_values():
    """
    Вывод всех данных(Value) за день
    """
    sql_query = f"""
    SELECT
      Finance.id,
      Finance.Nominal,
      Finance.Value
    FROM
      Finance
    """
    values = execute_read_query(connection, sql_query)
    return values

def read_name(val):
    """
    Вывод названия валюты, даты и значения
    """
    sql_query = f"""
    SELECT
      Finance.Name,
      Finance.Date,
      Finance.Value,
      Finance.Nominal
    FROM
      Finance
    WHERE
      Finance.id = '{val}'
    """
    read_name = execute_read_query(connection, sql_query)
    return read_name


#Создание таблиц
create_cons_table = """
CREATE TABLE IF NOT EXISTS Finance(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    NumCode TEXT,
    CharCode TEXT,
    Nominal TEXT,
    Name TEXT,
    Value TEXT,
    Date TEXT
);
"""

execute_query(connection, create_cons_table)
