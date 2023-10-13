class DBManager:

    def __init__(self, cur):
        self.cur = cur
        self.quantity = self.cur.execute(f"""select count(*) FROM vacancies""")
        self.rows = self.cur.fetchone()

    def get_companies_and_vacancies_count(self):
        """получает список всех компаний и количество вакансий у каждой компании."""
        self.cur.execute(f"""select employer, count(*) as кол_во from vacancies
        GROUP BY employer ORDER BY кол_во DESC""")
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
        return self.cur.fetchall()

    def print_vacancy(self, user_response, parsing):
        """
        Вывод вакансий
        :param parsing: получает список вакансий по любимым компаниям
        :param user_response: выбор показа вакансий
        """

        if user_response == 1:
            return parsing.favorite_employer([10356459, 10321757, 4938750, 2467312, 9901773,
                                              9295279, 5347571, 4112759, 833298, 1583540])
        elif user_response == 5:
            key_word = input("Что найти в названии вакансии?\n")
            return [print(row) for row in self.get_vacancies_with_keyword(key_word)]
        else:
            show_vacancies = {2: self.get_companies_and_vacancies_count(),
                              3: self.get_all_vacancies(),
                              4: self.get_vacancies_with_higher_salary()}
            return [print(row) for row in show_vacancies[user_response]]
