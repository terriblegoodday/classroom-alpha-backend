from random import choice, randint
from sympy import solveset, symbols, latex, log, expand, Mul

class Expression:
    """
    Logarithmic expression data structure

    -@param repr<str>: string representation of expression-
    @param ex<Eq>: Equation representation of object to extend existing equation
    @param m<int>: integer representation of solved expression
    """

    def __init__(self, m, ex, repr=None):
    #    self.repr = repr
       self._ex = ex
       self.m = m

    # def __repr__(self):
    #     return self.repr

    def get_ex(self):
        return self._ex

def generate_log_expr():
    m = randint(0, 4)

    random_foundation = choice(range(2, 5))

    a = random_foundation ** m

    ex = log(a, random_foundation, evaluate=False)

    random_multiply = choice(range(2, 6))

    sign = choice([-1, 1])

    return Mul(Mul(sign, random_multiply), ex, evaluate=False)
