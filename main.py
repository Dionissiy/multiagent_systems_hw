from selenium import webdriver
from lxml.html import fromstring
import lxml
import time
import json

def get_data(link, agent):
    agent.get(link)

    journal_description = agent.find_element_by_class_name('journaldescription')

    result = dict()
    result['Title'] = journal_description.find_element_by_class_name('title').text

    xpath = '//*[@id="journals"]/div/div[1]/div[1]/div[2]/div/table[2]/tbody'
    table = journal_description.find_element_by_xpath(xpath)





if __name__ == '__main__':
    agent = webdriver.Firefox('bin/')
    agent.get('https://www.ronpub.com')
    time.sleep(2)

    button = agent.find_element_by_link_text('Journals')
    button.click()

    links = [x.get_attribute('href') for x in agent.find_elements_by_xpath('//*[@id="journals"]/div/div/div/a')]

    data = {}
    for link in links:
        agent.get(link)
        time.sleep(2)
        journal_description = agent.find_element_by_class_name('journaldescription')

        result = dict()
        result['Title'] = agent.find_element_by_xpath('//*[@id="journals"]/div/div[1]/div[1]/div[2]/div/table[1]/tbody/tr[1]/td').text

        table = journal_description.find_element_by_xpath('//table[2]/tbody')

        rows = table.find_elements_by_xpath('//tr')

        for row in rows:
            header = row.find_element_by_xpath('//td[1]')
            content = row.find_element_by_xpath('//td[2]')
            result[header.text] = content.text

        data.append(result)

    with open('nnsps.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

    agent.close()
