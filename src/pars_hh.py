import requests
import json

class HeadHunterAPI():
    def get_vacancies(self, answer, page=1):
        params = {"text": answer}
        req = requests.get('https://api.hh.ru/vacancies/', params=params, page=page)
        data = req.content.decode()
        vacant = json.loads(data)
        return vacant