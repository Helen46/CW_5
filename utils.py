from typing import Any

import psycopg2


def create_database(database_name: str, params: dict) -> None:
    """Создание базы данных и таблиц для сохранения данных о работадателях и ваканискиях"""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS companies(
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                city TEXT NOT NULL,
                website TEXT,
                description TEXT,
                open_vacancies INT
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancies(
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                company_id INT REFERENCES companies(id),
                salary_from INTEGER NULL,
                salary_to INTEGER NULL,
                currency TEXT,
                url TEXT NOT NULL
            )
        """)
    conn.commit()
    conn.close()


def save_data_to_database(data: list[dict[str, Any]], database_name: str, params: dict) -> None:
    """Сщхранение данных о работадателях и ваканискиях в базу данных"""
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for employer in data:
            employer_data = employer['employer']
            cur.execute(
                """
                INSERT INTO companies (name, city, website, description, open_vacancies)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """,
                (employer_data['name'], employer_data['area']['name'], employer_data['area']['url'],
                 employer_data['description'], employer_data['open_vacancies'])
            )
            id_ = cur.fetchone()[0]
            vacancies_data = employer['vacancies']
            for vacancy_data in vacancies_data:
                salary = vacancy_data.get("salary")
                salary_from = 0
                salary_to = 0
                salary_currency = None
                if salary:
                    salary_from = salary.get("from", 0) if salary.get("from") is not None else 0
                    salary_to = salary.get("to", 0) if salary.get("to") is not None else 0
                    salary_currency = salary.get("currency")
                cur.execute(
                    """
                    INSERT INTO vacancies (name, company_id, salary_from, salary_to, currency, url)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (vacancy_data['name'], id_, salary_from,
                     salary_to, salary_currency, vacancy_data['alternate_url'])
                )

        conn.commit()
        conn.close()
