import psycopg2


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
            database=self.database,
            user=self.user,
            password=self.password
        )
        try:
            with self.connect:
                with self.connect.cursor() as cursor:
                    self.connect.autocommit = True
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
                    salary INTEGER,
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
        finally:
            self.connect.close()

            return cursor.fetchall()


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
                    SELECT employers.employer_name, vacancies.vacancy_name, vacancies.salary, vacancies.url_vacancy
                    FROM vacancies
                    INNER JOIN employers ON employers.employer_id = vacancies.employer_id;
                    ''')
        finally:
            self.connect.close()

        return cursor.fetchall()


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
                            SELECT AVG(salary) 
                            FROM vacancies;
                            ''')
        finally:
            self.connect.close()

        return cursor.fetchall()[0]


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
                    cursor.execute('SELECT * FROM vacancies WHERE salary > %s', (avg_salary,))
        finally:
            self.connect.close()

        return cursor.fetchall()


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
                    cursor.execute('SELECT * FROM vacancies WHERE vacancy_name LIKE %s', ('%' + keyword + '%'))
        finally:
            self.connect.close()

        return cursor.fetchall()