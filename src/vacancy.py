from typing import Any


class Vacancy:
    """
    Class for work with vacancy.
    In class described dander methods for print and compare vacancies, add new vacancy and validation of salary
    """

    __slot__ = ("name", "link", "salary", "description")

    name: str
    link: str
    salary: dict
    description: str

    def __init__(self, name: str, link: str, salary: dict, description: str) -> None:
        self.__name = name
        self.__link = link
        self.__salary = self.__salary_validation(salary)
        self.__description = description

    def __str__(self) -> str:
        return (f"Название: {self.__name}, ссылка: {self.__link}, зарплата: {self.__salary["from"]} - "
                f"{self.__salary["to"]}, описание: {self.__description}")

    def __get_salary_for_compare(self, compare_obj: Any) -> Any:
        """
        Static method to get integer from dict of salary or integer
        """

        if isinstance(compare_obj, Vacancy):
            item_salary = compare_obj.__salary["to"] if compare_obj.__salary["to"] else compare_obj.__salary["from"]
            return item_salary
        elif isinstance(compare_obj, int):
            return compare_obj
        else:
            return 0

    # Dander methods for compare two vacations by salary and compare integer with vacation salary
    def __lt__(self, other: Any) -> bool:
        if self.__get_salary_for_compare(self) < self.__get_salary_for_compare(other):
            return True
        else:
            return False

    def __le__(self, other: Any) -> bool:
        if self.__get_salary_for_compare(self) <= self.__get_salary_for_compare(other):
            return True
        else:
            return False

    def __gt__(self, other: Any) -> bool:
        if self.__get_salary_for_compare(self) > self.__get_salary_for_compare(other):
            return True
        else:
            return False

    def __ge__(self, other: Any) -> bool:
        if self.__get_salary_for_compare(self) >= self.__get_salary_for_compare(other):
            return True
        else:
            return False

    @property
    def get_params_dict(self) -> dict:
        """
        Getter return dictionary of vacation parameters.
        Use for save vacation in files
        """

        return {
            "name": self.__name,
            "link": self.__link,
            "salary": {"from": self.__salary["from"], "to": self.__salary["to"]},
            "description": self.__description,
        }

    @classmethod
    def new_vacancy(cls, vacancy_dict: dict) -> Any:
        """
        Class method to create new vacation object by dictionary params
        User can create new vacation by hh.ru Api or by file data, and dicts of params have different keys

        for description parameter we get key "snippet" and "requirement" if we create vacation from hh date and
        key "description" if we create vacancy from data file

        :param vacancy_dict: dict of vacation params
        :return: new vacation object
        """

        name = vacancy_dict.get("name")
        link = (
            vacancy_dict.get("alternate_url") if vacancy_dict.get("alternate_url") else vacancy_dict.get("link")
        )  # link of vacation page on hh.ru
        salary = vacancy_dict.get("salary")
        try:
            description = vacancy_dict.get("snippet").get("requirement")
        except AttributeError:
            description = vacancy_dict.get("description")

        return cls(name, link, salary, description)

    def __salary_validation(self, salary_data: dict) -> dict:
        """
        Method of validation salary data in dict {"from": - , "to": - }, if user create vacation without salary,
        vacation salary = 0

        :param salary_data: dict of min and max salary and another params
        :return: salary_data: dict of min and max salary
        """

        salary_dict = {"from": 0, "to": 0}
        if salary_data:
            salary_dict["from"] = salary_data.get("from") if salary_data.get("from") else 0
            salary_dict["to"] = salary_data.get("to") if salary_data.get("to") else 0
        return salary_dict

    def get_dict(self) -> dict:
        """
        Method to return dictionary of vacation parameters.
        Use for save vacation in files
        """

        return {
            "name": self.__name,
            "link": self.__link,
            "salary": {"from": self.__salary["from"], "to": self.__salary["to"]},
            "description": self.__description,
        }
