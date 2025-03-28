from unittest.mock import Mock, patch

from src.api import HeadHunterAPI


def test_connect_failure():
    api = HeadHunterAPI()

    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        try:
            api.connect()
            assert False, "Ожидалось исключение при статусе 404"
        except Exception as e:
            assert str(e) == "Ошибка подключения: 404"


# Тест для метода get_vacancies
def test_get_vacancies_success():
    api = HeadHunterAPI()

    with patch("requests.get") as mock_get:
        # Подготовка ответа API
        mock_response = Mock()
        mock_response.json.return_value = {
            "items": [{"id": 1, "name": "Вакансия 1"}, {"id": 2, "name": "Вакансия 2"}],
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        vacancies = api.get_vacancies("разработчик")
        assert len(vacancies) == 2, "Ошибка: Должно быть 2 вакансии"
        assert (
            vacancies[0]["name"] == "Вакансия 1"
        ), "Ошибка: Неверное имя первой вакансии"
        assert (
            vacancies[1]["name"] == "Вакансия 2"
        ), "Ошибка: Неверное имя второй вакансии"
        mock_get.assert_called()  # Проверяем, что get был вызван


def test_get_vacancies_no_items():
    api = HeadHunterAPI()

    with patch("requests.get") as mock_get:
        # Подготовка ответа API без вакансий
        mock_response = Mock()
        mock_response.json.return_value = {
            "items": [],
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        vacancies = api.get_vacancies("разработчик")
        assert len(vacancies) == 0, "Ошибка: Должно быть 0 вакансий"
        mock_get.assert_called()  # Проверяем, что get был вызван


def test_get_vacancies_missing_items_key():
    api = HeadHunterAPI()

    with patch("requests.get") as mock_get:
        # Подготовка ответа API без ключа 'items'
        mock_response = Mock()
        mock_response.json.return_value = {
            "other_key": [],
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        vacancies = api.get_vacancies("разработчик")
        assert len(vacancies) == 0, "Ошибка: Должно быть 0 вакансий"
        mock_get.assert_called()  # Проверяем, что get был вызван
