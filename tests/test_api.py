from unittest.mock import patch, Mock

from src.api import HeadHunterAPI

def test_connect_success():
    api = HeadHunterAPI(file_worker=None)  # Передайте нужный объект file_worker, если требуется
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        response = api.connect()
        assert response.status_code == 200, "Ошибка: Метод connect не вернул статус 200"
        mock_get.assert_called_once_with(api.base_url)

def test_connect_failure():
    api = HeadHunterAPI(file_worker=None)
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        try:
            api.connect()
            assert False, "Ошибка: Метод connect не вызвал исключение при статусе 404"
        except Exception as e:
            assert str(e) == "Ошибка подключения: 404", "Ошибка: Неверное сообщение об ошибке"

# Тест метода get_vacancies
def test_get_vacancies_success():
    api = HeadHunterAPI(file_worker=None)
    with patch('requests.get') as mock_get:
        # Имитация первого ответа с вакансиями
        mock_response_1 = Mock()
        mock_response_1.json.return_value = {
            'items': [{'id': 1, 'name': 'Вакансия 1'}, {'id': 2, 'name': 'Вакансия 2'}],
            'pages': 1
        }
        mock_response_1.status_code = 200
        mock_get.return_value = mock_response_1

        # Имитация второго ответа с пустым списком вакансий
        mock_response_2 = Mock()
        mock_response_2.json.return_value = {'items': []}
        mock_response_2.status_code = 200
        mock_get.side_effect = [mock_response_1, mock_response_2]

        vacancies = api.get_vacancies("Программист")
        assert len(vacancies) == 2, "Ошибка: Метод get_vacancies не вернул ожидаемое количество вакансий"
        assert vacancies[0]['id'] == 1, "Ошибка: Неверная вакансия в результате"

def test_get_vacancies_no_items():
    api = HeadHunterAPI(file_worker=None)
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {}  # Отсутствие ключа 'items'
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        vacancies = api.get_vacancies("Программист")
        assert vacancies == [], "Ошибка: Метод get_vacancies не вернул пустой список при отсутствии вакансий"
