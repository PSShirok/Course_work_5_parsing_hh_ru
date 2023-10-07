from src.bd_for_sql import DBManager
import psycopg2

from src.pars_hh import vacancy_on_sql, favorite_employer

connect_database = psycopg2.connect(database="seach_vacancies", user="postgres", password="159763")
cur = connect_database.cursor()
cur.execute("TRUNCATE TABLE vacancies")

answer = input('Давай посмотрим кто готов взять тебя на работу?!\n'
               'Введи свой запрос, и, если тебя интересует определенный город, укажи его тоже. \n'
               'ПРИМЕР: python на дому, а я поищу тебе нормальных работодателей\n')
print('Ожидайте, ваш звонок очень важен для нас, сейчас я все загружу, и все расскажу, буквально 5 сек\n')

vacancy_on_sql(answer, cur)
vacant = DBManager(cur)
connect_database.commit()


def print_vacancy(user_response):
    """
    :param user_response: слово в нназвании вакансии
    """
    show_vacancies = {2: vacant.get_companies_and_vacancies_count(),
                      3: vacant.get_all_vacancies(),
                      4: vacant.get_vacancies_with_higher_salary()}
    return print(show_vacancies[user_response])


print(f"Я нашел тебе {vacant.rows[0]} вакансий,\n"
      f"Средняя зарплата равна {vacant.get_avg_salary()[0]}\n"
      f"давай их немного отсортируем, напиши нужный пункт\n")

show_vacancy = 0
while show_vacancy not in (1, 2, 3, 4, 5):
    show_vacancy = int(input(f"1. Твои любимые компании: 10 штук\n"
                             f"2. Вывести компании с количеством вакансий в каждой\n"
                             f"3. Показать все вакансии, компании, зарплату, ссылку\n"
                             f"4. Показать все вакансии с зарплатой вышесреднего\n"
                             f"5. Поиск по фразе в названии вакансии\n"))
    if show_vacancy not in [1, 2, 3, 4, 5]:
        print('Ошибочка вышла, выбери пункт снова')
        continue
    if show_vacancy == 5:
        key_word = input("Что найти в названии вакансии?\n")
        print(vacant.get_vacancies_with_keyword(key_word))
    if show_vacancy == 1:
        favorite_employer([10356459, 10321757, 4938750, 2467312, 9901773,
                           9295279, 5347571, 4112759, 833298, 1583540])
    if show_vacancy in [2, 3, 4]:
        print_vacancy(show_vacancy)
    user_key = input('Выбрать другой пункт?\n1. ДА\n2. НЕТ\n')
    if user_key == '1':
        show_vacancy = 0
    else:
        break


print("УСПЕХОВ")
cur.close()
connect_database.close()
