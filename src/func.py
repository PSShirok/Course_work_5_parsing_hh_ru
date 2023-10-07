#
#
# """спросить"""
# from src.bd_for_sql import DBManager
#
#
# def limit(vacant):
#     limit_vacancy = input(f"Я напомню, в списке {vacant.rows[0]} вакансий\n"
#                           f"выведу тебе топ 10? ок?"
#                           f"Если норм, нажми 'enter',"
#                           f"Если нет напиши - сколько хочешь увидеть")
#     if limit_vacancy.isdigit():
#         limit_vacancy = limit_vacancy
#     else:
#         limit_vacancy = 10
#     return limit_vacancy
#
#
# def print_vacancy(user_response, limit=10):
#     """
#
#     :type vacant: object
#     """
#     show_vacancies = [vacant.get_companies_and_vacancies_count(limit),
#                       vacant.get_all_vacancies(limit),
#                       vacant.get_vacancies_with_higher_salary(),
#                       vacant.get_vacancies_with_keyword()]
#     return print(show_vacancies[user_response])
