from DBManager import DBManager
from config import config
from utils import get_company, get_vacancies


def main():
    # Создание словаря с параметрами для создания и подключения к БД
    params = config()

    #  Создание БД
    while True:
        database_name = input('Введите название базы данных на английском:\n> ')
        if all(one_letter in 'abcdefghijklmnopqrstuvwxyz1234567890' for one_letter in
               database_name):
            db_manager = DBManager()
            db_manager.create_database(database_name, params)
            break
        else:
            print('\nВведите название на английском')

    # Создание списка с названиями компаний
    companies_list = ['Lamoda tech', 'Альфа-Банк', 'TINKOFF', 'VK', 'X5 Tech', 'Совкомбанк ПАО ',
                      'Лига Цифровой Экономики', 'I Like IT', 'amoCRM', 'ООО ЛингуаЛео', 'Skyeng']

    # Парсинг и сохранение данных в БД
    for company in companies_list:
        company_info = get_company(company)
        company_vacancies = get_vacancies(company_info['url_vacancies'])
        db_manager.save_data_to_database(company_info, company_vacancies, database_name, params)
    print(f'\nДанные о вакансиях и компаниях сохранены в базу данных {database_name}')

    # Получает список всех компаний и количество вакансий у каждой компании.
    while True:
        request_one = input(
            '\nПоказать список всех компаний и количество вакансий у каждой компании? '
            '(1 - да, 2 - нет)\n> ')
        if request_one == '1':
            list_companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count(
                database_name, params)
            print(list_companies_and_vacancies_count)
            break
        elif request_one == '2':
            print('Следующий вопрос')
            break
        else:
            print('Введите корректное значение')
            continue

    # Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и
    # ссылки на вакансию.
    while True:
        request_two = input(
            '\nПоказать список всех вакансий с указанием названия компании, названия вакансии и '
            'зарплаты и ссылки на вакансию? (1 - да, 2 - нет)\n> ')
        if request_two == '1':
            list_all_vacancies = db_manager.get_all_vacancies(database_name, params)
            print(list_all_vacancies)
            break
        elif request_two == '2':
            print('Следующий вопрос')
            break
        else:
            print('Введите корректное значение')
            continue

    # Получает среднюю зарплату по вакансиям
    while True:
        request_three = input(
            '\nПоказать список компаний и их среднюю зарплату по вакансиям? (1 - да, 2 - нет)\n> ')
        if request_three == '1':
            list_avg_salary = db_manager.get_avg_salary(database_name, params)
            print(list_avg_salary)
            break
        elif request_three == '2':
            print('Следующий вопрос')
            break
        else:
            print('Введите корректное значение')
            continue

    # Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
    while True:
        request_four = input(
            '\nПоказать список всех вакансий, у которых зарплата выше средней по всем вакансиям? '
            '(1 - да, 2 - нет)\n> ')
        if request_four == '1':
            list_vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary(
                database_name, params)
            print(list_vacancies_with_higher_salary)
            break
        elif request_four == '2':
            print('Следующий вопрос')
            break
        else:
            print('Введите корректное значение')
            continue

    # Получает список всех вакансий, в названии которых содержатся переданные в метод слова
    while True:
        request_five = input(
            '\nПоказать список всех вакансий, по ключевому слову? (1 - да, 2 - нет)\n> ')
        if request_five == '1':
            keyword = input('Тогда введите ключевые слова из названия вакансии:\n> ')
            list_vacancies_with_keyword = db_manager.get_vacancies_with_keyword(keyword,
                                                                                database_name,
                                                                                params)
            print(list_vacancies_with_keyword)
            break
        elif request_five == '2':
            print('Следующий вопрос')
            break
        else:
            print('Введите корректное значение')
            continue


if __name__ == '__main__':
    main()
