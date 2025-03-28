from abc import ABC, abstractmethod

import requests


class AbstractAPI(ABC):
    @abstractmethod
    def connect(self):
        """Абстрактный метод для проверки соединения"""
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str, per_page: int = 20):
        """Абстрактный метод для получения вакансий"""
        pass


class HeadHunterAPI(AbstractAPI):
    """Класс для работы с API HeadHunter"""

    def __init__(self):
        self.__base_url = "https://api.hh.ru/vacancies"

    def connect(self):
        response = requests.get(self.__base_url)
        if response.status_code != 200:
            raise Exception("Ошибка подключения: 404")
        return response

    def get_vacancies(self, keyword: str, per_page: int = 20):
        response = self.connect()
        params = {"text": keyword, "per_page": per_page}
        response = requests.get(self.__base_url, params=params)
        if response.status_code != 200:
            raise Exception("Failed to fetch vacancies")
        return response.json().get("items", [])
