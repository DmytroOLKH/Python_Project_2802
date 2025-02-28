from database import get_connection, read_dbconfig
from typing import List, Dict

def search_movies_by_keyword(keyword: str):
    """
    Поиск фильмов по ключевому слову в названии или описании.
    """
    try:
        with get_connection(read_dbconfig) as connection:
            with connection.cursor() as cursor:
                sql = """
                SELECT title, description
                FROM film
                WHERE title LIKE %s OR description LIKE %s
                """
                cursor.execute(sql, ('%' + keyword + '%', '%' + keyword + '%'))
                return cursor.fetchall()
    except Exception as e:
        print(f"Error when searching for movies:: {e}")
    return []

def search_movies_by_genre(genre_id: int):
    """
    Поиск фильмов по ID жанра.
    """
    try:
        with get_connection(read_dbconfig) as connection:
            with connection.cursor() as cursor:
                sql = """
                SELECT f.title, f.description
                FROM film f
                JOIN film_category fc ON f.film_id = fc.film_id
                JOIN category c ON fc.category_id = c.category_id
                WHERE c.category_id = %s
                """
                cursor.execute(sql, (genre_id,))
                return cursor.fetchall()
    except Exception as e:
        print(f"Error when searching for movies: {e}")
    return []

def search_movies_by_year(release_year: int):
    """
    Поиск фильмов по году выпуска.
    """
    try:
        with get_connection(read_dbconfig) as connection:
            with connection.cursor() as cursor:
                sql = """
                SELECT title, description
                FROM film
                WHERE release_year = %s
                """
                cursor.execute(sql, (release_year,))
                return cursor.fetchall()
    except Exception as e:
        print(f"Error when searching for movies: {e}")
    return []

def search_movies_by_genre_and_year(genre_id: int, release_year: int):
    """
    Поиск фильмов по жанру и году выпуска.
    """
    try:
        with get_connection(read_dbconfig) as connection:
            with connection.cursor() as cursor:
                sql = """
                SELECT f.title, f.description
                FROM film f
                JOIN film_category fc ON f.film_id = fc.film_id
                JOIN category c ON fc.category_id = c.category_id
                WHERE c.category_id = %s AND f.release_year = %s
                """
                cursor.execute(sql, (genre_id, release_year))
                return cursor.fetchall()
    except Exception as e:
        print(f"Error when searching for movies: {e}")
    return []



