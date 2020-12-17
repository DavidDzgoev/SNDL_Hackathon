import requests
from bs4 import BeautifulSoup

import pandas as pd

from SPARQLWrapper import SPARQLWrapper, JSON
from fake_useragent import UserAgent

import wikipediaapi

from qwikidata.linked_data_interface import get_entity_dict_from_api

import arrow
import re

language = wikipediaapi.Wikipedia('en')


def check_person(QID):
    """
    Проверка является ли сущность человеком и есть ли у него свойство position_held

    :param QID: qID личности
    :return: True/False
    """
    print(QID)
    sparql = SPARQLWrapper("http://query.wikidata.org/sparql", agent=UserAgent().random)
    q = """
        SELECT ?inception WHERE {
          wd:""" + QID + """ wdt:P31 ?inception
        }
    """
    sparql.setQuery(q)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if results['results']['bindings'] != [] and results['results']['bindings'][0]['inception']['value'][-2:] == 'Q5':
        return True
    else:
        return False


def get_position(QID):
    """
    Получение позиции по QID

    :param QID: qID личности
    :return: id позиции
    """
    sparql = SPARQLWrapper("http://query.wikidata.org/sparql", agent=UserAgent().random)
    q = """
        SELECT ?inception WHERE {
          wd:""" + QID + """ wdt:P39 ?inception
        }
    """
    sparql.setQuery(q)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if results['results']['bindings']:
        return results['results']['bindings'][0]['inception']['value']
    else:
        return False


def get_start(QID):
    """
    Получение даты начала срока правления по QID в нужном формате

    :param QID: qID личности
    :return: дата начала правления
    """
    person_dict = get_entity_dict_from_api(QID)
    if 'qualifiers' in person_dict['claims']['P39'][0] and 'P580' in person_dict['claims']['P39'][0]['qualifiers']:
        start_time = str(person_dict['claims']['P39'][0]['qualifiers']['P580'][0]['datavalue']['value']['time'])[1:11]
        if start_time[5:] == '00-00':
            start_time = start_time[:4]
        elif start_time[8:] == '00':
            start_time = start_time[:7]
        if len(start_time) == 4:
            if str(person_dict['claims']['P39'][0]['qualifiers']['P580'][0]['datavalue']['value']['time'])[0] == '-':
                start_time = '-' + start_time
                start_time = start_time[:start_time.rfind('.') + 1] + start_time[start_time.rfind('.') + 1:].replace(
                    '0', '')
                return start_time
            else:
                start_time = start_time[:start_time.rfind('.') + 1] + start_time[start_time.rfind('.') + 1:].replace(
                    '0', '')
                return start_time
        elif len(start_time) == 7:
            if str(person_dict['claims']['P39'][0]['qualifiers']['P580'][0]['datavalue']['value']['time'])[0] == '-':
                start_time = '-' + arrow.get(start_time, 'YYYY-MM').format('MM.YYYY')
                start_time = start_time[:start_time.rfind('.') + 1] + start_time[start_time.rfind('.') + 1:].replace(
                    '0', '')
                return start_time
            else:
                start_time = arrow.get(start_time, 'YYYY-MM').format('MM.YYYY')
                start_time = start_time[:start_time.rfind('.') + 1] + start_time[start_time.rfind('.') + 1:].replace(
                    '0', '')
                return start_time
        elif len(start_time) == 10:
            if str(person_dict['claims']['P39'][0]['qualifiers']['P580'][0]['datavalue']['value']['time'])[0] == '-':
                start_time = '-' + arrow.get(start_time, 'YYYY-MM-DD').format('DD.MM.YYYY')
                start_time = start_time[:start_time.rfind('.') + 1] + start_time[start_time.rfind('.') + 1:].replace(
                    '0', '')
                return start_time
            else:
                start_time = arrow.get(start_time, 'YYYY-MM-DD').format('DD.MM.YYYY')
                start_time = start_time[:start_time.rfind('.') + 1] + start_time[start_time.rfind('.') + 1:].replace(
                    '0', '')
                return start_time
    return 'нет данных'


def get_end(QID):
    """
    Получение даты окончания срока правления по qID в нужном формате
    
    :param QID: qID личности
    :return: дата окончания правления
    """
    person_dict = get_entity_dict_from_api(QID)
    if 'qualifiers' in person_dict['claims']['P39'][0] and 'P582' in person_dict['claims']['P39'][0]['qualifiers']:
        end_time = str(person_dict['claims']['P39'][0]['qualifiers']['P582'][0]['datavalue']['value']['time'])[1:11]
        if end_time[5:] == '00-00':
            end_time = end_time[:4]
        elif end_time[8:] == '00':
            end_time = end_time[:7]
        if len(end_time) == 4:
            if str(person_dict['claims']['P39'][0]['qualifiers']['P582'][0]['datavalue']['value']['time'])[0] == '-':
                end_time = '-' + end_time
                end_time = end_time[:end_time.rfind('.') + 1] + end_time[end_time.rfind('.') + 1:].replace('0', '')
                return end_time
            else:
                end_time = end_time[:end_time.rfind('.') + 1] + end_time[end_time.rfind('.') + 1:].replace('0', '')
                return end_time
        elif len(end_time) == 7:
            if str(person_dict['claims']['P39'][0]['qualifiers']['P582'][0]['datavalue']['value']['time'])[0] == '-':
                end_time = '-' + arrow.get(end_time, 'YYYY-MM').format('MM.YYYY')
                end_time = end_time[:end_time.rfind('.') + 1] + end_time[end_time.rfind('.') + 1:].replace('0', '')
                return end_time
            else:
                end_time = arrow.get(end_time, 'YYYY-MM').format('MM.YYYY')
                end_time = end_time[:end_time.rfind('.') + 1] + end_time[end_time.rfind('.') + 1:].replace('0', '')
                return end_time
        elif len(end_time) == 10:
            if str(person_dict['claims']['P39'][0]['qualifiers']['P582'][0]['datavalue']['value']['time'])[0] == '-':
                end_time = '-' + arrow.get(end_time, 'YYYY-MM-DD').format('DD.MM.YYYY')
                end_time = end_time[:end_time.rfind('.') + 1] + end_time[end_time.rfind('.') + 1:].replace('0', '')
                return end_time
            else:
                end_time = arrow.get(end_time, 'YYYY-MM-DD').format('DD.MM.YYYY')
                end_time = end_time[:end_time.rfind('.') + 1] + end_time[end_time.rfind('.') + 1:].replace('0', '')
                return end_time
    else:
        return 'нет данных'


def get_precision(date):
    """
    Получения точности даты

    :param date: датаправления
    :return: индекс точности
    """
    if date == 'нет данных':
        return 'нет данных'
    elif date.count('.') == 0:
        return 2
    elif date.count('.') == 1:
        return 1
    elif date.count('.') == 2:
        return 0
    else:
        return 4


def get_reign(wikipedia_url):
    """
    Получение должности, даты начала и даты окончания правления
    личности по url её страницы на wikipedia.
    Важно, что здесь используются шаблоны регулряных выражений для поиска дат

    :param wikipedia_url: url страницы личности на wikipedia
    :return: ans: датафрейм
    """
    p = re.compile(r'[1-9][0-9][0-9][0-9][\–\-][1-9][0-9][0-9][0-9]')
    p2 = re.compile(r'[^{0:9}][1-9][0-9][0-9][\–\-][1-9][0-9][0-9]')
    p3 = re.compile(r'[^{0:9}][1-9][0-9][0-9][\–\-][1-9][0-9][0-9][0-9]')
    p4 = re.compile(r'[1-9][0-9][0-9][\s][B][C][\s][\–\-][\s][1-9][0-9][0-9][\s][B][C]')
    p5 = re.compile(r'[1-9][0-9][0-9][\s][\–\-][\s][1-9][0-9][0-9][\s][B][C]')
    p6 = re.compile(r'[1-9][0-9][0-9][\–\-][1-9][0-9][0-9][\s][B][C]')
    p7 = re.compile(r'[1-9][0-9][0-9][\–\-][1-9][0-9][0-9][0-9][\s][B][C]')
    p8 = re.compile(r'[^{0:9}][1-9][0-9][\s][B][C][\s][\–\-][\s][1-9][0-9]')
    p9 = re.compile(r'[^{0:9}][1-9][0-9][\–\-][1-9][0-9]')
    p10 = re.compile(r'[^{0:9}][1-9][0-9][\–\-][1-9][0-9][0-9]')
    ans = pd.DataFrame(columns=['position', 'start', 'end'])
    positions = []
    starts = []
    ends = []
    contents = requests.get(wikipedia_url).text
    soup = BeautifulSoup(contents, 'lxml')
    for table in soup.find_all("table"):
        if 'wikitable succession-box' in str(table):
            for row in table.find_all('tr'):
                if 'Titles in pretence' in row.text:
                    break
                for col in row.find_all('td'):
                    if p8.findall(col.text):
                        for reign in p8.findall(col.text):
                            for ref in col.find_all('a'):
                                if language.page(ref['href'][6:]).exists():
                                    contents2 = requests.get(language.page(ref['href'][6:]).fullurl).text
                                    soup2 = BeautifulSoup(contents2, 'lxml')
                                    for tag in soup2.find_all("li"):
                                        if 'wikidata' in str(tag):
                                            for link in tag.find_all('a'):
                                                if 'wiki/Special' in str(link['href']):
                                                    positions.append(str(link['href']))
                                                    if ' – ' in str(reign):
                                                        start, end = str(reign).split(' – ')
                                                        start = '-' + start[1:3]
                                                        end = end
                                                    else:
                                                        start, end = str(reign).split(' - ')
                                                        start = '-' + start[1:3]
                                                        end = end
                                                    starts.append(start)
                                                    ends.append(end)
                    if p7.findall(col.text):
                        for reign in p7.findall(col.text):
                            for ref in col.find_all('a'):
                                if language.page(ref['href'][6:]).exists():
                                    contents2 = requests.get(language.page(ref['href'][6:]).fullurl).text
                                    soup2 = BeautifulSoup(contents2, 'lxml')
                                    for tag in soup2.find_all("li"):
                                        if 'wikidata' in str(tag):
                                            for link in tag.find_all('a'):
                                                if 'wiki/Special' in str(link['href']):
                                                    positions.append(str(link['href']))
                                                    if '–' in str(reign):
                                                        start, end = str(reign).split('–')
                                                        start = '-' + start[:-3]
                                                        end = '-' + end[:-4]
                                                    else:
                                                        start, end = str(reign).split('-')
                                                        start = '-' + start[:-3]
                                                        end = '-' + end[:-4]
                                                    starts.append(start)
                                                    ends.append(end)
                    elif p5.findall(col.text):
                        for reign in p5.findall(col.text):
                            for ref in col.find_all('a'):
                                if language.page(ref['href'][6:]).exists():
                                    contents2 = requests.get(language.page(ref['href'][6:]).fullurl).text
                                    soup2 = BeautifulSoup(contents2, 'lxml')
                                    for tag in soup2.find_all("li"):
                                        if 'wikidata' in str(tag):
                                            for link in tag.find_all('a'):
                                                if 'wiki/Special' in str(link['href']):
                                                    positions.append(str(link['href']))
                                                    if ' – ' in str(reign):
                                                        start, end = str(reign).split(' – ')
                                                        start = '-' + start[:-3]
                                                        end = '-' + end[:-3]
                                                    else:
                                                        start, end = str(reign).split(' - ')
                                                        start = '-' + start[:-3]
                                                        end = '-' + end[:-3]
                                                    starts.append(start)
                                                    ends.append(end)
                    elif p6.findall(col.text):
                        for reign in p6.findall(col.text):
                            for ref in col.find_all('a'):
                                if language.page(ref['href'][6:]).exists():
                                    contents2 = requests.get(language.page(ref['href'][6:]).fullurl).text
                                    soup2 = BeautifulSoup(contents2, 'lxml')
                                    for tag in soup2.find_all("li"):
                                        if 'wikidata' in str(tag):
                                            for link in tag.find_all('a'):
                                                if 'wiki/Special' in str(link['href']):
                                                    positions.append(str(link['href']))
                                                    if '–' in str(reign):
                                                        start, end = str(reign).split('–')
                                                        start = '-' + start
                                                        end = '-' + end[:-3]
                                                    else:
                                                        start, end = str(reign).split('-')
                                                        start = '-' + start
                                                        end = '-' + end[:-3]
                                                    starts.append(start)
                                                    ends.append(end)
                    elif p4.findall(col.text):
                        for reign in p4.findall(col.text):
                            for ref in col.find_all('a'):
                                if language.page(ref['href'][6:]).exists():
                                    contents2 = requests.get(language.page(ref['href'][6:]).fullurl).text
                                    soup2 = BeautifulSoup(contents2, 'lxml')
                                    for tag in soup2.find_all("li"):
                                        if 'wikidata' in str(tag):
                                            for link in tag.find_all('a'):
                                                if 'wiki/Special' in str(link['href']):
                                                    positions.append(str(link['href']))
                                                    if ' – ' in str(reign):
                                                        start, end = str(reign).split(' – ')
                                                        start = '-' + start[:-3]
                                                        end = '-' + end[:-3]
                                                    else:
                                                        start, end = str(reign).split(' - ')
                                                        start = '-' + start[:-3]
                                                        end = '-' + end[:-3]
                                                    starts.append(start)
                                                    ends.append(end)
                    elif p.findall(col.text):
                        for reign in p.findall(col.text):
                            for ref in col.find_all('a'):
                                if language.page(ref['href'][6:]).exists():
                                    contents2 = requests.get(language.page(ref['href'][6:]).fullurl).text
                                    soup2 = BeautifulSoup(contents2, 'lxml')
                                    for tag in soup2.find_all("li"):
                                        if 'wikidata' in str(tag):
                                            for link in tag.find_all('a'):
                                                if 'wiki/Special' in str(link['href']):
                                                    positions.append(str(link['href']))
                                                    if '–' in str(reign):
                                                        start, end = str(reign).split('–')
                                                    else:
                                                        start, end = str(reign).split('-')
                                                    starts.append(start)
                                                    ends.append(end)
                    elif p3.findall(col.text):
                        for reign in p3.findall(col.text):
                            for ref in col.find_all('a'):
                                if language.page(ref['href'][6:]).exists():
                                    contents2 = requests.get(language.page(ref['href'][6:]).fullurl).text
                                    soup2 = BeautifulSoup(contents2, 'lxml')
                                    for tag in soup2.find_all("li"):
                                        if 'wikidata' in str(tag):
                                            for link in tag.find_all('a'):
                                                if 'wiki/Special' in str(link['href']):
                                                    positions.append(str(link['href']))
                                                    if '–' in str(reign):
                                                        start, end = str(reign).split('–')
                                                        start = start[1:]
                                                    else:
                                                        start, end = str(reign).split('-')
                                                        start = start[1:]
                                                    starts.append(start)
                                                    ends.append(end)
                    elif p2.findall(col.text):
                        for reign in p2.findall(col.text):
                            for ref in col.find_all('a'):
                                if language.page(ref['href'][6:]).exists():
                                    contents2 = requests.get(language.page(ref['href'][6:]).fullurl).text
                                    soup2 = BeautifulSoup(contents2, 'lxml')
                                    for tag in soup2.find_all("li"):
                                        if 'wikidata' in str(tag):
                                            for link in tag.find_all('a'):
                                                if 'wiki/Special' in str(link['href']):
                                                    positions.append(str(link['href']))
                                                    if '–' in str(reign):
                                                        start, end = str(reign).split('–')
                                                        start = start[1:]
                                                    else:
                                                        start, end = str(reign).split('-')
                                                        start = start[1:]
                                                    starts.append(start)
                                                    ends.append(end)
                    elif p10.findall(col.text):
                        for reign in p10.findall(col.text):
                            for ref in col.find_all('a'):
                                if language.page(ref['href'][6:]).exists():
                                    contents2 = requests.get(language.page(ref['href'][6:]).fullurl).text
                                    soup2 = BeautifulSoup(contents2, 'lxml')
                                    for tag in soup2.find_all("li"):
                                        if 'wikidata' in str(tag):
                                            for link in tag.find_all('a'):
                                                if 'wiki/Special' in str(link['href']):
                                                    positions.append(str(link['href']))
                                                    if '–' in str(reign):
                                                        start, end = str(reign).split('–')
                                                        start = start[1:]
                                                    else:
                                                        start, end = str(reign).split('-')
                                                        start = start[1:]
                                                    starts.append(start)
                                                    ends.append(end)
                    elif p9.findall(col.text):
                        for reign in p9.findall(col.text):
                            for ref in col.find_all('a'):
                                if language.page(ref['href'][6:]).exists():
                                    contents2 = requests.get(language.page(ref['href'][6:]).fullurl).text
                                    soup2 = BeautifulSoup(contents2, 'lxml')
                                    for tag in soup2.find_all("li"):
                                        if 'wikidata' in str(tag):
                                            for link in tag.find_all('a'):
                                                if 'wiki/Special' in str(link['href']):
                                                    positions.append(str(link['href']))
                                                    if '–' in str(reign):
                                                        start, end = str(reign).split('–')
                                                        start = start[1:]
                                                    else:
                                                        start, end = str(reign).split('-')
                                                        start = start[1:]
                                                    starts.append(start)
                                                    ends.append(end)
    if starts:
        ans['position'] = positions
        ans['start'] = starts
        ans['end'] = ends
    else:
        ans['position'] = ['нет данных']
        ans['start'] = ['нет данных']
        ans['end'] = ['нет данных']
    return ans.drop_duplicates(['position', 'start'])


def get_qid(wikidata_link):
    """
    Получение QID по ссылке из wikidata путем срезки

    :param wikidata_link: ссылка на wikidata
    :return: QID
    """
    return wikidata_link[wikidata_link.rfind('Q'):]


def get_wikidata_page(wikipedia_url, data):
    """
    Парсинг данных для ссылки из wikipedia, в случае если это человек со свойстовом position_held

    :param wikipedia_url: url страницы личности на wikipedia
    :param data: датафрейм, к которому мы добавим данные о личности
    :return: возвращает подаваемый датафрейм, но с прибавленными данными о правителе
    """
    contents = requests.get(wikipedia_url).text
    soup = BeautifulSoup(contents, 'lxml')
    for tag in soup.find_all("li"):
        if 'wikidata' in str(tag):
            for link in tag.find_all('a'):
                if 'wiki/Special' in str(link['href']):
                    q = get_qid(str(link['href']))
                    if check_person(q):
                        person_df = pd.DataFrame(
                            columns=['person', 'position', 'start_precision', 'start', 'end_precision', 'end'])
                        pos = get_position(q)
                        if pos:
                            start = get_start(q)
                            end = get_end(q)
                            if start == 'нет данных':
                                print(wikipedia_url)
                                reigns = get_reign(wikipedia_url)
                                person_df['start'] = reigns['start']
                                start_prec = []
                                end_prec = []
                                for x in list(reigns['start']):
                                    start_prec.append(get_precision(x))
                                for x in list(reigns['end']):
                                    end_prec.append(get_precision(x))
                                person_df['start_precision'] = start_prec
                                person_df['end_precision'] = end_prec
                                person_df['end'] = reigns['end']
                                person_df['person'] = [str(link['href'])] * len(list(person_df['start']))
                                if reigns['position'][0] != ['нет данных']:
                                    person_df['position'] = reigns['position']
                                else:
                                    person_df['position'] = [pos]
                            else:
                                person_df['person'] = [str(link['href'])]
                                person_df['position'] = [pos]
                                start_prec = get_precision(start)
                                end_prec = get_precision(end)
                                person_df['start_precision'] = [start_prec]
                                person_df['end_precision'] = [end_prec]
                                person_df['start'] = [start]
                                person_df['end'] = [end]
                            data = pd.concat([data, person_df])
    return data


def page_links(page_url):
    """
    Проход по всем ссылкам на страницы со списком правителей на википедии
    
    :param page_url: url страницы личности на wikipedia
    :return: список данных о всех правителях со страницы
    """
    data = pd.DataFrame(columns=['person', 'position', 'start_precision', 'start', 'end_precision', 'end'])
    for link in page_url.links:
        print(link)
        if language.page(link).exists():
            data = get_wikidata_page(language.page(link).fullurl, data)
    return data
