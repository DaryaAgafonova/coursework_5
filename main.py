from class_HeadHunter import HeadHunter
from class_DBManager import DBManager


hh = HeadHunter()


db_manager = DBManager(host='localhost',
                       port='5432',
                       database='coursework_5',
                       user='postgres',
                       password='')

db_manager.create_database()
db_manager.creating_tables()
db_manager.insert_employer(hh.get_employers())
db_manager.insert_vacansies(hh.get_vacancies())

print(db_manager.get_companies_and_vacancies_count())
print(db_manager.get_all_vacancies())
print(db_manager.get_avg_salary())
print(db_manager.get_vacancies_with_higher_salary())
print(db_manager.get_vacancies_with_keyword("менеджер"))