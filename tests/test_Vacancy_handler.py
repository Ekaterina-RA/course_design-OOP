import json
from unittest.mock import mock_open, patch
from src.Vacancy_handler import JSONFileHandler

import json
from unittest.mock import mock_open, patch

from src.vacancies import Vacancy


def test_add_vacancy():
    filename = 'test_vacancies.json'
    handler = JSONFileHandler(filename)

    # Создаем объект Vacancy
    vacancy = Vacancy('Python Developer', 100000, 'https://api.hh.ru/vacancies', 'Описание вакансии')

    # Мокаем open
    m = mock_open()
    with patch('builtins.open', m):
        handler.add_vacancy(vacancy)

        # Проверяем, что файл открыт с правильными параметрами
        m.assert_called_once_with(filename, 'a', encoding='utf-8')

        # Проверяем, что метод write был вызван с правильными данными
        expected_data = json.dumps(vacancy.to_dict(), ensure_ascii=False) + '\n'
        write_call = m().write.call_args[0][0]  # Получаем аргумент, с которым был вызван write

        if write_call == expected_data:
            print("Test passed: Vacancy added correctly.")
        else:
            print("Test failed: Expected data does not match written data.")
            print(f"Expected: {expected_data}")
            print(f"Written: {write_call}")

# Тест для вакансии с пустой зарплатой
def test_add_vacancy_empty_salary():
    filename = 'test_vacancies.json'
    handler = JSONFileHandler(filename)

    # Создаем объект Vacancy с пустой зарплатой
    vacancy = Vacancy('Python Developer', None, 'https://api.hh.ru/vacancies', 'Описание вакансии')

    # Мокаем open
    m = mock_open()
    with patch('builtins.open', m):
        handler.add_vacancy(vacancy)

        # Проверяем, что файл открыт с правильными параметрами
        m.assert_called_once_with(filename, 'a', encoding='utf-8')

        # Проверяем, что метод write был вызван с правильными данными
        expected_data = json.dumps(vacancy.to_dict(), ensure_ascii=False) + '\n'
        write_call = m().write.call_args[0][0]

        if write_call == expected_data:
            print("Test passed: Vacancy with empty salary added correctly.")
        else:
            print("Test failed: Expected data does not match written data.")
            print(f"Expected: {expected_data}")
            print(f"Written: {write_call}")

# Тест для некорректного объекта
def test_add_vacancy_invalid_object():
    filename = 'test_vacancies.json'
    handler = JSONFileHandler(filename)

    try:
        handler.add_vacancy("Некорректный объект")
        print("Test failed: No exception raised for invalid object.")
    except AttributeError:
        print("Test passed: Correctly raised exception for invalid object.")

# Запуск тестов
test_add_vacancy()
test_add_vacancy_empty_salary()
test_add_vacancy_invalid_object()
def test_get_vacancies_success():
    vacancies_data = [
        {'name': 'Python Developer', 'salary': 100000, 'url': "https://api.hh.ru/vacancies"},
        {'name': 'Data Scientist', 'salary': 120000, 'url': "https://api.hh.ru/vacancies"}
    ]
    m = mock_open(read_data='\n'.join(json.dumps(v) for v in vacancies_data) + '\n')
    with patch('builtins.open', m):
        handler = JSONFileHandler('test_vacancies.json')
        result = handler.get_vacancies('Python')

        # Проверяем, что вернулась одна вакансия
        assert len(result) == 1
        assert result[0]['name'] == 'Python Developer'

def test_get_vacancies_no_results():
    m = mock_open(read_data='')
    with patch('builtins.open', m):
        handler = JSONFileHandler('test_vacancies.json')
        result = handler.get_vacancies('Python')
        assert result == [], "Ошибка: Должен быть возвращен пустой список"

def delete_vacancy(self, vacancy_name):
    with open(self.filename, 'r', encoding='utf-8') as file:
        vacancies = [json.loads(line) for line in file if line.strip()]

    vacancies = [v for v in vacancies if v['name'] != vacancy_name]

    with open(self.filename, 'w', encoding='utf-8') as file:
        for vacancy in vacancies:
            json.dump(vacancy, file)
            file.write('\n')

def test_delete_vacancy_not_found():
    vacancies_data = [
        {'name': 'Python Developer', 'salary': 100000, 'url': "https://api.hh.ru/vacancies"}
    ]
    m = mock_open(read_data='\n'.join(json.dumps(v) for v in vacancies_data) + '\n')
    with patch('builtins.open', m):
        handler = JSONFileHandler('test_vacancies.json')
        handler.delete_vacancy('Data Scientist')  # Удаляем несуществующую вакансию
        m().write.assert_not_called()  # Проверяем, что метод write не был вызван
