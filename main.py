import psycopg2


class DBManager:
    def __init__(self, dbname: str, host: str, user: str, password: str, port: int):
        self.conn = psycopg2.connect(dbname=dbname, host=host, user=user, password=password, port=port)

    def get_companies_and_vacancies_count(self):
        """
        получает список всех компаний и количество вакансийу каждой компании
        :return:
        """
        cur = self.conn.cursor()
        cur.execute("""
            SELECT c.name, COUNT(v.id)
            FROM companies as c
            LEFT JOIN vacancies as v ON c.id = v.company_id
            GROUP BY c.name
        """)

        return cur.fetchall()