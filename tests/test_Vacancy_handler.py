import json
from unittest.mock import mock_open, patch

from src.Vacancy_handler import JSONFileHandler


def test_load_data_success():
    mock_data = [{"name": "Vacancy 1"}, {"name": "Vacancy 2"}]
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
        handler = JSONFileHandler("test_vacancies.json")
        data = handler.load_data()
        assert data == mock_data, "Ошибка: Данные не загружены корректно"


def test_load_data_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        handler = JSONFileHandler("test_vacancies.json")
        data = handler.load_data()
        assert data == [], "Ошибка: Должен вернуть пустой список при отсутствии файла"


def test_get_vacancies_success():
    mock_data = [
        {"name": "Vacancy 1"},
        {"name": "Vacancy 2"},
        {"name": "Developer Vacancy"},
    ]
    with patch(
        "builtins.open",
        mock_open(read_data="\n".join(json.dumps(d) for d in mock_data)),
    ):
        handler = JSONFileHandler("test_vacancies.json")
        vacancies = handler.get_vacancies("developer")
        assert len(vacancies) == 1, "Ошибка: Должна быть одна вакансия"
        assert (
            vacancies[0]["name"] == "Developer Vacancy"
        ), "Ошибка: Неверное имя вакансии"


def test_get_vacancies_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        handler = JSONFileHandler("test_vacancies.json")
        vacancies = handler.get_vacancies("developer")
        assert (
            vacancies == []
        ), "Ошибка: Должен вернуть пустой список при отсутствии файла"
