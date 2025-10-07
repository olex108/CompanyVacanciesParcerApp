from abc import ABC, abstractmethod
from typing import Any

import requests

from src.vacancy import Vacancy


class BaseApiService(ABC):
    """Abstract class to work with API"""

    @abstractmethod
    def _get_api_response(self, url: str, search_params: dict) -> list[dict]:
        """Method to connection and get response by API"""

    @abstractmethod
    def get_vacancies(
        self, search_word: str,
            search_area_name: str | None = None,
            vacancies_count: int = 20
    ):
        """Method to get vacancies by search parameters"""


class HeadHunterApiService(BaseApiService):
    """
    Class for work with site hh.ru
    """

    url_vacancies: str = "https://api.hh.ru/vacancies"
    url_areas: str = "https://api.hh.ru/areas"
    vacancies: list[Vacancy]

    def __init__(self) -> None:
        self.__vacancies: list = []

    @property
    def vacancies(self) -> list[str]:
        return [str(vacancy) for vacancy in self.__vacancies]

    def __get_area_id(self, area_name: str) -> int | None:
        """
        Method for search area id from Api HeadHunter request by area name.
        Ger response from method _get_api_response by url: "https://api.hh.ru/areas"
        If response status code valid start recurs search in lists of data with function recurs_search_by_name()

        :param area_name: name of city or region
        :return: area id or None if area name is not in list
        """

        areas_data_list = self._get_api_response(self.url_areas, {})

        return self.recurs_search_by_name(area_name, areas_data_list)

    def recurs_search_by_name(self, keyword: str, data_list: list[dict]) -> str | None:
        """
        Method to search id of area by area name in data list

        :param keyword: searched word
        :param data_list: list of data
        :return: search_id: id of area
        """

        if keyword is None or len(data_list) == 0:
            return None

        else:
            for item in data_list:
                if item.get("name") == keyword:
                    return item.get("id")
                else:
                    if len(item.get("areas")) > 0:
                        search_id = self.recurs_search_by_name(keyword, item.get("areas"))
                        if search_id is not None:
                            return search_id
            return None

    def _get_api_response(self, url: str, search_params: dict) -> Any:
        """
        Method for connection to HeadHunter API

        :param url: url address of API
        :param search_params: dict of search params for API
        :return: data: response of API
        """

        response = requests.get(url, params=search_params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Connection Error (HeadHunter Api)")

    def get_vacancies(
        self, search_word: str, search_area_name: str | None = None, vacancies_count: int = 20
    ) -> list[Vacancy]:
        """
        Method to get vacancies by search parameters.
        Method call method _get_api_response to get vacancies data

        :param search_word: string to search in vacation
        :param search_area_name: name of city or region
        :param vacancies_count: count of vacation
        :return: data_json: list of vacations
        """

        search_params = {"text": search_word, "area": None, "page": 0, "per_page": vacancies_count}

        # Add area param for search vacations if user add area name
        if search_area_name:
            search_params["area"] = self.__get_area_id(search_area_name)

        # Circle requests with params of pages
        page_counter = 0
        per_page_num = vacancies_count

        while True:
            if page_counter <= vacancies_count:
                search_params["page"] = page_counter

                if per_page_num <= 100:
                    search_params["per_page"] = per_page_num
                else:
                    search_params["per_page"] = 100
                    per_page_num -= 100

                vacancies_list = self._get_api_response(self.url_vacancies, search_params)["items"]
                self.__vacancies.extend([Vacancy.new_vacancy(vacancy) for vacancy in vacancies_list])

                page_counter += 100

            else:
                break

        return self.__vacancies
