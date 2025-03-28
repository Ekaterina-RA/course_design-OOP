import json
from src.api import HeadHunterAPI
from src.utils import filter_vacancies
from src.vacancies import Vacancy
from src.Vacancy_handler import JSONFileHandler


def main():
    api = HeadHunterAPI()
    file_manager = JSONFileHandler('vacancies.json')  # Убедитесь, что вы передаете имя файла

    while True:
        print("\n1. Получить вакансии по запросу")
        print("2. Получить минимальную зарплату по вакансии")
        print("3. Удалить вакансию по названию")
        print("4. Выход")
        choice = input("Выберите действие: ")

        if choice == '1':
            keyword = input('Введите ключевое слово для поиска вакансий: ')
            vacancies_data = api.get_vacancies(keyword)
            vacancies = []
            for item in vacancies_data:
                vacancy = Vacancy(
                    id=item['id'],
                    title=item['name'],
                    salary=item['salary']['from'] if item['salary'] else 0,
                    url=item['alternate_url']
                )
                vacancies.append(vacancy)

            # Сохраняем вакансии в файл
            file_manager.save_data([{
                'id': vacancy.id,
                'title': vacancy.title,
                'salary': vacancy.salary,
                'url': vacancy.url
            } for vacancy in vacancies])
            print(f"Добавлена вакансия: {vacancy.title}")

        elif choice == '2':
            min_salary = float(input('Введите минимальную зарплату: '))
            filtered_vacancies = filter_vacancies([{
                'id': vacancy.id,
                'title': vacancy.title,
                'salary': vacancy.salary,
                'url': vacancy.url
            } for vacancy in vacancies], min_salary)
            print('Отфильтрованные вакансии: ')
            for vacancy in filtered_vacancies:
                print(vacancy)

        elif choice == '3':
            title = input("Введите название вакансии для удаления: ")
            file_manager.delete_vacancy(title)
            print(f"Вакансия '{title}' удалена.")

        elif choice == '4':
            break

        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    main()
