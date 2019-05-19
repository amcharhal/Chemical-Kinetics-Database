from automatedsearch import AutomatedSearch
from  testscrapping import  TestScrapping

import logging
logging.getLogger().setLevel(logging.INFO)





if __name__ == '__main__':
    website = 'https://kinetics.nist.gov/kinetics/index.jsp'
    react_name = " (CH3)3COOh"
    automated_search = AutomatedSearch(website, react_name)
    tests = TestScrapping()
    tests.run_tests()

    data = automated_search.search()
    print(data)
