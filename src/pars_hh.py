import requests

def get_vacancies(answer, page=0):
    params = {"text": answer, 'page': page}
    req = requests.get('https://api.hh.ru/vacancies/', params=params)
    data = req.content.decode()
    req.close()
    return data



