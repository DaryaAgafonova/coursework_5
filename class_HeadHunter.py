import requests


class HeadHunter:

    """ """

    def __init__(self):

        """ """

        self.base_url = "https://api.hh.ru/"

        self.employers = [
            '1753496',  # ООО Бизапс
            '1795330',  # Ateuco
            '2751250',  # AdminDivision
            '1975782',  # ООО 101
            '669853',  # BeFresh
            '2450307',  # ООО АльянсТелекоммуникейшнс
            '10170495',  # ООО 20 тонн
            '3446179',  # Gembo
            '5536919',  # Come&Pass
            '193400',  # АВТОВАЗ
        ]


    def get_vacancies(self):

        """ """

        vacancies = []
        for employer_id in self.employers:
            vacancies_url = self.base_url + f"vacancies?employer_id={employer_id}"
            vacancies_response = requests.get(vacancies_url)
            vacancies_data = vacancies_response.json()['items']
            vacancies.extend(vacancies_data)

        return vacancies


    def get_employers(self):

        """ """

        employers = []
        for employer_id in self.employers:
            employer_url = self.base_url + f"employers/{employer_id}"
            employer_response = requests.get(employer_url)
            employer_data = employer_response.json()
            employers.append(employer_data)

        return employers
