import unittest
from automatedsearch import AutomatedSearch
import urllib.request as ur
from bs4 import BeautifulSoup


class TestScrapping(unittest.TestCase):
    website = "https://kinetics.nist.gov/kinetics/index.jsp"
    react_name = "(CH3)3COOh"
    automated_search = AutomatedSearch(website, react_name)

    def run_tests(self):
        """ this function run test"""

        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        # add tests to the test suite
        suite.addTests(loader.loadTestsFromModule(self))
        # initialize a runner, pass it your suite and run it
        runner = unittest.TextTestRunner(verbosity=3)
        runner.run(suite)

    def test_search_length(self):
        size = len(self.automated_search.search())
        self.assertEqual(size, 19)

    def test_send_key_match(self):
        reactions_web_element, record_number = self.automated_search.send_key(self.website, self.react_name)
        self.assertEqual(len(reactions_web_element), 19)
        self.assertEqual(int(record_number), 39)

    def test_send_key_not_match(self):
        self.assertRaises(NameError, self.automated_search.send_key(self.website, "amcharhal"))

    def test_html_parse(self):
        link_elements = ['https://kinetics.nist.gov/kinetics/ReactionSearch?r0=7732185&r1='
                         '590389143&r2=0&r3=0&r4=0&p0=79414&p1=7732185&p2=7732185&p3=0&p4=0&'
                         'expandResults=true&']
        read = ur.urlopen(link_elements[0])
        soup = BeautifulSoup(read, 'html.parser')
        results = self.automated_search.html_parse(link_elements)[0]
        self.assertAlmostEqual(len(str(soup)), len(str(results)))

    def test_html_navigate(self):
        read = ur.urlopen("https://kinetics.nist.gov/kinetics/ReactionSearch?r0=7732185&r1=590389143&r2=0&r3=0&r4=0&p0=79414&p1=7732185&p2=7732185&p3=0&p4=0&expandResults=true&")
        soup = BeautifulSoup(read, 'html.parser')
        results = self.automated_search.html_navigate(soup)
        expected = {"reactants": ('H2O', 'CH2=C(CH3)-CH(OH)(OOH)'), "products": ('CH2=C(CH3)COOH', 'H2O', 'H2O'), "rate_reaction": str(8.314472)}
        self.assertEqual(results, expected)


