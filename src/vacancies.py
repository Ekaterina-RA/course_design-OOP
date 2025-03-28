class Vacancy:
    __slots__ = ("_id", "_title", "_url", "_salary")

    def __init__(self, id: str, title: str, salary: float, url: str):
        self._id = id
        self._title = title
        self._salary = salary
        self._url = url

    def __lt__(self, other):
        return self.salary < other.salary

    def __repr__(self):
        return f"Vacancy(id={self._id},title={self._title},salary={self._salary},url={self._url})"

    @property
    def id(self):
        return self._id

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
