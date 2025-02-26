import pymysql
from typing import Dict, Any


# Исходная БД на чтение
read_dbconfig: Dict[str, Any] = {
    'host': 'ich-db.ccegls0svc9m.eu-central-1.rds.amazonaws.com',
    'user': 'ich1',
    'password': 'password',
    'database': 'sakila',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# Созданная БД для редактирования
edit_dbconfig: Dict[str, Any] = {
    'host': 'ich-edit.edu.itcareerhub.de',
    'user': 'ich1',
    'password': 'ich1_password_ilovedbs',
    'database': '160924_dmytr0',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}