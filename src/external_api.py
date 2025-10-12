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
        self, search_word: str, search_area_name: str | None = None, vacancies_count: int = 20
    ) -> list[Vacancy]:
        """Method to get vacancies by search parameters"""


class HeadHunterApiService(BaseApiService):
    """
    Class for work with site hh.ru
    """

    url_vacancies: str = "https://api.hh.ru/vacancies"
    url_areas: str = "https://api.hh.ru/areas"
    url_employers: str = "https://api.hh.ru/employers"
    vacancies: list[Vacancy]

    def __get_area_id(self, area_name: str) -> int | str | None:
        """
        Method for search area id from Api HeadHunter request by area name.
        Ger response from method _get_api_response by url: "https://api.hh.ru/areas"
        If response status code valid start recurs search in lists of data with function recurs_search_by_name()

        :param area_name: name of city or region
        :return: area id or None if area name is not in list
        """

        areas_data_list = self._get_api_response(self.url_areas, {})

        return self.__recurs_search_by_name(area_name, areas_data_list)

    def __recurs_search_by_name(self, keyword: str, data_list: list[dict]) -> str | None:
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
                        search_id = self.__recurs_search_by_name(keyword, item.get("areas"))
                        if search_id is not None:
                            return search_id
            return None

    def _get_api_response(self, url: str, search_params: dict | None) -> Any:
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
        self,
        search_word: str | None = None,
        search_area_name: str | None = None,
        vacancies_count: int = 99,
        employer_id: int | None = None,
    ) -> list[Vacancy]:
        """
        Method to get vacancies by search parameters.
        Method call method _get_api_response to get vacancies data

        :param search_word: string to search in vacation
        :param search_area_name: name of city or region
        :param vacancies_count: count of vacation
        :param employer_id: id of employer
        :return: list of vacancies
        """

        search_params = {
            "employer_id": employer_id,
            "text": search_word,
            "area": None,
            "page": 0,
            "per_page": vacancies_count,
        }

        # Add area param for search vacations if user add area name
        if search_area_name:
            search_params["area"] = self.__get_area_id(search_area_name)

        # Circle requests with params of pages
        page_counter = 0
        per_page_num = vacancies_count

        vacancies_list = []
        while True:
            if page_counter <= vacancies_count:
                search_params["page"] = page_counter

                if per_page_num <= 100:
                    search_params["per_page"] = per_page_num
                else:
                    search_params["per_page"] = 100
                    per_page_num -= 100

                page_vacancies_list = self._get_api_response(self.url_vacancies, search_params)["items"]
                vacancies_list.extend([Vacancy.new_vacancy(vacancy) for vacancy in page_vacancies_list])

                page_counter += 100

            else:
                break

        return vacancies_list

    def get_employer_data_by_name(
        self,
        search_word: str,
    ) -> list[dict]:
        """
        Method to get information about employer by name.
        Method call method _get_api_response to get employer data

        :param search_word: string to search in vacation
        :return: list of employers

        """

        search_params = {"text": search_word, "only_with_vacancies": True}

        employers_list = self._get_api_response(self.url_employers, search_params)["items"]

        employers_data_list = []

        for employer in employers_list:
            employer_data = {}
            employer_data["name"] = employer["name"]
            employer_data["hh_id"] = employer["id"]
            description = self._get_api_response(f"{self.url_employers}/{employer["id"]}", None)["description"]
            if description is not None:
                if "</p>" in description:
                    try:
                        description = description.split("</p>")[0]
                    except Exception:
                        pass
                    if ". " in description:
                        try:
                            description = description.split(". ")[0]
                        except Exception:
                            pass

            employer_data["description"] = description
            employer_data["url"] = employer["alternate_url"]
            employers_data_list.append(employer_data)

        return employers_data_list


if __name__ == "__main__":
    vacancies = HeadHunterApiService()
    vac_list = vacancies.get_vacancies(employer_id=2104700)
    print([vac.get_dict() for vac in vac_list])
