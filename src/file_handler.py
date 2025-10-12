import json
import os
from abc import ABC, abstractmethod
from typing import Any

from src.vacancy import Vacancy


class FileHandler(ABC):
    """
    Abstract class for work with files, include save, get or del data from files
    """

    @abstractmethod
    def save_data(self, save_data: list) -> None:
        pass

    @abstractmethod
    def get_data(self) -> list:
        pass

    @abstractmethod
    def del_data(self, list_of_index: list[int]) -> None:
        pass


class JSONFileHandler(FileHandler):
    """
    Class for work with JSON files, with include save, get or del data.
    """

    file_name: str

    def __init__(self, file_name: str = "vacancies.json"):
        self.__file_name = file_name
        self.__path_to_file = os.path.join(os.path.abspath(__file__), os.pardir, os.pardir, "data", self.__file_name)

    def __verification_data(self, add_data: list[dict]) -> list[dict] | Any:
        """
        Method of verification vacancies(dictionary) data, if vacancy exist new vacancy will be not add.
        """

        try:
            with open(self.__path_to_file, "r", encoding="utf-8") as file:
                file_data = json.load(file)

            for item in add_data:
                if item not in [item_in_file for item_in_file in file_data]:
                    file_data.append(item)

            return file_data

        except FileNotFoundError:
            return add_data

    def save_data(self, save_data: list[dict]) -> None:
        """
        Method to save data in JSON file.
        For add data in file with data, call method __verification_data

        :param save_data: list of data
        """

        save_data_dicts = self.__verification_data(save_data)

        with open(self.__path_to_file, "w", encoding="utf-8") as file:
            json.dump(save_data_dicts, file, ensure_ascii=False, indent=4)

    def get_data(self) -> list[Vacancy] | list[Any]:
        """
        Method to get vacancies from JSON file

        :return data_json: list of vacancies from json
        """

        try:
            with open(self.__path_to_file, "r", encoding="utf-8") as file:
                data_json = json.load(file)
            return data_json
        except FileNotFoundError:
            print("Файл не найден")
            return []

    def del_data(self, list_of_index: list[int]) -> None:
        """
        Method to del vacancies from JSON file by indexes

        :param list_of_index: list of indexes for del from file
        """

        try:

            with open(self.__path_to_file, "r", encoding="utf-8") as file:
                file_data = json.load(file)

            for index in list_of_index[::-1]:
                del file_data[index]

            with open(self.__path_to_file, "w", encoding="utf-8") as file:
                json.dump(file_data, file, ensure_ascii=False, indent=4)

        except IndexError:
            print("Индекс выходит за рамки списка")

        except FileNotFoundError:
            print("Файл не найден")
