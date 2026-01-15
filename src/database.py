import psycopg2

from src.external_api import HeadHunterApiService


class DatabaseHandler:
    """
    Class to create database, create tables and feel tables with information about companies and vacancies
    """

    def __init__(
        self,
        user: str,
        password: str,
        host: str = "localhost",
        port: str = "5432",
        dbname: str = "companies_vacations",
    ) -> None:
        """Initialisation function to create connection to PostgreSQL database"""
        self.dbname = dbname
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

    @staticmethod
    def create_database(
        user: str, password: str, host: str = "localhost", port: str = "5432", dbname: str = "companies_vacations"
    ) -> None:
        """Static method to create new database before connection to PostgreSQL database"""

        try:
            conn = psycopg2.connect(user=user, password=password, host=host, port=port)
            conn.autocommit = True
            cur = conn.cursor()
            cur.execute(f"CREATE DATABASE {dbname}")
            cur.close()
            conn.close()

        except psycopg2.errors.DuplicateDatabase:
            pass

    def create_tables(self) -> None:
        """Method to create tables companies and vacancies"""

        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute(
                        """
                        CREATE TABLE companies (
                            company_id SERIAL PRIMARY KEY,
                            company_name VARCHAR(255) NOT NULL,
                            hh_company_id INTEGER NOT NULL,
                            company_url VARCHAR(255),
                            company_description TEXT
                        )
                    """
                    )

                with self.conn.cursor() as cur:
                    cur.execute(
                        """
                        CREATE TABLE vacancies (
                            vacancy_id SERIAL PRIMARY KEY,
                            company_id INT REFERENCES companies(company_id),
                            vacancy_name VARCHAR(255) NOT NULL,
                            vacancy_url VARCHAR(255) NOT NULL,
                            salary_from INTEGER,
                            salary_to INTEGER,
                            vacancy_description TEXT
                        )
                    """
                    )

                self.conn.commit()

        except psycopg2.errors.DuplicateTable:
            pass


    def clear_tables(self) -> None:
        """Method to drop database"""

        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute("""DROP TABLE companies CASCADE""")
                with self.conn.cursor() as cur:
                    cur.execute("""DROP TABLE vacancies CASCADE""")

                self.conn.commit()
        except psycopg2.errors.Error:
            self.conn.rollback()

    def fill_companies_vacancies_tables(self, list_of_companies: list[dict]) -> None:
        """
        Method to fill companies vacancies tables with information about companies
        Method get list of companies and by circle for fill table companies, get company_id from database,
        and fill table vacancies with information about vacancies of this company from API hh.ru

        :param list_of_companies: list of dicts with information about companies
        """

        # Create Api
        api_service = HeadHunterApiService()
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    for company in list_of_companies:
                        # Fill table with information about company from list of dicts
                        cur.execute(
                            """
                            INSERT INTO companies (company_name, hh_company_id, company_url, company_description)
                            VALUES (%s, %s, %s, %s)
                            RETURNING company_id
                            """,
                            (company["name"], int(company["hh_id"]), company["url"], company["description"]),
                        )
                        # Get company_id from database
                        company_id = cur.fetchone()[0]
                        # Get vacancies of company by API hh.ru
                        list_of_vacancies = []
                        list_of_vacancies = api_service.get_vacancies(company["hh_id"])

                        for vacancy in list_of_vacancies:
                            vacancy = vacancy.get_dict()
                            cur.execute(
                                """
                                INSERT INTO vacancies (company_id, vacancy_name, vacancy_url, salary_from, salary_to, vacancy_description)
                                VALUES (%s, %s, %s, %s, %s, %s)
                                """,
                                (
                                    company_id,
                                    vacancy["name"],
                                    vacancy["link"],
                                    vacancy["salary"]["from"],
                                    vacancy["salary"]["to"],
                                    vacancy["description"],
                                ),
                            )

                self.conn.commit()

        except psycopg2.errors.Error as e:
            print(e)
            self.conn.rollback()


class DBManager:
    """
    Class to create connection to database PostgreSQL and has methods to manage database:
    """

    def __init__(
        self,
        user: str,
        password: str,
        host: str = "localhost",
        port: str = "5432",
        dbname: str = "companies_vacations",
    ) -> None:
        """Initialisation function to create connection to PostgreSQL database"""

        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

    def get_companies_and_vacancies_count(self) -> list[tuple]:
        """
        Method to get list of tuples with companies and count of vacancies from database. Use INNER JOIN.

        :return: list of tuples with companies and count of vacancies from database
        """

        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT companies.company_name, COUNT(*) FROM vacancies
                        INNER JOIN companies USING(company_id)
                        GROUP BY company_name;
                        """
                    )
                    data = cur.fetchall()
                return data

        except psycopg2.errors.Error as e:
            print(e)
            return []

    def get_all_vacancies(self) -> list[tuple]:
        """
        Method to get list of tuples with company name, vacancy_name, salary and vacancy link. Use RIGHT JOIN.

        :return: list of tuples with companies and count of vacancies from database
        """

        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT company_name, vacancies.vacancy_name, vacancies.salary_from, vacancies.salary_to, vacancies.vacancy_url  FROM companies
                        RIGHT JOIN vacancies USING(company_id);
                        """
                    )
                    data = cur.fetchall()
                return data

        except psycopg2.errors.Error as e:
            print(e)
            return []

    def get_avg_salary(self) -> float | None:
        """
        Method to get AVG salary of vacancies.

        :return: avg_salary:  AVG salary of vacancies
        """

        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT AVG((salary_from + salary_to)/2) FROM vacancies;
                        """
                    )
                    avg_salary = cur.fetchone()[0]
                return avg_salary

        except psycopg2.errors.Error as e:
            print(e)
            return None

    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        """
        Method to get list of tuples with company name, vacancy_name, salary and vacancy link,
        with a higher than average salary. Use RIGHT JOIN.

        :return: list of tuples with companies and count of vacancies from database
        """

        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT company_name, vacancies.vacancy_name, vacancies.salary_from, vacancies.salary_to, vacancies.vacancy_url 
                        FROM companies
                        RIGHT JOIN vacancies USING(company_id)
                        WHERE vacancies.salary_to > (SELECT AVG((salary_from + salary_to)/2) FROM vacancies);
                        """
                    )
                    data = cur.fetchall()
                return data

        except psycopg2.errors.Error as e:
            print(e)
            return []

    def get_vacancies_with_keyword(self, search_word: str) -> list[tuple]:
        """
        Method to get list of tuples with company name, vacancy_name, salary and vacancy link,
        with search word in vacancy name. Use RIGHT JOIN.

        :param: search_word:  search word in vacancy name
        :return: list of tuples with companies and count of vacancies from database"""

        search_word = search_word.lower()
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute(
                        """SELECT company_name, vacancies.vacancy_name, vacancies.salary_from, vacancies.salary_to, vacancies.vacancy_url 
                            FROM companies
                            RIGHT JOIN vacancies USING(company_id)
                            WHERE LOWER(vacancies.vacancy_name) LIKE ('{}%') OR LOWER(vacancies.vacancy_name) LIKE ('%{}%') OR LOWER(vacancies.vacancy_name) LIKE ('%{}');
                        """.format(
                            search_word, search_word, search_word
                        )
                    )
                    data = cur.fetchall()
                return data

        except psycopg2.errors.Error as e:
            print(e)
            return []
