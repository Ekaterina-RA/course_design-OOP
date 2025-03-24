class Vacancy:
    __slots__ = ('title', 'salary', 'url', 'description')

    def __init__(self, title: str, salary: float, url: str, description: str):
        self.title = title
        self.salary = salary
        self.url = url
        self.description = description


    def __lt__(self, other):
        return self.salary < other.salary

    def __gt__(self, other):
        return self.salary > other.salary

    def validate_salary(self):
        if self.salary < 0:
            raise ValueError("Заработная плата не может быть отрицательной")