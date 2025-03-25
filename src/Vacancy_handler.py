import json
from abc import ABC, abstractmethod

class VacancyHandler(ABC):
    @abstractmethod
    def add_vacancy(self,vacancy):
        """Добавить вакансию в файл."""
        pass

    @abstractmethod
    def get_vacancies(self,criteria):
        """Получить вакансии из файла по указанным критериям."""
        pass

    @abstractmethod
    def delete_vacancy(self, title):
        """Удалить вакансию по названию."""
        pass


class JSONFileHandler(VacancyHandler):
    def __init__(self, filename='vacancies.json'):
        self.filename = filename

    def add_vacancy(self, vacancy):
        """Добавить вакансию в JSON-файл."""
        with open(self.filename, 'a', encoding='utf-8') as f:
            f.write(json.dumps(vacancy.to_dict(), ensure_ascii=False) + '\n')

    def get_vacancies(self, criteria):
        """Получить вакансии из файла по указанным критериям."""
        filtered_vacancies = []
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                for line in file:
                    if line.strip():  # Проверяем, что строка не пустая
                        data = json.loads(line)
                        if criteria.lower() in data.get('name', '').lower():
                            filtered_vacancies.append(data)
        except FileNotFoundError:
            print(f"Файл {self.filename} не найден.")
        except json.JSONDecodeError as e:
            print(f"Ошибка декодирования JSON: {e}")

        return filtered_vacancies  # Возвращаем отфильтрованные вакансии

    def delete_vacancy(self, vacancy_name):
        """Удалить вакансию по имени."""
        vacancies_found = False
        vacancies_to_keep = []

        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                for line in file:
                    if line.strip():  # Проверяем, что строка не пустая
                        data = json.loads(line)
                        if data.get('name') == vacancy_name:
                            vacancies_found = True  # Вакансия найдена, не добавляем её в новый список
                        else:
                            vacancies_to_keep.append(data)  # Сохраняем вакансию, если она не совпадает

        except FileNotFoundError:
            print(f"Файл {self.filename} не найден.")
        except json.JSONDecodeError as e:
            print(f"Ошибка декодирования JSON: {e}")

        # Если вакансия не найдена, ничего не делаем
        if not vacancies_found:
            return

        # Если вакансия была найдена, перезаписываем файл
        with open(self.filename, 'w', encoding='utf-8') as file:
            for vacancy in vacancies_to_keep:
                file.write(json.dumps(vacancy) + '\n')
