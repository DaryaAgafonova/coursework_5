import psycopg2
from psycopg2 import extensions


class DBManager:

    """ Класс DBManager для работы с данными в БД.
    Класс DBManager будет подключаться к БД PostgreSQL"""

    def __init__(self, host, port, database, user, password) -> None:

        """ Инициализация атрибутов класса DBManager. """

        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password



    def create_database(self):

        """ Создание Базы Данных. """

        self.connect = psycopg2.connect(
            host=self.host,
            port=self.port,
            database='postgres',
            user=self.user,
            password=self.password
        )
        try:
            self.connect.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            with self.connect.cursor() as cursor:
                cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (self.database,))
                exists = cursor.fetchone()
                if exists:
                    cursor.execute(f"DROP DATABASE {self.database};")
                cursor.execute(f"CREATE DATABASE {self.database};")
        finally:
            self.connect.close()


    def creating_tables(self) -> None:

        """ Создание таблиц employers и vacancies в БД."""

        self.connect = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )
        try:
            with self.connect:
                with self.connect.cursor() as cursor:
                    self.connect.autocommit = True
                    cursor.execute('''
                    CREATE TABLE employers (
                    employer_id SERIAL PRIMARY KEY,
                    employer_name VARCHAR(255) NOT NULL
                    );
                    ''')

                    cursor.execute('''
                    CREATE TABLE vacancies (
                    vacancy_id SERIAL PRIMARY KEY,
                    employer_id INTEGER REFERENCES employers(employer_id),
                    vacancy_name VARCHAR(255) NOT NULL,
                    salary_from INTEGER,
                    salary_to INTEGER,
                    url_vacancy TEXT
                    );
                    ''')
        finally:
            self.connect.close()


    def get_companies_and_vacancies_count(self) -> list:

        """ Получает список всех компаний и количество вакансий у каждой компании. """

        self.connect = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )
        try:
            with self.connect:
                with self.connect.cursor() as cursor:
                    cursor.execute('''
                    SELECT employers.employer_name, COUNT(vacancies.vacancy_id)
                    FROM employers
                    LEFT JOIN vacancies ON employers.employer_id = vacancies.employer_id
                    GROUP BY employer_name;
                    ''')
                    result = cursor.fetchall()
        finally:
            self.connect.close()

            return result


    def insert_employer(self, data):

        """ """

        self.connect = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )
        try:
            with self.connect:
                with self.connect.cursor() as cursor:
                    for employer in data:
                        cursor.execute('''
                        INSERT INTO employers(employer_id, employer_name) VALUES (%s, %s)
                        ''', (employer['id'], employer['name']))
        finally:
            self.connect.close()


    def insert_vacansies(self, data):

        """ """

        self.connect = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )
        try:
            with self.connect:
                with self.connect.cursor() as cursor:
                    for vacancy in data:
                        if vacancy['salary'] is not None:
                            salary_from = vacancy['salary']['from'] if vacancy['salary']['from'] else 0
                            salary_to = vacancy['salary']['to'] if vacancy['salary']['to'] else 0
                        else:
                            salary_from = 0
                            salary_to = 0
                        cursor.execute('''
                        INSERT INTO vacancies(vacancy_id, employer_id, vacancy_name, salary_from, salary_to, url_vacancy) VALUES (%s, %s, %s, %s, %s, %s)
                        ''', (vacancy['id'], vacancy['employer']['id'], vacancy['name'], salary_from, salary_to , vacancy['alternate_url']))
        finally:
            self.connect.close()


    def get_all_vacancies(self) -> list:

        """ Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию. """

        self.connect = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )
        try:
            with self.connect:
                with self.connect.cursor() as cursor:
                    cursor.execute('''
                    SELECT employers.employer_name, vacancies.vacancy_name, vacancies.salary_from, vacancies.salary_to, vacancies.url_vacancy
                    FROM vacancies
                    INNER JOIN employers ON employers.employer_id = vacancies.employer_id;
                    ''')
                    result = cursor.fetchall()
        finally:
            self.connect.close()

        return result


    def get_avg_salary(self):

        """ Получает среднюю зарплату по вакансиям. """

        self.connect = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )
        try:
            with self.connect:
                with self.connect.cursor() as cursor:
                    cursor.execute('''
                            SELECT AVG((salary_from + salary_to) / 2) 
                            FROM vacancies;
                            ''')
                    result = cursor.fetchall()[0]
        finally:
            self.connect.close()

        return result


    def get_vacancies_with_higher_salary(self):

        """ Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям. """

        avg_salary = self.get_avg_salary()

        self.connect = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )
        try:
            with self.connect:
                with self.connect.cursor() as cursor:
                    cursor.execute('SELECT * FROM vacancies WHERE salary_to > %s', (avg_salary,))
                    result = cursor.fetchall()
        finally:
            self.connect.close()

        return result


    def get_vacancies_with_keyword(self, keyword: str) -> list:

        """ Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python. """

        self.connect = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )
        try:
            with self.connect:
                with self.connect.cursor() as cursor:
                    cursor.execute('SELECT * FROM vacancies WHERE vacancy_name LIKE %s', ('%' + keyword + '%',))
                    result = cursor.fetchall()
        finally:
            self.connect.close()

        return result