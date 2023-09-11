import requests
import xml.etree.ElementTree as ET
from exceptions import ParsingError

def get_currencies():
    """
    Функция получения валюты
    """
    try:
        response = requests.get("https://www.cbr.ru/scripts/XML_daily.asp")
        if response.status_code != 200:
            raise ParsingError(f"Ошибка получения курса валют! Статус:{response.status_code}")

        root = ET.fromstring(response.content)
        formatted_currencies = {}
        for valute in root.findall('Valute'):
            char_code = valute.find('CharCode').text
            value = float(valute.find('Value').text.replace(',', '.'))
            nominal = int(valute.find('Nominal').text)
            rate = value / nominal
            formatted_currencies[char_code] = rate

        formatted_currencies['RUB'] = 1.0
        return formatted_currencies
    except ParsingError as error:
        print(error)


def filter_vacancies_by_keyword(vacancies, keyword):
    """
    Функция поиска по введенному пользователю слову
    """
    filtered_vacancies = []
    keyword = keyword.lower()

    for vacancy in vacancies:
        if keyword in vacancy.title.lower() or keyword in vacancy.employer.lower():
            filtered_vacancies.append(vacancy)

    return filtered_vacancies


def filter_vacancies_by_platform(vacancies, platform):
    """
    Функция фильтрации вакансий по платформе
    """
    return [vacancy for vacancy in vacancies if vacancy.api.lower() == platform.lower()]

def sort_vacancies_by_min_salary(vacancies):
    """
    Функция сортировки по минимальной заработной плате
    """
    return sorted(vacancies, key=lambda vacancy: (vacancy.salary_from is None, vacancy.salary_from))


def get_top_n_highest_paid_vacancies(vacancies, n):
    """
    Функция вывода необходимого количества вакансий по высокой зарплате
    """
    vacancies_with_salary = [vacancy for vacancy in vacancies if vacancy.salary_from is not None]
    sorted_vacancies = sorted(vacancies_with_salary, key=lambda x: x.salary_from, reverse=True)
    top_n_vacancies = sorted_vacancies[:n]

    return top_n_vacancies


