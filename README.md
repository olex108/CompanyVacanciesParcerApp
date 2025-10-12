# CompanyVacanciesParserApp

App get information about companies and vacancies from hh.ru save it on Postgres database and manage information of vacations on database.

## Installation:

For work in program need to clone repos 
```
git clone https://github.com/olex108/CompanyVacanciesParcerApp.git
```
and install dependencies from `pyproject.toml`
```
poetry install
```

For work with database create file `database.ini` with params of PostgresSQL. Example:

```
[postgresql]
host=localhost
user=your_db_username
password=your_db_password
port=5432
```

## Description of Functionality

### functions

- `main.py` include function `main`, print list of base companies, user can add company to base list. Function save data of companies and its vacation in database, and get different informations of vacations.

- `selection.py` include function `add_company` for select company. Function ask user employers name. Create Api request and get list of founded employers data in dict by name.  User select one employer from list. Function add employer data to json file and return employer data

### classes

- Class `Vacancy` for work with vacancies. In class described dander methods for print and compare vacancies, add new vacancy and validation of salary

- Class `JSONFileHandler` for work with JSON files, with include save, get or del data.

- Class `HeadHunterApiService` for work with site hh.ru with methods:

`get_vacancies` Method to get vacancies by search parameters. Method call method _get_api_response to get vacancies data

`get_employer_data_by_name` Method to get information about employer by name. Method call method _get_api_response to get employer data

- Class `DatabaseHandler` to create database, create tables and feel tables with information about companies and vacancies

- Class `DBManager` to create connection to database PostgreSQL and has methods to manage database:

`get_companies_and_vacancies_count` Method to get list of tuples with companies and count of vacancies from database.

`get_all_vacancies` Method to get list of tuples with company name, vacancy_name, salary and vacancy link.

`get_avg_salary` Method to get AVG salary of vacancies.

`get_vacancies_with_higher_salary`  Method to get list of tuples with company name, vacancy_name, salary and vacancy link, with a higher than average salary

`get_vacancies_with_keyword` Method to get list of tuples with company name, vacancy_name, salary and vacancy link, with search word in vacancy name


