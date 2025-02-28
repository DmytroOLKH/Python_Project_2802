from datetime import date, datetime
import json
from collections import Counter
from typing import List, Dict, Any
from  search_bd import(
    search_movies_by_keyword,
    search_movies_by_genre,
    search_movies_by_year,
    search_movies_by_genre_and_year)

from database import save_search_query_to_db, display_popular_queries_last_n_days

def display_results(results: List[Dict[str, str]]) -> None:
    """
    Выводим результаты поиска по страницам.
     """
    lines_per_page = 10
    start = 0
    total_results = len(results)

    while start < total_results:
        end = start + lines_per_page
        for id_, row in enumerate(results[start:end], start + 1):
            print(f"{id_}. Title: {row['title']}\nDescription: {row['description']}\n")

        start = end
        if start < total_results:
            user_input = input("Enter '1' to continue or '0' to exit:")
            if user_input.strip() == '0':
                return
            elif user_input.strip() != '1':
                print("Invalid input. Please enter '1' or '0'.")

def display_popular_queries_today() -> None:
    """
    Возвращаем список популярных запросов из лок_файла search_history.json.
    """
    try:
        with open("search_history.json", "r", encoding="utf-8") as file:
            history = json.load(file)

        today = date.today().strftime("%Y-%m-%d")
        today_queries = [entry for entry in history if entry["timestamp"].startswith(today)]

        if not today_queries:
            print("No popular queries found for today.")
            return

        query_counter = Counter(entry["query"] for entry in today_queries)
        popular_queries = query_counter.most_common(10)

        print("Popular queries for today:")
        for rank, (query, count) in enumerate(popular_queries, 1):
            print(f"{rank}. Query: {query}, Quantity: {count}")

        # Очищаем данные в JSON-файле, кроме текущего дня
        with open("search_history.json", "w", encoding="utf-8") as file:
            json.dump(today_queries, file, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        print("The request history is empty.")
    except Exception as e:
        print(f"Error when getting popular queries for today: {e}")



def save_search_query(query: str, search_type: str):
    """
    Сохраняем запрос в JSON-файл.
    """
    try:
        # Читаем данные
        try:
            with open("search_history.json", "r", encoding="utf-8") as file:
                history = json.load(file)
        except FileNotFoundError:
            history = []
        # Добавляем новый запрос
        history.append({
            "query": query,
            "search_type": search_type,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        # Сохраняем обновленных данных
        with open("search_history.json", "w", encoding="utf-8") as file:
            json.dump(history, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error when saving request: {e}")



def main_menu() -> None:
    """
    Основное меню программы.
    """
    while True:
        print("Select action: ")
        print("1. Search movies by keyword")
        print("2. Search movies by genre")
        print("3. Search movies by year")
        print("4. Search films by genre and year")
        print("5. Show popular searches today")
        print("6. Show popular queries for the last N days")
        print("0. Exit the program")
        choice = input("Enter action number: ")

        if choice == '1':
            keyword = input("Enter a keyword to search for movies: ")
            if len(keyword) < 2 or not any(char.isalpha() for char in keyword):
                print("Please enter a valid keyword with at least 2 characters and at least one letter.")
            else:
                results = search_movies_by_keyword(keyword)
                if results:
                    display_results(results)
                else:
                    print("No films found.")
                save_search_query(keyword, 'keyword')


        elif choice == '2':
            genres = [
                "1. Action", "2. Animation", "3. Children", "4. Classics", "5. Comedy",
                "6. Documentary", "7. Drama", "8. Family", "9. Foreign", "10. Games",
                "11. Horror", "12. Music", "13. New", "14. Sci-Fi", "15. Sports", "16. Travel"
            ]
            while True:
                for genre in genres:
                    print(genre)
                genre_choice = input("Enter genre number (1-16) or 0(zero) to exit: ")

                if genre_choice == '0':
                    break
                elif genre_choice.isdigit() and 1 <= int(genre_choice) <= 16:
                    genre_id = int(genre_choice)
                    results = search_movies_by_genre(genre_id)
                    if results:
                        display_results(results)
                    else:
                        print("No films found.")
                    save_search_query(genres[genre_id - 1].split(". ")[1],'genre')
                    break
                else:
                    print("Please enter 1-16 or 0(zero) to exit: ")

        elif choice == '3':
            year = input("Enter the year the movie was released (1990-2025): ")
            if year.isdigit() and 1990 <= int(year) <= 2025:
                results = search_movies_by_year(int(year))
                if results:
                    display_results(results)
                else:
                    print("No films found.")
                save_search_query(year, 'year')
            else:
                print("Invalid input. Please enter a year between 1990 and 2025.")

        elif choice == '4':
            genres = [
                "1. Action", "2. Animation", "3. Children", "4. Classics", "5. Comedy",
                "6. Documentary", "7. Drama", "8. Family", "9. Foreign", "10. Games",
                "11. Horror", "12. Music", "13. New", "14. Sci-Fi", "15. Sports", "16. Travel"
            ]
            while True:
                for genre in genres:
                    print(genre)
                genre_choice = input("Enter genre number (1-16) or 0(zero) to exit: ")

                if genre_choice == '0':
                    break
                elif genre_choice.isdigit() and 1 <= int(genre_choice) <= 16:
                    genre_id = int(genre_choice)
                    year = input("Enter the year the movie was released (1990-2025): ")
                    if year.isdigit() and 1990 <= int(year) <= 2025:
                        results = search_movies_by_genre_and_year(genre_id, int(year))
                        if results:
                            display_results(results)
                        else:
                            print("No films found.")
                        save_search_query(f"{genres[genre_id - 1].split('. ')[1]} {year}", 'genre_year')
                        break
                    else:
                        print("Invalid input. Please enter a year between 1990 and 2025.")
                else:
                    print("Please enter 1-16 or 0(zero) to exit: ")

        elif choice == '5':
            display_popular_queries_today()


        elif choice == '6':
            try:
                n_days = int(input("Enter the number of days to display popular queries: "))
                if n_days <= 0:
                    raise ValueError("The number of days must be greater than zero.")
                display_popular_queries_last_n_days(n_days)
            except ValueError:
                print("Please enter a valid number.")

        elif choice == '0':
            try:
                with open("search_history.json", "r", encoding="utf-8") as file:
                    history = json.load(file)
                save_search_query_to_db()
                print("Writing to SQL database completed successfully.")
            except Exception as e:
                print(f"Error writing to SQL database: {e}")
                print("Exit the program.")
            break

        else:
            print("Wrong choice. Please try again.")




if __name__ == "__main__":
    main_menu()



