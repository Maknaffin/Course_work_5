import requests


def get_company(company):
    """Метод получения данных о компании по API HeadHunter"""
    params = {
        'text': company
    }
    headers = {'User-Agent': 'HH-User-Agent'}
    url = 'https://api.hh.ru/employers'

    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    values = {
        'company': data['items'][0]['name'],
        'url_vacancies': data['items'][0]['vacancies_url'],
        'open_vacancies': data['items'][0]['open_vacancies']
    }

    return values


def get_vacancies(url_vacancies):
    """Метод получения данных о вакансиях компаний по API HeadHunter"""
    headers = {'User-Agent': 'HH-User-Agent'}
    list_vacancies = []
    response = requests.get(url_vacancies, headers=headers)
    data = response.json()
    raw_vacancies = data.get('items')
    if raw_vacancies:
        for vacancy in raw_vacancies:
            list_vacancies.append(
                {
                    'name': vacancy['name'],
                    'salary': vacancy['salary']['from'] if vacancy.get('salary') else 0,
                    'company_name': vacancy['employer']['name'],
                    'url': vacancy['url']
                }
            )

    return list_vacancies
