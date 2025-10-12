from src.file_handler import JSONFileHandler
from src.selection import add_company
from config import config

from src.database import DatabaseHandler, DBManager


def main():
    """
    Function start work of user, select operation with files or hh.ru
    """

    # Create database and tables
    database_params = config()
    DatabaseHandler.create_database(**database_params)
    database = DatabaseHandler(**database_params)
    database.create_tables()

    # Fill user companies list by base companies list
    base_company_json_file = JSONFileHandler("base_companies_list.json")
    user_company_json_file = JSONFileHandler("user_companies_list.json")

    base_company_list = base_company_json_file.get_data()
    user_company_indexes_list = [index for index in range(0, len(user_company_json_file.get_data()))]
    user_company_json_file.del_data(user_company_indexes_list)
    user_company_json_file.save_data(base_company_list)

    while True:
        # Get list of companies from json_file
        companies_list = user_company_json_file.get_data()
        print(f"Список из {len(companies_list)} компаний для получения вакансий:")
        [print(company) for company in companies_list]

        user_selection = input("""
            1. Заполнить базу данных компаниями и вакансиями
            2. Добавить компанию
        Выбор: \n""")

        if user_selection == "1":
            # Fill tables
            database.clear_tables()
            database.fill_companies_vacancies_tables(companies_list)
            break

        elif user_selection == "2":
            # Add company in file
            add_company()

        else:
            print("Неверный ввод")

    while True:
        database_manager = DBManager(**database_params)
        print("Операции с базой данных:")

        user_selection = input("""
            1. Получить список всех компаний и количество вакансий у каждой компании
            2. Получить список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки
            3. Получить среднюю зарплату по вакансиям
            4. Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям
            5. Получить список вакансий, по ключевому 
            q. Выход из программы
        Выбор: \n""")

        if user_selection == "1":
            [print(*item) for item in database_manager.get_companies_and_vacancies_count()]
        elif user_selection == "2":
            [print(*item) for item in database_manager.get_all_vacancies()]
        elif user_selection == "3":
            print(database_manager.get_avg_salary())
        elif user_selection == "4":
            [print(*item) for item in database_manager.get_vacancies_with_higher_salary()]
        elif user_selection == "5":
            search_word = input("Слово дла поиска:")
            [print(*item) for item in database_manager.get_vacancies_with_keyword(search_word=search_word)]
        elif user_selection == "q":
            break
        else:
            print("Неверный ввод")


if __name__ == "__main__":
    main()
