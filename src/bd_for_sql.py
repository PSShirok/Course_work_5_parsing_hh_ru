import psycopg2


class DBManager:
    #connect_database = psycopg2.connect(database="seach_vacancies", user="postgres", password="159763")

    def __init__(self, cur):
        self.cur = cur
        self.quantity = cur.execute(f"""select count(*) FROM vacancies""")
        self.rows = cur.fetchone()

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

    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых
        зарплата выше средней по всем вакансиям."""
        self.cur.execute(f"""select vacancy, salary, url  FROM vacancies 
        where salary > (select avg(salary) from vacancies 
        where salary >0)
        Order by salary desc""")
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, answer):
        """получает список всех вакансий, в названии
        которых содержатся переданные в метод слова, например python."""
        self.cur.execute(f"""SELECT vacancy, salary, url FROM vacancies 
        WHERE vacancy LIKE '%{answer}%'""")
        return self.cur.fetchone()
