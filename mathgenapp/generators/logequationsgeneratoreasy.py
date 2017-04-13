from random import choice, randint
from json import dumps as prepared
from mathgenapp.generators.lib.generateLog import generate_log_expr
from sympy import Mul, Add, pprint, Eq, latex, evaluate, N

title = "Логарифмические выражения (простые)"
description = "Генерация простейших (не всегда ;) логарифмических выражений и представление их в виде теста.\
    \nПримечание: log(a, b) – логарифм a по основанию b."

def generate(s=None):

    number_of_parts = randint(1, 2) # Количество генерируемых частей
    multiply_factor = randint(1, 3) # Коэффициент уравнения

    parts = [ ] # Части выражения

    for _ in range(number_of_parts):
        parts.append(generate_log_expr())

    expr = Mul(multiply_factor, Add(*parts, evaluate=False), evaluate = False)

    return prepared({
        "task": "Найдите значение выражения: ${0}$. ".format(latex(expr)),
        "answers": {
            "eval": {
                "placeholder": "Значение выражения",
                "answer": [str(int(N(expr)))]
            }
        }
    })
