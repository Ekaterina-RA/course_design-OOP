class Vacancy:
    __slots__ = ('_title', '_salary', '_url', '_description')

    def __init__(self, title: str, salary: float, url: str, description: str):
        self._title = title
        self._salary = salary  # Вызовет валидацию
        self._url = url
        self._description = description

    @property
    def title(self):
        return self._title

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, value: float):
        if value is None:
            self._salary = 0  # Или можно использовать "Зарплата не указана"
        elif not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Заработная плата не может быть отрицательной")
        else:
            self._salary = value

    @property
    def url(self):
        return self._url

    @property
    def description(self):
        return self._description

    def to_dict(self):
        return {
            'title': self.title,
            'url': self.url,
            'salary': self.salary,
            'description': self.description
        }

    def __lt__(self, other):
        return self.salary < other.salary

    def __gt__(self, other):
        return self.salary > other.salary




