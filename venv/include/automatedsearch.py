from selenium import webdriver
from bs4 import BeautifulSoup
import logging
import urllib.request as ur
import pandas as pd
logging.getLogger().setLevel(logging.INFO)


class AutomatedSearch:

    website = str
    react_name = str
    data = list

    def __init__(self, website, react_name):
        self.website = website
        self.react_name = react_name

    def search(self):
        data = pd.DataFrame(columns=['reactants', 'products', 'rate_reaction'])
        logging.info("starting automated search from {0} for this reactant"
                     " element {1}".format(self.website, self.react_name))

        reactions_web_links, record_number = self.send_key(self.website, self.react_name)
        reactions_html = self.html_parse(reactions_web_links)

        for page in reactions_html:
            data_map = self.html_navigate(page)
            data = data.append(data_map, ignore_index=True)

        return data

    @staticmethod
    def html_navigate(html_page):
        data_map = {"reactants": None, "products": None, "rate_reaction": None}
        for element in html_page.find_all('b'):
            if element.a:
                reaction_equation = element.text.split()
                index = reaction_equation.index('→')
                reactants = tuple(element for element in reaction_equation[0:index] if element != '+')
                products = tuple(element for element in reaction_equation[index+1::] if element != '+')
        try:
            data_map["reactants"] = reactants
            data_map["products"] = products
        except Exception as e:
            logging.error(e)

        for line in html_page.stripped_strings:
            if 'R =' in line:
                rate_reaction = line.split()[2]
                data_map["rate_reaction"] = rate_reaction
                break
        logging.info("out from html_navigate")
        return data_map

    @staticmethod
    def send_key(link, react_name):
        logging.info("entreing send key")
        try:
            browser = webdriver.Firefox(executable_path="./geckodriver")
            browser.get(link)
            browser.find_element_by_name("text1").send_keys(react_name)
            browser.find_element_by_xpath("//input[@type='submit']").click()
            try:
                record_number = browser.find_element_by_name("nRec").get_attribute("value")
                logging.info("{0} results founded for {1}".format(record_number, react_name))
            except:
                logging.error("No match founded in data base for", react_name)
            reactions_tag_name = browser.find_elements_by_tag_name("a")
            filter_function = lambda anchor_tag: "matched" in anchor_tag.text
            reactions_web_element = list(filter(filter_function, reactions_tag_name))
            reactions_web_links = [element.get_attribute("href") for element in reactions_web_element]
            return reactions_web_links, record_number
        except Exception as error:
            logging.error(error)

        finally:
            browser.quit()
            logging.info("closing browser from sending key")

    @staticmethod
    def html_parse(reactions_web_element):
        logging.info("entreing html_parse")
        reactions_html = list()
        for element in reactions_web_element:
            html_page = ur.urlopen(element)
            soup = BeautifulSoup(html_page, 'html.parser')
            reactions_html.append(soup)
            logging.info("out from html_parse")
        return reactions_html
