import psycopg2


class DBManager():
    """Класс для работы с БД PostgreSQL."""

    def create_database(self, database_name, params):
        """Создание базы данных и таблиц для сохранения данных о вакансиях и компаниях."""
        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
        cur.execute(f"CREATE DATABASE {database_name}")

        cur.close()
        conn.close()

        conn = psycopg2.connect(dbname=database_name, **params)
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE companies (
                    id_company SERIAL PRIMARY KEY,
                    company VARCHAR(255) NOT NULL,
                    open_vacancies INTEGER,
                    url_vacancies TEXT
                )
            """)

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE vacancies (
                    id_vacancy SERIAL PRIMARY KEY,
                    id_company INTEGER REFERENCES companies(id_company),
                    name VARCHAR(255) NOT NULL,
                    salary INTEGER,
                    company_name TEXT,
                    url TEXT
                )
            """)

        conn.commit()
        conn.close()

        print(
            f'База данных {database_name} и таблицы для сохранения данных о вакансиях и компаниях созданы')

    def save_data_to_database(self, company, vacancies, database_name, params):
        """Сохранение данных о вакансиях и компаниях в базу данных."""
        conn = psycopg2.connect(dbname=database_name, **params)
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO companies (company, open_vacancies, url_vacancies)
                VALUES (%s, %s, %s)
                RETURNING id_company
                """,
                (company['company'], company['open_vacancies'],
                 company['url_vacancies'])
            )

            id_company = cur.fetchone()[0]

            for vacancy in vacancies:
                cur.execute(
                    """
                    INSERT INTO vacancies (id_company, name, salary, company_name, url)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (id_company, vacancy['name'], vacancy['salary'], vacancy['company_name'],
                     vacancy['url'])
                )

        conn.commit()
        conn.close()

    def get_companies_and_vacancies_count(self, database_name, params):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        conn = psycopg2.connect(dbname=database_name, **params)
        with conn.cursor() as cur:
            cur.execute("""
                SELECT company, open_vacancies FROM companies
            """)
            res = cur.fetchall()

        conn.commit()
        conn.close()

        return res

    def get_all_vacancies(self, database_name, params):
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""
        conn = psycopg2.connect(dbname=database_name, **params)
        with conn.cursor() as cur:
            cur.execute("""
                SELECT name, salary, company_name, url FROM vacancies
            """)
            res = cur.fetchall()

        conn.commit()
        conn.close()

        return res

    def get_avg_salary(self, database_name, params):
        """Получает среднюю зарплату по вакансиям"""
        conn = psycopg2.connect(dbname=database_name, **params)
        with conn.cursor() as cur:
            cur.execute("""
                SELECT company_name, AVG(salary) FROM vacancies
                GROUP BY company_name
            """)
            res = cur.fetchall()

        conn.commit()
        conn.close()

        return res

    def get_vacancies_with_higher_salary(self, database_name, params):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        conn = psycopg2.connect(dbname=database_name, **params)
        with conn.cursor() as cur:
            cur.execute("""
                SELECT name FROM vacancies
                WHERE salary > (SELECT AVG(salary) FROM vacancies)
            """)
            res = cur.fetchall()

        conn.commit()
        conn.close()

        return res

    def get_vacancies_with_keyword(self, keyword, database_name, params):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова."""
        conn = psycopg2.connect(dbname=database_name, **params)
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT name FROM vacancies
                WHERE name LIKE '%{keyword}%'
            """)
            res = cur.fetchall()

        conn.commit()
        conn.close()

        return res
