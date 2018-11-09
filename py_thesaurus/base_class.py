import re
import urllib.error
from urllib.request import urlopen
from bs4 import BeautifulSoup
import sys


class WordAnalyzer():

    """ A class to fetch synonyms of a word from thesaurus.com
    using selenium or beautiful soup """

    def __init__(self, word):
        self.entry = word

    def check_not_null(self):
        """ Check if input is null"""
        temp = re.sub(r"\s+", " ", self.entry)
        temp = temp.strip()
        if temp != "":
            return True
        else:
            return False

    def get_synonym(self):
        """Fetches the synonyms from the thesaurus.com using Beautiful Soup"""
        try:
            if self.check_not_null():
                response = urlopen(
                    'http://www.thesaurus.com/browse/{}'.format(self.entry))
                html = response.read().decode('utf-8')
                soup = BeautifulSoup(html, 'lxml')
                result = []
                for element in soup.findAll('div', {'class': 'relevancy-list'}):
                    for sub_elem in element.findAll('span', {'class': 'text'}):
                        result.append(sub_elem.text)
                return result
            else:
                print("Provide a not-null input word")
                return []
        except urllib.error.HTTPError as err:
            if err.code == 404:
                print("Word is not valid")
                return []
        except urllib.error.URLError:
            print("No Internet Connection")
            return []
        except:
            print(sys.exc_info())
            return []

    def get_definition(self):
        """Fetches the definitions from the dictionary.com \
        using Beautiful Soup"""

        try:
            if self.check_not_null():
                response = urlopen(
                    'http://www.dictionary.com/browse/{}?s=t'.format(self.entry))
                html = response.read().decode('utf-8')
                soup = BeautifulSoup(html, 'lxml')
                result = []
                section = soup.select(
                    '#source-luna > div:nth-of-type(1) > section > div.source-data > \
                    div.def-list > section')[0]
                elements = section.select("> div.def-set > div.def-content")
                for elem in elements:
                    for remove in elem.findAll("div", {"class": "def-block \
                    def-inline-example"}):
                        remove.decompose()
                    temp = elem.text
                    temp = re.sub(r"\s+", " ", temp)
                    temp = temp.strip()
                    temp = temp.rstrip(":")
                    temp = temp.capitalize()
                    result.append(temp)
                if len(result) > 5:
                    return result[:5]
                else:
                    return result
            else:
                print("Provide a not-null input word")
                return []
        except urllib.error.HTTPError as err:
            if err.code == 404:
                print("Word is not valid")
                return []
        except IndexError:
            print("Give a non-empty argument")
            return []
        except urllib.error.URLError:
            print("No Internet Connection")
            return []
