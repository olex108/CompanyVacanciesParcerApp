import os

from src.file_handler import JSONFileHandler


def test_json_file_handler(list_of_vacancies_dict: list[dict], vacancies_list_two_vac_dict: list[dict]) -> None:
    json_handler = JSONFileHandler("test.json")

    # Test for save list of vacancies in file
    json_handler.save_data(list_of_vacancies_dict)
    list_of_save_vacancies = json_handler.get_data()

    assert len(list_of_save_vacancies) == 4

    # Test for add list of vacancies in file (one of two vacancies is existed in file)
    json_handler.save_data(vacancies_list_two_vac_dict)
    list_of_save_vacancies = json_handler.get_data()

    assert len(list_of_save_vacancies) == 5

    # delite and assert vacancies in file

    json_handler.del_data([1, 0])
    list_of_save_vacancies = json_handler.get_data()

    assert len(list_of_save_vacancies) == 3

    # Delite test file from data/
    try:
        os.remove("data/test.json")
    except FileNotFoundError:
        pass
