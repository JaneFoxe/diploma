import requests


from func import db_manager


def parsing_code():
    db = db_manager.DBManager()
    response = requests.get("https://codeforces.com/api/problemset.problems").json()
    problems = response["result"]["problems"]
    problemstatistics = response["result"]["problemStatistics"]

    # обновляем в базе задачи
    for problem in problems:
        if 'rating' in problem:
            rating = problem['rating']
        else:
            rating = 0

        db.db_update_problem(problem['contestId'], problem['index'], problem['name'], rating, problem["tags"])

    # добавляем в базу задачи
    for problem in problems:
        if 'rating' in problem:
            rating = problem['rating']
        else:
            rating = 0
        url = f"https://codeforces.com/problemset/problem/{problem['contestId']}/{problem['index']}"

        db.db_add_problem(problem['contestId'], problem['index'], problem['name'], url, rating, problem["tags"])
        for tag in problem["tags"]:
            db.db_add_tag(problem['contestId'], problem['index'], tag)

    # обновляем задачи
    for ps in problemstatistics:
        db.db_add_problem_solvedcount(ps['contestId'], ps['index'], ps['solvedCount'])
