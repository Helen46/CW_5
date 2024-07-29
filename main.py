from classes.db_manager import DBManager
from classes.hh_api import HH
from config import config
from settings import EMPLOYERS_IDS
from utils import create_database, save_data_to_database


def main():

    params = config()
    hh = HH(EMPLOYERS_IDS)
    data = hh.get_hh_employer_data()
    create_database("hh", params)
    db = DBManager("hh", **params)
    save_data_to_database(data, "hh", params)

    attempt = 0
    while attempt < 1:

        user_answer = int(input("Если желаете узнать информацию о всех работадателях "
                                "и колличестве их вакансий введите 1, если нет - введите 2:\n"))
        if user_answer == 1:
            print(db.get_companies_and_vacancies_count())
            attempt += 1
        elif user_answer == 2:
            attempt += 1
        else:
            print("Вы ввели не правильный код")
            continue

    user_answer = int(input("Если желаете узнать информацию о всех вакансиях "
                            "введите 1, если нет - введите 2:\n"))

    while attempt < 2:
        if user_answer == 1:
            print(db.get_all_vacancies())
            attempt += 1
        elif user_answer == 2:
            attempt += 1
        else:
            print("Вы ввели не правильный код")
            continue

    user_answer = int(input("Если желаете узнать среднюю зарплату по всем вакансиям "
                            "введите 1, если нет - введите 2:\n"))

    while attempt < 3:
        if user_answer == 1:
            print(db.get_avg_salary())
            attempt += 1
        elif user_answer == 2:
            attempt += 1
        else:
            print("Вы ввели не правильный код")
            continue

    user_answer = int(input("Если желаете узнать информацию о вакансиях с зарплатой выше средней "
                            "введите 1, если нет - введите 2:\n"))

    while attempt < 4:
        if user_answer == 1:
            print(db.get_vacancies_with_higher_salary())
            attempt += 1
        elif user_answer == 2:
            attempt += 1
        else:
            print("Вы ввели не правильный код")
            continue

        user_answer = int(input("Если желаете узнать информацию о вакансиях с заданым словом "
                                "введите 1, если нет - введите 2:\n"))

    while attempt < 5:
        if user_answer == 1:
            query = input("Ведите слово для поиска\n")
            print(db.get_vacancies_with_keyword(query))
            print("Спасибо за обращение, ждем вас снова")
            attempt += 1
        elif user_answer == 2:
            print("Спасибо за обращение, ждем вас снова")
            attempt += 1
        else:
            print("Вы ввели не правильный код")
            continue


if __name__ == '__main__':
    main()
