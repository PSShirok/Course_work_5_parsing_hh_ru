import json

from src.bd_for_sql import DBManager
import psycopg2

from src.pars_hh import get_vacancies

connect_database = psycopg2.connect(database="seach_vacancies", user="postgres", password="159763")

answer = input('Давай посмотрим кто готов взять тебя на работу?!\n'
      'Введи свой запрос, и, если тебя интересует определенный город, укажи его тоже. \n'
      'ПРИМЕР: python на дому, а я поищу тебе нормальных работодателей\n')

cur = connect_database.cursor()
cur.execute("TRUNCATE TABLE vacancies")

print('Ожидайте, ваш звонок очень важен для нас, сейчас я все загружу, и все расскажу, буквально 5 сек\n')

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
connect_database.commit()
vacant = DBManager()
limit = input(f"Я нашел тебе {vacant.rows[0]} вакансий, "
              f"твои последующие запросы буду выводить \n"
              f"ТОПом по 10 штук, если все ок нажми 'enter' "
              f"либо любое другое число до {vacant.rows[0]}\n")
if limit.isdigit():
    limit = limit
else:
    limit = 10


#print(vacant.get_companies_and_vacancies_count(limit))
#print(vacant.get_all_vacancies())


#print(int(vacant.get_avg_salary()[0]))


