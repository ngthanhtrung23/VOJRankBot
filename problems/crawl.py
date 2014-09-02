import re
import requests
import os
from bs4 import BeautifulSoup


# def crawl():
#     crawl_problemset('acm')
#     crawl_problemset('oi')


def crawl_contest(contest='', problemsets=['acm', 'oi']):

    DEFAULT_URL = 'http://vn.spoj.com/'
    contest_url = DEFAULT_URL + contest
    contest_directory = os.path.dirname(os.path.realpath(__file__))

    def extract_problemsets():

        problems_url = contest_url + '/problems'
        request = requests.get(problems_url)
        if request.status_code != 200:
            print 'Unable to extract problemsets from', contest_url
            return []

        html = BeautifulSoup(request.text)
        elements = html.select('div[class="submenucmd"]')
        problemsets = []

        if elements:
            html = BeautifulSoup(elements[0].__str__())
            elements = html.select('a[href]')
            for element in elements:
                problemset = str(element.text)
                problemsets += [problemset]

        return problemsets

    if contest:
        contest_directory = os.path.join(contest_directory, contest)
        if not os.path.exists(contest_directory):
            os.makedirs(contest_directory)

        problemsets = extract_problemsets()

    def crawl_problemset(problemset):

        PROBLEMS_PER_PAGE = 50
        problemset_url = contest_url + '/problems/' + problemset

        def crawl_page(page):

            print 'Page', page
            start = page * PROBLEMS_PER_PAGE
            url = problemset_url + '/sort=0,start=' + str(start)

            request = requests.get(url)
            if request.status_code != 200:
                print 'Unable to crawl page', page
                return []

            html = BeautifulSoup(request.text)
            elements = html.select('tr[class="problemrow"]')
            problems = []

            for element in elements:
                text = element.__str__().replace('\n', ' ')
                problem_re = re.compile(r'.*\/problems\/(?P<id>[A-Z][A-Z0-9_]{1,7})\/.*').match(text)

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
        output_directory = os.path.join(contest_directory, problemset + '.txt')
        print "Output to " + output_directory
        output_file = open(output_directory, 'w')
        for problem in problems:
            output_file.write(problem + '\n')

        return problems

    for problemset in problemsets:
        crawl_problemset(problemset)


crawl_contest()
