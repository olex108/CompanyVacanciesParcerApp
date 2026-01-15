from src.database import DatabaseHandler, DBManager

import pytest
from unittest.mock import patch

from config import config
from src.external_api import HeadHunterApiService


@pytest.fixture
def test_database_connection():
    test_params = config()
    DatabaseHandler.create_database(**test_params, dbname="test_database")
    test_database = DatabaseHandler(**test_params, dbname="test_database")
    test_database.create_tables()

    yield
    test_database.clear_tables()


def test_fill_companies_vacancies_tables(
    # mock_get,
    test_database_connection,
    list_companies_dicts,
    lists_of_vacations_class,
    lists_of_vacations_dict,
) -> None:
    test_params = config()
    test_database = DatabaseHandler(**test_params, dbname="test_database")
    with patch.object(HeadHunterApiService, "get_vacancies") as mock_get:
        mock_get.return_value = lists_of_vacations_class
        #
        test_database.fill_companies_vacancies_tables(list_companies_dicts)
        #
        test_database_manager = DBManager(**test_params, dbname="test_database")

        assert test_database_manager.get_companies_and_vacancies_count() == [("Ozon", 4)]

        assert test_database_manager.get_avg_salary() == 62625.000000000000

        result = [
            ("Ozon", vac["name"], vac["salary"]["from"], vac["salary"]["to"], vac["link"])
            for vac in lists_of_vacations_dict
        ]

        assert test_database_manager.get_all_vacancies() == result

        assert test_database_manager.get_vacancies_with_higher_salary() == []

        assert test_database_manager.get_vacancies_with_keyword("python") == result[:2]
