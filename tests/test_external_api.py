import unittest
from unittest.mock import Mock, patch

from src.external_api import HeadHunterApiService


class TestHeadHunterApiService(unittest.TestCase):

    # test private method __get_area_id
    @patch.object(HeadHunterApiService, "_get_api_response")
    def test_private_get_area_id(self, mock_method: Mock) -> None:
        service = HeadHunterApiService()
        mock_method.return_value = [
            {
                "id": "113",
                "parent_id": None,
                "name": "Россия",
                "areas": [
                    {
                        "id": "1620",
                        "parent_id": "113",
                        "name": "Республика Марий Эл",
                        "areas": [
                            {
                                "id": "4228",
                                "parent_id": "1620",
                                "name": "Виловатово",
                                "areas": [],
                                "utc_offset": "+03:00",
                            },
                            {"id": "1621", "parent_id": "1620", "name": "Волжск", "areas": [], "utc_offset": "+03:00"},
                            {
                                "id": "1622",
                                "parent_id": "1620",
                                "name": "Звенигово",
                                "areas": [],
                                "utc_offset": "+03:00",
                            },
                        ],
                    }
                ],
            }
        ]
        area_name = "Волжск"

        result = "1621"

        assert service._HeadHunterApiService__get_area_id(area_name) == result

    # Test for method get_vacancies
    @patch.object(HeadHunterApiService, "_get_api_response")
    def test_get_vacancies(self, mock_method: Mock) -> None:
        service = HeadHunterApiService()
        mock_method.return_value = {
            "items": [
                {
                    "name": "Python-разработчик",
                    "link": "https://hh.ru/vacancy/125138836",
                    "salary": {"from": 500000, "to": 0},
                    "description": "Опыт коммерческой разработки на <highlighttext>Python</highlighttext> 3.9+. "
                    "Отличные знания FastAPI (или аналогов: Django REST Framework, Flask). "
                    "Уверенные навыки работы...",
                },
                {
                    "name": "Python Django developer",
                    "link": "https://hh.ru/vacancy/125010047",
                    "salary": {"from": 0, "to": 1000},
                    "description": "Опыт: 3–6 лет в разработке на <highlighttext>Python</highlighttext>/Django. "
                    "Multi tenancy. "
                    "Уверенное владение <highlighttext>Python</highlighttext> 3 и "
                    "фреймворком Django (DRF). ",
                },
                {
                    "name": "Директор по финансовому моделированию и сценарному анализу",
                    "link": "https://hh.ru/vacancy/125169109",
                    "salary": {"from": 0, "to": 0},
                    "description": "Навыки анализа данных с помощью Python</highlighttext> и R. "
                    "Опыт работы с СУБД PostgreSQL и SQLite. Знание подходов к оценке кредитных...",
                },
            ]
        }

        assert len(service.get_vacancies(search_word="Puthon")) == 3

    @patch.object(HeadHunterApiService, "_get_api_response")
    def test_get_employer_data_by_name(self, mock_method: Mock) -> None:
        service = HeadHunterApiService()

        mock_method.return_value = {
            "items": [
                {
                    "name": "Ozon",
                    "id": 2180,
                    "description": "<p>Ozon — ведущая мультикатегорийная платформа электронной коммерции и одна из крупнейших интернет-компаний в России",
                    "alternate_url": "https://hh.ru/employer/2180",
                }
            ],
            "description": "Ozon — ведущая мультикатегорийная платформа электронной коммерции и одна из крупнейших интернет-компаний в России",
        }

        result = [
            {
                "name": "Ozon",
                "hh_id": 2180,
                "description": "Ozon — ведущая мультикатегорийная платформа электронной коммерции и одна из крупнейших интернет-компаний в России",
                "url": "https://hh.ru/employer/2180",
            }
        ]

        assert service.get_employer_data_by_name("Ozon") == result
