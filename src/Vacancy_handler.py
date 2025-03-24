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
        with open(self.filename, 'a', encoding='utf-8') as file:
            json.dump(vacancy, file)
            file.write('\n')  # Записываем каждую вакансию на новой строке

    def get_vacancies(self, criteria):
        """Получить вакансии из файла по указанным критериям."""
        vacancies = []
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                for line in file:
                    if line.strip():  # Проверяем, что строка не пустая
                        data = json.loads(line)
                        if criteria.lower() in data.get('name', '').lower():
                            vacancies.append(data)
        except FileNotFoundError:
            print(f"Файл {self.filename} не найден.")
        except json.JSONDecodeError as e:
            print(f"Ошибка декодирования JSON: {e}")

        return []

    def delete_vacancy(self, title):
        """Удалить вакансию по названию."""
        vacancies = []
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                vacancies = [json.loads(line) for line in file if line.strip()]

            # Фильтруем вакансии, исключая ту, которую нужно удалить
            vacancies = [v for v in vacancies if v.get('title') != title]

            # Записываем оставшиеся вакансии обратно в файл
            with open(self.filename, 'w', encoding='utf-8') as file:
                for vacancy in vacancies:
                    json.dump(vacancy, file)
                    file.write('\n')

        except FileNotFoundError:
            print(f"Файл {self.filename} не найден.")
        except json.JSONDecodeError as e:
            print(f"Ошибка декодирования JSON: {e}")

# Пример использования
if __name__ == "__main__":
    handler = JSONFileHandler()

    # Добавление вакансий
    handler.add_vacancy({'name': 'Python Developer', 'salary': 100000, 'url':"https://api.hh.ru/vacancies"})
    handler.add_vacancy({'name': 'Data Scientist', 'salary': 120000, 'url':"https://api.hh.ru/vacancies"})

    # Получение вакансий
    vacancies = handler.get_vacancies('Python')
    print("Найденные вакансии:", vacancies)

    # Удаление вакансии
    handler.delete_vacancy('Python Developer')
    vacancies_after_deletion = handler.get_vacancies('Python')
    print("Вакансии после удаления:", vacancies_after_deletion)