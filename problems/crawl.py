import re
import requests
import os.path
from bs4 import BeautifulSoup


def crawl():
    crawl_problemset('acm')
    crawl_problemset('oi')


def crawl_problemset(problemset):

    OUTPUT_FILE = problemset +'.txt'
    URL = 'http://vn.spoj.com/problems/' + problemset
    PROBLEMS_PER_PAGE = 50


    def crawl_page(page):

        print 'Page', page
        start = page * PROBLEMS_PER_PAGE
        url = URL + '/sort=0,start=' + str(start)

        request = requests.get(url)
        if request.status_code != 200:
            print 'Unable to crawl page', page
            return []

        html = BeautifulSoup(request.text)
        elements = html.select('tr[class="problemrow"]')
        problems = []

        for element in elements:
            text = element.__str__().replace('\n', ' ')
            problem_re = re.compile(r'.*href="\/problems\/(?P<id>[A-Z][A-Z0-9_]{1,7})\/.*').match(text)

            if problem_re:
                problems += [problem_re.groupdict()['id']]
            else:
                print 'Regex error', text

        return problems


    page = 0
    problems = []
    print 'Crawling problemset:', problemset

    while True:
        new_problems = crawl_page(page)
        problems += new_problems

        if len(new_problems) < PROBLEMS_PER_PAGE:
            break

        page += 1

    # Write to file
    problems.sort()
    full_output_path = os.path.join( os.path.dirname(os.path.realpath(__file__)), OUTPUT_FILE)
    print "Output to " + full_output_path
    output_file = open(full_output_path, 'w')
    for problem in problems:
        output_file.write(problem + '\n')

    return problems


crawl()
