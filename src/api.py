from abc import ABC, abstractmethod
import requests
from config import JSON_PATH
from src import vacancies


class AbstractAPI(ABC):
    @abstractmethod
    def connect(self):
        """Абстрактный метод для проверки соединения"""
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str):
        """Абстрактный метод для получения вакансий"""
        pass

class HeadHunterAPI(AbstractAPI):
    """  Класс для работы с API HeadHunter"""
    def __init__(self, file_worker):
        self.base_url = "https://api.hh.ru/vacancies"
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 100}
        self.file_worker = file_worker
        self.vacancies = []
        super().__init__()


    def connect(self):
        # Проверяем доступность API
        response = requests.get(self.base_url)
        if response.status_code != 200:
            raise Exception(f"Ошибка подключения: {response.status_code}")
        return response

    def get_vacancies(self, keyword):
        self.params['text'] = keyword
        while True:
            response = requests.get(self.base_url, headers=self.headers, params=self.params)
            data = response.json()

            # Проверяем наличие ключа 'items' в ответе
            if 'items' not in data:
                print("Ключ 'items' отсутствует в ответе API.")
                break

            vacancies = data['items']
            if not vacancies:  # Если вакансий больше нет, выходим из цикла
                break

            self.vacancies.extend(vacancies)
            self.params['page'] += 1  # Переходим к следующей странице

        return self.vacancies
