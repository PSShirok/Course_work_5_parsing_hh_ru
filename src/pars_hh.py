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


def favorite_employer(list_id):
    for ident in list_id:
        params = {"employer_id": ident}
        req = requests.get('https://api.hh.ru/vacancies/', params=params)
        data = req.content.decode()
        req.close()
        vacant = json.loads(data)
        print(vacant['items'][0]['name'], vacant['items'][0]['employer']['name'],
              vacant['items'][0]['salary']['from'], vacant['items'][0]['alternate_url'])
