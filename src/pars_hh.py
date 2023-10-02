import requests
import json


class Vacancy:
    def __init__(self, name, employer, salary, requirements, responsibility, url):
        self.name = name
        self.employer = employer
        self.salary = salary
        self.requirements = requirements
        self.responsibility = responsibility
        self.url = url

    def __dict__(self):
        """
        метод для добавления данных экземпляров класса в словарь
        """
        return{"name": self.name,
               "employer": self.employer,
               "salary": self.salary,
               "requirements": self.requirements,
               "responsibility": self.responsibility,
               "url": self.url}

    def __str__(self):
        return self.name

    @staticmethod
    def compare_salary():
        """
        метод для сортировки по зар.плате и вывода заданного
        пользователем коли-ва вакансий
        """
        with open('vacancy.json', 'r', encoding='utf-8') as outfile:
            vacancies_data = json.load(outfile)
            for vacancy in vacancies_data:
                if vacancy['salary'] is None:
                    vacancy['salary'] = 0
            new_list = sorted(vacancies_data, key=lambda d: d['salary'], reverse=True)
            return new_list


class Filework:

    def __init__(self):
        pass

    @staticmethod
    def add_vacancy(file):
        """
        метод для добавления вакнсий в файл
        """
        with open('vacancy.json', 'r', encoding='utf-8') as outfile:
            content = json.load(outfile)
        content.append(file.__dict__())
        with open('vacancy.json', 'w', encoding='utf-8') as outfile:
            json.dump(content, outfile, ensure_ascii=False, indent=6)

    @staticmethod
    def del_vacancy():
        """
        метод для удаления вакансий из файла
        """
        with open('vacancy.json', "w", encoding='utf-8') as outfile:
            content = []
            json.dump(content, outfile)


Filework.del_vacancy()


def get_vacancies(answer, page=0):
    params = {"text": answer, 'page': page}
    req = requests.get('https://api.hh.ru/vacancies/', params=params)
    data = req.content.decode()
    req.close()
    return data


for page in range(0, 20):
    vacant = json.loads(get_vacancies("python", page))
    get_vacancies("Python", page=page)
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
        vacancy_for_file = Vacancy(name, employer, salary, requirements, responsibility, url)
        Filework.add_vacancy(vacancy_for_file)
