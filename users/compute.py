

def compute_acm():

    def compute_acm_problem(problem):
        print 'Computing', problem
        rank_file = open('ranks/acm/' + problem + '.txt', 'r')

        users = []
        while True:
            user = rank_file.readline()
            if not user:
                break
            users += [user[0:-1]]

        return users

    problem_file = open('../problems/acm.txt', 'r')
    problems = []
    while True:
        problem = problem_file.readline()
        if not problem:
            break
        problems += [problem[0:-1]]

    user_scores = {}

    for problem in problems:
        users = compute_acm_problem(problem)
        score = 80.0 / (40 + len(users))
        print 'Solved =', len(users), 'Score = ', score
        for user in users:
            if not user in user_scores:
                user_scores[user] = 0.0
            user_scores[user] += score

    user_scores_list = []
    for user in user_scores:
        user_scores_list += [(user_scores[user], user)]

    user_scores_list.sort()
    user_scores_list = user_scores_list[::-1]
    output_file = open('rank-acm.txt', 'w')
    for user in user_scores_list:
        text = user[1]
        while len(text) < 20:
            text += ' '
        text += str(round(user[0], 1)) + '\n'
        output_file.write(text)

    output_file.close()


def compute_oi():

    def compute_oi_problem(problem):
        print 'Computing', problem
        rank_file = open('ranks/oi/' + problem + '.txt', 'r')

        users = {}
        ac_count = 0
        while True:
            line = rank_file.readline().split()
            if not line:
                break

            user = line[0]
            score = float(line[1])
            if score == 100:
                ac_count += 1
            users[user] = score

        return users, ac_count

    problem_file = open('../problems/oi.txt', 'r')
    problems = []
    while True:
        problem = problem_file.readline()
        if not problem:
            break
        problems += [problem[0:-1]]

    user_scores = {}

    for problem in problems:
        users, ac_count = compute_oi_problem(problem)
        score = 80.0 / (40 + ac_count)
        print 'Solved =', ac_count, 'Score = ', score
        for user in users:
            if not user in user_scores:
                user_scores[user] = 0.0
            user_scores[user] += score * users[user] / 100.0

    user_scores_list = []
    for user in user_scores:
        user_scores_list += [(user_scores[user], user)]

    user_scores_list.sort()
    user_scores_list = user_scores_list[::-1]
    output_file = open('rank-oi.txt', 'w')
    for user in user_scores_list:
        text = user[1]
        while len(text) < 20:
            text += ' '
        text += str(round(user[0], 1)) + '\n'
        output_file.write(text)

    output_file.close()


def merge():
    acm_rank_file = open('rank-acm.txt', 'r')
    oi_rank_file = open('rank-oi.txt', 'r')

    user_scores = {}

    while True:
        line = acm_rank_file.readline().split()
        if not line:
            break

        user = line[0]
        score = float(line[1])

        if not user in user_scores:
            user_scores[user] = 0.0
        user_scores[user] += score

    while True:
        line = oi_rank_file.readline().split()
        if not line:
            break

        user = line[0]
        score = float(line[1])

        if not user in user_scores:
            user_scores[user] = 0.0
        user_scores[user] += score


    user_scores_list = []
    for user in user_scores:
        user_scores_list += [(user_scores[user], user)]

    user_scores_list.sort()
    user_scores_list = user_scores_list[::-1]
    output_file = open('rank.txt', 'w')
    index = 1
    for user in user_scores_list:
        # text = str(index) + '. ' + user[1]
        text = user[1] + ', '
        # while len(text) < 20:
        #     text += ' '
        text += str(round(user[0], 1)) + '\n'
        output_file.write(text)
        index += 1

    output_file.close()



compute_acm()
compute_oi()
merge()

