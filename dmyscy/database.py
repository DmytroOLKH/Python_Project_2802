from datetime import datetime, timedelta
import pymysql
from collections import Counter
from typing import Dict, Any
import json
from config import read_dbconfig, edit_dbconfig


def get_connection(dbconfig: Dict[str, Any]):
    """
    Устанавливаем соединение с БД.
    """
    return pymysql.connect(**dbconfig)

def display_popular_queries_last_n_days(n_days: int) -> None:
    """
    Отображаем популярные запросы за последние N дней.
    """
    try:
        # Вычисляем дату начала (сегодня - N дней)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=n_days)

        # Форматируем даты для SQL-запроса
        start_date_str = start_date.strftime("%Y-%m-%d %H:%M:%S")
        end_date_str = end_date.strftime("%Y-%m-%d %H:%M:%S")

        connection = get_connection(edit_dbconfig)
        try:
            with connection.cursor() as cursor:
                sql = """
                SELECT query, COUNT(*) as search_count
                FROM search_history
                WHERE timestamp BETWEEN %s AND %s
                GROUP BY query
                ORDER BY search_count DESC
                LIMIT 10
                """
                cursor.execute(sql,(start_date_str, end_date_str))
                popular_queries = cursor.fetchall()

                if popular_queries:
                    print(f"Popular searches in the last {n_days} days:")
                    for rank, entry in enumerate(popular_queries, 1):
                        print(f"{rank}. Query : {entry['query']}, Quantity: {entry['search_count']}")
                else:
                    print(f"No queries found for the last {n_days} days.")
        finally:
            connection.close()
    except Exception as e:
        print(f"Error when retrieving popular queries for the last {n_days} days: {e}")


def save_search_query_to_db():
    """
    Сохраняем все запросы из JSON-файла в БД_edit.
    """
    try:
        # Чтение существующих данных
        with open("search_history.json", "r", encoding="utf-8") as file:
            history = json.load(file)

        # Подключаемся к БД_edit и записываем запросы
        connection = get_connection(edit_dbconfig)
        try:
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO search_history (query, search_type, timestamp)
                VALUES (%s, %s, %s)
                """
                for entry in history:
                    cursor.execute(sql, (entry["query"], entry["search_type"], entry["timestamp"]))
            connection.commit()
        finally:
            connection.close()
    except FileNotFoundError:
        print("Search history is empty. There is nothing to write to the database.")
    except Exception as e:
        print(f"Error when saving queries to the database: {e}")


""" Тестовая функция для сохранения запроса
def test_save_query():
    save_search_query("example query", "keyword")
    save_search_query_to_db()

# Запускаем тестовую функцию
test_save_query()

# Проверка создания файла и его содержимого
with open("search_history.json", "r", encoding="utf-8") as file:
    history = json.load(file)
    # print(history)
"""
