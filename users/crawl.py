import sys
import time
import re
import requests
import os.path
from bs4 import BeautifulSoup

MAX_CRAWL = 5
SLEEP_MINUTE = 1


def crawl():
    crawl_acm()
    crawl_oi()


cur_dir = os.path.dirname(os.path.realpath(__file__))

def crawl_acm(last_crawled=None):

    INPUT_FILE = os.path.join(cur_dir, '../problems/acm.txt')
    OUTPUT_FILE = os.path.join(cur_dir, 'ranks/acm/')
    RANK_URL = 'http://vn.spoj.com/ranks/'
    SUBMISSION_PER_PAGE = 20


    def crawl_page(page):

        print '   page', page
        start = SUBMISSION_PER_PAGE * page
        url = RANK_URL + problem_id + '/start=' + str(start)

        request = requests.get(url)
        if request.status_code != 200:
            print 'Unable to crawl problem', problem_id

        html = BeautifulSoup(request.text)
        elements = html.select('td[class="status_sm"]')

        users = set()
        cnt = 0

        for element in elements:
            submission = element.next.next.next
            text = submission.__str__()
            submission_re = re.compile(r'.*href="\/users\/(?P<id>[a-z][a-z0-9_]*)\/.*').match(text)

            if submission_re:
                user_id = submission_re.groupdict()['id']
                users |= {user_id}
                cnt += 1
            else:
                print 'Regex error', text

        return users, cnt


    input_file = open(INPUT_FILE, 'r')
    cnt_crawl = 0
    while True:
        problem_id = input_file.readline()
        if not problem_id:
            break

        if last_crawled and problem_id <= last_crawled:
            continue

        # Remove endline character
        problem_id = problem_id[0:-1]
        page = 0
        users_solved = set()
        print 'Crawling problem', problem_id

        while True:
            users, cnt = crawl_page(page)
            users_solved |= users
            if cnt < SUBMISSION_PER_PAGE:
                break
            page += 1

        # Write to file
        output_file = open(OUTPUT_FILE + problem_id + '.txt', 'w')
        for user in users_solved:
            output_file.write(user + '\n')

        cnt_crawl += 1
        if cnt_crawl == MAX_CRAWL:
            print "Sleep"
            cnt_crawl = 0
            sys.stdout.flush()
            time.sleep(60 * SLEEP_MINUTE)


def crawl_oi(last_crawled=None):

    INPUT_FILE = os.path.join(cur_dir, '../problems/oi.txt')
    OUTPUT_FILE = os.path.join(cur_dir, 'ranks/oi/')
    RANK_URL = 'http://vn.spoj.com/ranks/'
    SUBMISSION_PER_PAGE = 20


    def crawl_page(page):

        print '   page', page
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

            try:
                score = str(score.text)
                score = score.replace('\n', '')
                score = score.replace('\t', '')
                space_index = score.find(' ')
                if space_index > -1:
                    score = score[:space_index]
                score = float(score)
            except Exception as e:
                print e
                continue

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


    input_file = open(INPUT_FILE, 'r')
    cnt_crawl = 0
    while True:
        problem_id = input_file.readline()
        if not problem_id:
            break

        if last_crawled and problem_id <= last_crawled:
            continue

        # Remove endline character
        problem_id = problem_id[0:-1]
        page = 0
        users_solved = {}
        print 'Crawling problem', problem_id

        while True:
            users, user_count = crawl_page(page)
            stop = False

            for user in users:
                if not user in users_solved:
                    users_solved[user] = users[user]

                if users[user] == 0:
                    stop = True

            if user_count < SUBMISSION_PER_PAGE or stop:
                break

            page += 1

        # Sort by score
        users_solved_list = []
        for user in users_solved:
            users_solved_list += [(users_solved[user], user)]
        users_solved_list.sort()
        users_solved_list = users_solved_list[::-1]

        # Write to file
        output_file = open(OUTPUT_FILE + problem_id + '.txt', 'w')
        for user in users_solved_list:
            output_file.write(user[1] + ' ' + str(user[0]) + '\n')

        cnt_crawl += 1
        if cnt_crawl == MAX_CRAWL:
            cnt_crawl = 0
            print "Sleep"
            sys.stdout.flush()
            time.sleep(60 * SLEEP_MINUTE)


if __name__ == '__main__':
    crawl()
