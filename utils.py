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
