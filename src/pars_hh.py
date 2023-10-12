import json

import requests


class HHapi:
    """
    Класс получения вакансий с hh.ru
    """
    def __init__(self, answer, cur):
        self.cur = cur
        self.answer = answer

    def get_vacancies(self, page=0):
        """
        Получаем вакансии по заданному слову в init
        :param page: страницы поиска
        :return: словарь списков вакансий
        """
        params = {"text": self.answer, 'page': page}
        req = requests.get('https://api.hh.ru/vacancies/', params=params)
        data = req.content.decode()
        req.close()
        return data

    def vacancy_on_sql(self):
        """
        Пробегаем 20 страниц поиска вакансийб загружая в sql
        """
        for page in range(0, 20):
            vacant = json.loads(self.get_vacancies(page))
            if (vacant['pages'] - page) <= 1:
                break
            for vacancy in vacant['items']:
                name = vacancy['name']
                employer = vacancy['employer']['name']
                if vacancy['salary']:
                    salary = vacancy['salary']['from']
                else:
                    salary = 0
                requirements = vacancy['snippet']['requirement']
                responsibility = vacancy['snippet']['responsibility']
                url = vacancy['alternate_url']
                self.cur.execute("INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s)",
                                 (name, employer, salary, requirements, responsibility, url))

    @staticmethod
    def favorite_employer(list_id):
        """
        Печать вакансий по любимым компаниям
        :param list_id:  Список любимых коммпаний
        """
        for ident in list_id:
            params = {"employer_id": ident}
            req = requests.get('https://api.hh.ru/vacancies/', params=params)
            data = req.content.decode()
            req.close()
            vacant = json.loads(data)
            print(vacant['items'][0]['name'], vacant['items'][0]['employer']['name'],
                  vacant['items'][0]['salary']['from'], vacant['items'][0]['alternate_url'])
