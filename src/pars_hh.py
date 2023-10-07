import json

import requests


def get_vacancies(answer, page=0):
    params = {"text": answer, 'page': page}
    req = requests.get('https://api.hh.ru/vacancies/', params=params)
    data = req.content.decode()
    req.close()
    return data


def vacancy_on_sql(answer, cur):
    for page in range(0, 20):
        vacant = json.loads(get_vacancies(answer, page))
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
            cur.execute("INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s)",
                        (name, employer, salary, requirements, responsibility, url))
