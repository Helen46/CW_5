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

    def get_all_vacancies(self):
        """
        получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        :return:
        """
        cur = self.conn.cursor()
        cur.execute("""
            SELECT c.name, v.name, v.salary_from, v.salary_to, v.url
            FROM vacancies as v
            JOIN companies as c ON v.company_id = c.id
        """)

        return cur.fetchall()

    def get_avg_salary(self):
        """
        получает среднюю зарплату по вакансиям
        :return:
        """
        cur = self.conn.cursor()
        cur.execute("""
            SELECT (AVG(DISTINCT v.salary_from) + AVG(DISTINCT v.salary_to)) / 2
            FROM vacancies as v
            WHERE v.salary_from > 0 AND v.salary_to > 0
        """)

        return cur.fetchall()

    def get_vacancies_with_higher_salary(self):
        """
        получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        :return:
        """
        cur = self.conn.cursor()
        cur.execute("""
            SELECT *
            FROM vacancies
            WHERE salary_from > (SELECT AVG(DISTINCT salary_from) FROM vacancies) or
            salary_to >(SELECT AVG(DISTINCT salary_to) FROM vacancies)
        """)

        return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """
        получает список всех вакансий, в названии которых содержатся переданные в метод слова
        :return:
        """
        cur = self.conn.cursor()
        cur.execute(f"""
            SELECT *
            FROM vacancies
            WHERE name LIKE '%{keyword}%'
        """)

        return cur.fetchall()
