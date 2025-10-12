from src.external_api import HeadHunterApiService
from src.file_handler import JSONFileHandler


def add_company() -> None:
    """
    Function for select company
    Function ask user employers name. Create Api request and get list of founded employers data in dict by name.
    User select one employer from list
    Function add employer data to json file and return employer data

    :return: employer data
    """

    employer_name = input("Введите название компании для поиска:")

    employers_service = HeadHunterApiService()

    employers_data_list = employers_service.get_employer_data_by_name(employer_name)

    if len(employers_data_list) == 0:
        print("Поиск не дал результатов")
        return None

    [print(f"{index} - {employer}") for index, employer in enumerate(employers_data_list)]

    while True:
        num_of_employer = input("Выберите компанию из списка по номеру:")

        try:
            employer_data = employers_data_list[int(num_of_employer)]
            break
        except ValueError:
            print("Неверный ввод")
        except IndexError:
            print("Неверный номер файла")

    save_data_dicts = JSONFileHandler("user_companies_list.json")

    save_data_dicts.save_data([employer_data])

    return None
