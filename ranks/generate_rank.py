import os.path
import json

NTOP_USER = 1000
CUR_DIR = os.path.dirname(os.path.realpath(__file__))
FILE_DATA_JS = os.path.join(CUR_DIR, '..', 'publish', 'data.js')
FILE_RANK_USER = os.path.join(CUR_DIR, '..', 'users', 'rank.txt')
FILE_PROBLEM_ACM = os.path.join(CUR_DIR, '..', 'problems', 'acm.txt')
FILE_PROBLEM_OI = os.path.join(CUR_DIR, '..', 'problems', 'oi.txt')
FILE_PROBLEM_POINT_PATH_ACM = os.path.join(CUR_DIR, '..', 'users', 'ranks', 'acm')
FILE_PROBLEM_POINT_PATH_OI = os.path.join(CUR_DIR, '..', 'users', 'ranks', 'oi')

def load_user_rank():
    users = []
    with open(FILE_RANK_USER, 'r') as file_rank_user:
        for i in xrange(NTOP_USER):
            user, score = file_rank_user.readline().split()
            users += [[i + 1, user, '', score]]
    return users

def load_problem_list():
    problems = []
    cnt = 0
    with open(FILE_PROBLEM_ACM) as file_problem:
        lines = file_problem.readlines()
        for line in lines:
            l = line.strip()
            ac = 0
            with open(os.path.join(FILE_PROBLEM_POINT_PATH_ACM, l + ".txt")) as file:
                ac = len(file.read().split('\n'))
            cnt += 1
            problems += [[cnt, 'acm', l, '', ac, round(80.0 / (40.0 + ac), 2)]]
    with open(FILE_PROBLEM_OI) as file_problem:
        lines = file_problem.readlines()
        for line in lines:
            l = line.strip()
            ac = 0
            with open(os.path.join(FILE_PROBLEM_POINT_PATH_OI, l + ".txt")) as file:
                lines = file.readlines()
                for line in lines:
                    if (line.strip().endswith("100.0")):
                        ac += 1
            cnt += 1
            problems += [[cnt, 'oi', l, '', ac, round(80.0 / (40.0 + ac), 2)]]
    return problems

with open(FILE_DATA_JS, 'w') as file_data_js:
    file_data_js.write("rank_users = ")
    file_data_js.write(json.dumps(load_user_rank()))
    file_data_js.write('\n')
    file_data_js.write("problem_list = ")
    file_data_js.write(json.dumps(load_problem_list()))
