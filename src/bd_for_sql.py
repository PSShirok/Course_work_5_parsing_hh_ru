import psycopg2

class DBManager:
    connect_database = psycopg2.connect(database="seach_vacancies", user="postgres", password="159763")



    def __init__(self):
        self.cur = self.connect_database.cursor()
        self.quantity = self.cur.execute(f"""select count(*) FROM vacancies""")
        self.rows = self.cur.fetchone()

    def get_companies_and_vacancies_count(self, limit=10):
        """получает список всех компаний и количество вакансий у каждой компании."""
        self.cur.execute(f"""select employer, count(*) as кол_во from vacancies
        GROUP BY employer ORDER BY кол_во DESC LIMIT {limit}""")
        return self.cur.fetchall()

    def get_all_vacancies(self):
       """ получает список всех вакансий с указанием названия компании,
       названия вакансии и зарплаты и ссылки на вакансию."""
       self.cur.execute(f"""select employer, vacancy, salary, url FROM vacancies""")
       return self.cur.fetchall()

    def get_avg_salary(self):
        """ получает среднюю зарплату по вакансиям."""
        self.cur.execute(f"""select avg(salary)  FROM vacancies 
                          where salary > 0""")
        return self.cur.fetchone()

    def get_vacancies_with_higher_salary():
        """получает список всех вакансий, у которых
        зарплата выше средней по всем вакансиям."""
        pass

    def get_vacancies_with_keyword():
        """получает список всех вакансий, в названии
        которых содержатся переданные в метод слова, например python."""
        pass
