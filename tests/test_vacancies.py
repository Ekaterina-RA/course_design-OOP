from src import vacancies
from src.vacancies import Vacancy


def test_initialization():
    vacancy_1 = Vacancy("Программист", 1000, "http://example.com/vacancy1", "Описание вакансии 1")
    assert vacancy_1.title == "Программист", "Ошибка: Заголовок вакансии не совпадает"
    assert vacancy_1.salary == 1000, "Ошибка: Зарплата вакансии не совпадает"
    assert vacancy_1.url == "http://example.com/vacancy1", "Ошибка: URL вакансии не совпадает"
    assert vacancy_1.description == "Описание вакансии 1", "Ошибка: Описание вакансии не совпадает"

def test_salary_validate():
    try:
        Vacancy("Тестовая вакансия", -500, "http://example.com/vacancy3", "Описание вакансии 3")
    except ValueError as e:
        assert str(e) == "Заработная плата не может быть отрицательной", "Ошибка: Неверное сообщение об ошибке"

def test_set_salary():
    vacancies.salary = 1500
    assert vacancies.salary == 1500, "Ошибка: Зарплата не была обновлена"


def test_salary_comparison():
    vacancy1 = Vacancy("Системный администратор", 1200, "http://example.com/vacancy2", "Описание вакансии 1")
    vacancy2 = Vacancy("Системный администратор", 1400, "http://example.com/vacancy2", "Описание вакансии 2")
    assert vacancy1 < vacancy2, "Ошибка: vacancy1 должна быть меньше vacancy2"
    assert vacancy2 > vacancy1, "Ошибка: vacancy2 должна быть больше vacancy1"

