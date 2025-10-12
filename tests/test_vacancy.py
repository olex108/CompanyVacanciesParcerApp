from src.vacancy import Vacancy


# Test initialization vacancy
def test_vacancy_init(vacancy_python: Vacancy) -> None:
    result = "Название: Python, ссылка: python.test, зарплата: 10000 - 20000, описание: Test description"
    assert str(vacancy_python) == result


# Test dander methods for compare two vacations
def test_vacancy_compare(vacancy_python_less_salary: Vacancy, vacancy_python_large_salary: Vacancy) -> None:

    # Compare two vacations
    compare_1 = vacancy_python_large_salary > vacancy_python_less_salary
    result_1 = True
    compare_2 = vacancy_python_large_salary >= vacancy_python_less_salary
    result_2 = True
    compare_3 = vacancy_python_large_salary < vacancy_python_less_salary
    result_3 = False
    compare_4 = vacancy_python_large_salary <= vacancy_python_less_salary
    result_4 = False

    assert compare_1 == result_1
    assert compare_2 == result_2
    assert compare_3 == result_3
    assert compare_4 == result_4

    # Compare vacancy and number
    compare_1 = vacancy_python_large_salary > 1000
    result_1 = True
    compare_2 = vacancy_python_large_salary >= 2000.20
    result_2 = True

    assert compare_1 == result_1
    assert compare_2 == result_2


def test_vacancy_new(list_of_vacancies_dict: list[dict]) -> None:
    vac_1 = Vacancy.new_vacancy(list_of_vacancies_dict[0])
    result = (
        "Название: Python-разработчик, ссылка: https://hh.ru/vacancy/125138836, зарплата: 500000 - 0, описание: "
        "Опыт коммерческой разработки на <highlighttext>Python</highlighttext> 3.9+. "
        "Отличные знания FastAPI (или аналогов: Django REST Framework, Flask). Уверенные навыки работы..."
    )
    assert str(vac_1) == result
