import requests


class HH:
    """
    Класс для работы с API HeadHunter
    """

    def __init__(self, url):
        self.url = url
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 100}
        self.data = []

    def get_hh_employer_data(self):
        """Получение данных о работадателях и ваканискиях с API HH"""
        for employer_id in self.url:
            employers = requests.get(url=employer_id)
            employers_data = employers.json()
            vacancies = requests.get(url=employers.json()['vacancies_url'])
            vacancies_data = vacancies.json()['items']

            self.data.append({
                'employer': employers_data,
                'vacancies': vacancies_data
            })
        return self.data
