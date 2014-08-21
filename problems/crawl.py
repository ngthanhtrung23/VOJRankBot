import re
import requests
from bs4 import BeautifulSoup

def crawl():
    crawl_category('acm')
    crawl_category('oi')

def crawl_category(category):
    OUTPUT_FILE = category +'.txt'
    URL = 'http://vn.spoj.com/problems/' + category
    PROBLEMS_PER_PAGE = 50

    page = 0
    problems = []

    while True:
        print 'Crawling page', page

        start = page * PROBLEMS_PER_PAGE
        url = URL + '/sort=0,start=' + str(start)

        request = requests.get(url)
        if request.status_code != 200:
            print 'Unable to crawl page', page
            continue

        html = BeautifulSoup(request.text)
        elements = html.select('tr[class="problemrow"]')

        for element in elements:
            text = element.__str__().replace('\n', ' ')
            problem_re = re.compile(r'.*href="\/problems\/(?P<id>[A-Z][A-Z0-9_]{1,7})\/.*').match(text)

            if problem_re:
                problems += [problem_re.groupdict()['id']]
            else:
                print 'Regex error', text

        # Last page
        if len(elements) < PROBLEMS_PER_PAGE:
            break

        page += 1

    problems.sort()
    output_file = open(OUTPUT_FILE, 'w')
    for problem in problems:
        output_file.write(problem + '\n')

crawl()
