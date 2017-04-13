from random import choice as random
from json import dumps as prepared
title = "Квадратные уравнения (сложные)"
description = "Генерация приведенных квадратных уравнений и представление их в виде теста."

def generate(s):

    start_range = s['RANGE_OF_GENERATION'][0]
    end_range = s['RANGE_OF_GENERATION'][1]
    x1 = 0
    x2 = 0
    while x1 == 0 or x2 == 0:
        x1 = random(range(start_range, end_range))
        x2 = random(range(start_range, end_range))
    p = -(x1 + x2)
    if p == 1: p = "+x"
    elif p == -1: p = "-x"
    elif p > 0: p = str("+" + str(p) + "x")
    elif p == 0: p = ""
    else: p = str(p) + "x"
    q = x1*x2
    if q > 0: q = "+"+str(q)

    return prepared({
        "task": "$x^2"+str(p)+str(q)+"=0$",
        "answers": {
            "first_thread": {
                "placeholder": "Первый корень",
                "answer": list(map(str, [x1, x2]))
            },
            "second_thread": {
                "placeholder": "Второй корень",
                "answer": list(map(str, [x1, x2]))
            }
        },
    })
