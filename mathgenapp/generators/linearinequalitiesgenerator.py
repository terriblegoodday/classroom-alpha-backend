from random import randint as random
from random import choice
from json import dumps as prepared
import logging
logger = logging.getLogger(__file__)
logger.warn('here be bugs')
title = "Линейные неравенства"
description = "ax+b<0, где a и b - любые числа, причем a!=0, а x - неизвестная переменная."

def generate(s):
    d_t = str()

    a = 0
    while a == 0:
        a = random(-15, 15)

    b = 0
    while not (int(b / a) == b / a) or b == 0 or b / a == 1 or b / a == -1:
        b = random(-60, 60)

    inequality = choice(['<', '>', '\geq', '\leq'])

    def reverse(x):
        if x == '<':
            c = '<'
            d_t = '>'
            return d_t
        if x == '>':
            c = '>'
            d_t = '<'
            return d_t
        if x == '\geq':
            c = '\geq'
            d_t = '\leq'
            return d_t
        if x == '\leq':
            c = '\leq'
            d_t = '\geq'
            return d_t
    if a < 0:
        d_t = reverse(inequality)
        
    else:
        d_t = inequality
            
    if d_t == '<':
        d_t = '<'
    if d_t == '>':
        d_t = '>'
    if d_t == '\geq': 
        d_t = '>='
    if d_t == '\leq': 
        d_t = '<='

    logger.warn("$" + str(a) + "x" + inequality + str(b) + "$. Введите решенное неравенство\
				без пробелов и\
					с x в левой части.")
    logger.warn(str(["x" + d_t + str(int(b/a)), "1"]))

    return prepared({
        "task": "$" + str(a) + "x" + inequality + str(b) + "$. Введите решенное неравенство\
				без пробелов и\
					с x в левой части.",
        "answers": {
            "inequality": {
                "placeholder": "Решенное неравенство",
                "answer": ["x" + d_t + str(int(b/a)), "1"]
            }
        }
    })
