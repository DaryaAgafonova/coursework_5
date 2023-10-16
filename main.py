from class_HeadHunter import HeadHunter
from class_DBManager import DBManager


hh = HeadHunter()
hh.get_requests()

db_manager = DBManager(host='localhost',
                       port='5432',
                       database='coursework_5',
                       user='postgres',
                       password='')

db_manager.create_database()
db_manager.creating_tables()

print(db_manager.get_companies_and_vacancies_count())
print(db_manager.get_all_vacancies())
print(db_manager.get_avg_salary())
print(db_manager.get_vacancies_with_higher_salary())
print(db_manager.get_vacancies_with_keyword("python"))