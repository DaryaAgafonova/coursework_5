import requests


class HeadHunter:

    """ """

    def __init__(self):

        """ """

        self.base_url = "https://api.hh.ru/"


    def get_requests(self):

        """ """

        employers = [
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

        for employer_id in employers:
            employer_url = self.base_url + f"employers/{employer_id}"
            employer_response = requests.get(employer_url)
            employer_data = employer_response.json()

            vacancies_url = self.base_url + f"vacancies?employer_id={employer_id}"
            vacancies_response = requests.get(vacancies_url)
            vacancies_data = vacancies_response.json()

            #print(f"Employer: {employer_data['name']}")
            #print("Job Vacancies:")
            #for vacancy in vacancies_data['items']:
            #    print(f"- {vacancy['name']}")
            #print("==============================")