import json
from src.api import HeadHunterAPI
from src.vacancies import Vacancy
from src.Vacancy_handler import JSONFileHandler


def main():
    file_handler = JSONFileHandler()
    api = HeadHunterAPI(file_worker=file_handler)

    while True:
        print("\n1. Получить вакансии по запросу")
        print("2. Получить топ вакансий по зарплате")
        print("3. Получить вакансии с ключевым словом в описании")
        print("4. Удалить вакансию по названию")
        print("5. Выход")
        choice = input("Выберите действие: ")

        if choice == '1':
            keyword = input("Введите поисковый запрос: ")
            vacancies_data = api.get_vacancies(keyword)
            for v in vacancies_data:
                # Проверяем наличие ключа 'salary' и его значение
                salary_from = v.get('salary', {}).get('from')  # Используем get для безопасного доступа
                if salary_from is None:
                    salary_from = 0  # Или любое другое значение по умолчанию

                vacancy = Vacancy(v['name'], v['alternate_url'], salary_from, v['snippet']['requirement'])
                file_handler.add_vacancy(vacancy)
                print(f"Добавлена вакансия: {vacancy.title}")

        elif choice == '2':
            vacancy_quantity = int(input("Введите количество вакансий для отображения: "))
            with open('vacancies.json', 'r') as file:
                vacancies = [json.loads(line) for line in file]
                sorted_vacancies = sorted(vacancies, key=lambda x: x.get('salary', {}).get('from', 0), reverse=True)[
                                   :vacancy_quantity]
                for v in sorted_vacancies:
                    print(
                        f"Title: {v['title']}, Salary: {v.get('salary', {}).get('from', 'Не указана')}, URL: {v['url']}")

        elif choice == '3':
            keyword = input("Введите ключевое слово для поиска в описании: ")
            vacancies = file_handler.get_vacancies(keyword)
            for v in vacancies:
                print(f"Title: {v['title']}, URL: {v['url']}")

        elif choice == '4':
            title = input("Введите название вакансии для удаления: ")
            file_handler.delete_vacancy(title)
            print(f"Вакансия '{title}' удалена.")

        elif choice == '5':
            break

        else:
            print("Упс, выбор некорректный, попробуйте снова.")


if __name__ == "__main__":
    main()