import re
import requests
import os.path
from bs4 import BeautifulSoup


user_scores = {}
user_problems = {}


def crawl():
    crawl_acm()
    crawl_oi()


cur_dir = os.path.dirname(os.path.realpath(__file__))

def crawl_acm(last_crawled=None):
    INPUT_FILE = os.path.join(cur_dir, '../problems/acm.txt')
    OUTPUT_FILE = os.path.join(cur_dir, 'ranks/acm/')
    RANK_URL = 'http://vn.spoj.com/ranks/'
    SUBMISSION_PER_PAGE = 20

    input_file = open(INPUT_FILE, 'r')
    while True:
        problem_id = input_file.readline()
        if not problem_id:
            break

        if last_crawled and problem_id <= last_crawled:
            continue

        # Remove endline character
        problem_id = problem_id[0:-1]
        print 'Crawling problem', problem_id

        # Crawl each page of submissions
        def crawl_page(page):

            start = SUBMISSION_PER_PAGE * page
            url = RANK_URL + problem_id + '/start=' + str(start)

            request = requests.get(url)
            if request.status_code != 200:
                print 'Unable to crawl problem', problem_id

            html = BeautifulSoup(request.text)
            elements = html.select('td[class="status_sm"]')

            users = []

            for element in elements:
                submission = element.next.next.next
                text = submission.__str__()
                submission_re = re.compile(r'.*href="\/users\/(?P<id>[a-z][a-z0-9_]*)\/.*').match(text)

                if submission_re:
                    user_id = submission_re.groupdict()['id']
                    users += [user_id]
                else:
                    print 'Regex error', text

            return users

        page = 0
        users_solved = []

        while True:
            print '   page', page
            users = crawl_page(page)
            users_solved += users
            if len(users) < SUBMISSION_PER_PAGE:
                break
            page += 1

        print 'Total solved =', len(users_solved)
        problem_score = 80.0 / (40 + len(users_solved))
        print 'Score =', problem_score

        output_file = open(OUTPUT_FILE + problem_id + '.txt', 'w')
        for user in users_solved:
            output_file.write(user + '\n')


def crawl_oi(last_crawled=None):

    INPUT_FILE = os.path.join(cur_dur, '../problems/oi.txt')
    OUTPUT_FILE = os.path.join(cur_dir, 'ranks/oi/')
    RANK_URL = 'http://vn.spoj.com/ranks/'
    SUBMISSION_PER_PAGE = 20

    input_file = open(INPUT_FILE, 'r')
    while True:
        problem_id = input_file.readline()
        if not problem_id:
            break

        if last_crawled and problem_id <= last_crawled:
            continue

        # Remove endline character
        problem_id = problem_id[0:-1]
        print 'Crawling problem', problem_id

        # Crawl each page of submissions
        def crawl_page(page):

            start = SUBMISSION_PER_PAGE * page
            url = RANK_URL + problem_id + '/start=' + str(start)

            request = requests.get(url)
            if request.status_code != 200:
                print 'Unable to crawl problem', problem_id

            html = BeautifulSoup(request.text)
            elements = html.select('td[class="status_sm"]')

            users = {}

            for element in elements:
                submission = element.next.next.next
                score = submission.next.next.next

                score = str(score.text)
                score = score.replace('\n', '')
                score = score.replace('\t', '')
                space_index = score.find(' ')
                if space_index > -1:
                    score = score[:space_index]
                score = float(score)

                if score == 0:
                    continue

                text = submission.__str__()
                submission_re = re.compile(r'.*href="\/users\/(?P<id>[a-z][a-z0-9_]*)\/.*').match(text)

                if submission_re:
                    user_id = submission_re.groupdict()['id']
                    users[user_id] = score
                else:
                    print 'Regex error', text


            return users, len(elements)

        page = 0
        users_solved = []

        while True:
            print '   page', page
            users, user_count = crawl_page(page)

            for user in users:
                users_solved += [(users[user], user)]

            if user_count < SUBMISSION_PER_PAGE:
                break
            page += 1

        print 'Total solved =', len(users_solved)
        problem_score = 80.0 / (40 + len(users_solved))
        print 'Score =', problem_score

        # Sort by score
        users_solved.sort()
        users_solved = users_solved[::-1]

        output_file = open(OUTPUT_FILE + problem_id + '.txt', 'w')
        for user in users_solved:
            output_file.write(user[1] + ' ' + str(user[0]) + '\n')


crawl()
# for user in user_scores:
#     print user, user_scores[user], user_problems[user]
