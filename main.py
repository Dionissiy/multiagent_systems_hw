from selenium import webdriver
from lxml.html import fromstring
import pprint as pp
import lxml
import time
import json


def get_source_code(link, agent):  # returns lxml.html.HtmlElement
    agent.get(link)
    source = agent.page_source
    return fromstring(source)


def get_journal_description(source):  # returns dictionary
    result = dict()
    journal_description = source.xpath('//*[@id="journals"]/div/div[1]/div[1]/div[2]/div')[0]

    title = journal_description.find_class('title')[0].xpath('text()')[0]
    result['Title'] = title

    table = journal_description.xpath('table[2]')[0]
    rows = table.xpath('tbody/tr')

    for row in rows:
        header = row.xpath('td[1]/text()')[0]
        value = row.xpath('td[2]/text()')[0]
        result[header] = value

    return result


def get_list_of_articles(source):  # returns list of HtmlElements
    articles = source.find_class('article')
    return articles


def get_list_of_authors(source_code):
    authors_source = source_code.xpath('a')
    authors = []
    for x in authors_source:
        author = {
            'Name': x.xpath('text()')[0],
            'Link': x.xpath('@href')[0]
        }
        authors.append(author)

    return authors


def get_data_from_article(article):  # returns dictionary with article data
    data = dict()
    #data['License'] = article.xpath('p[1]/strong/span/text()')[0]
    data['Title'] = article.xpath('p[2]/a/text()')[0]
    data['Authors'] = get_list_of_authors(article.xpath('p[3]')[0])

    link_container = article.find_class('download')[0]
    data['Link to PDF'] = link_container.xpath('@href')[0]

    return data


def save_file(data):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def get_journal_data(link, agent):
    agent.get(link)
    button = agent.find_element_by_xpath('//*[@id="journals"]/div/div[2]/div[1]/a[5]')
    time.sleep(1)
    button.click()
    time.sleep(1)

    source_code = fromstring(agent.page_source)

    journal_data = {}
    journal_data['Journal description'] = get_journal_description(source_code)

    container = source_code.xpath('//*[@id="VolumesIssuesRight"]')[0]
    articles = get_list_of_articles(container)
    journal_data['Articles'] = [get_data_from_article(x) for x in articles]

    return journal_data


if __name__ == '__main__':
    agent = webdriver.Firefox('bin/')
    agent.get('https://www.ronpub.com')
    time.sleep(2)

    button = agent.find_element_by_link_text('Journals')
    button.click()

    links = [x.get_attribute('href') for x in agent.find_elements_by_xpath('//*[@id="journals"]/div/div/div/a')]

    data = [get_journal_data(link, agent) for link in links]

    save_file(data)

    agent.close()
