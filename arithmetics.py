"""
Used for the creation of "questions" for the user,
along with the expected answer (that is, the result of the operation)

Some examples of "questions" and their "answers":

"+2-4" ,        "-2"
"(-2)(+7)",     "-14"
"-1.60-2.04",   "-3.64"

The program should be aimed specifically at teaching
the very basics of addition or multiplication of integers or decimals,
in a scaling difficulty.

Exercises that deviate from those specific concepts should be avoided.
Examples of what should NOT be implemented:

"2-4",          # Deviates (slightly) since it also teaches that 2 == +2
"-2(+7)",       # Deviates (same as example above)
"+2-4(-5)",     # Deviates since it combines addition and multiplication

"""


import decimal
import random
import languages


# ----------------------------------------------------------------------------------------------------------------------
DIFFICULTY_TO_TERMS_COUNT_AND_TYPE_MAP = {
    '1': {'terms_count': 2, 'terms_type': 'int', 'user_str': 'easy'},
    '2': {'terms_count': 3, 'terms_type': 'int', 'user_str': 'medium'},
    '3': {'terms_count': 2, 'terms_type': 'float', 'user_str': 'hard'}
}

TOTAL_DIFFICULTY_LVLS = len(DIFFICULTY_TO_TERMS_COUNT_AND_TYPE_MAP)


# ----------------------------------------------------------------------------------------------------------------------
class Terms(object):

    MIN_TERMS_COUNT = 2
    MAX_TERMS_COUNT = 3
    TERMS_TYPES = {'int', 'float'}
    MAX_ABS_VALUE = 10

    def __init__(self, difficulty_lvl):
        self.terms_count = DIFFICULTY_TO_TERMS_COUNT_AND_TYPE_MAP[difficulty_lvl]['terms_count']
        self.terms_type = DIFFICULTY_TO_TERMS_COUNT_AND_TYPE_MAP[difficulty_lvl]['terms_type']

    @staticmethod
    def _int_term(max_val=MAX_ABS_VALUE):
        return random.randint(0, max_val)

    @staticmethod
    def _float_term(max_val=MAX_ABS_VALUE):
        return random.random() * max_val

    @staticmethod
    def final_term(term_without_sign):
        """
        Creates a single term.

        :param term_without_sign:
        :return: (num)
        """
        sign = random.choice(['-', '+'])

        if sign == '-':
            final_term = -1 * term_without_sign
        else:
            final_term = term_without_sign

        return final_term

    def all_terms(self):
        lst = []

        if self.terms_type == 'int':
            func = self._int_term
        elif self.terms_type == 'float':
            func = self._float_term
        else:
            raise NotImplemented('{}'.format(self.terms_type))

        for _ in range(self.terms_count):
            term_without_sign = func()
            final_term = self.final_term(term_without_sign=term_without_sign)
            lst.append(final_term)

        return lst


class QuestionAndAnswer(object):
    """
    Based on difficulty and operation type,
    creates terms (either float or ints) which are then rounded to allow
    specific number of decimals.
    """

    OPERATIONS_TYPES = ('addition', 'multiplication')

    def __init__(self, difficulty_lvl, op_type):
        self.terms_as_numbers = Terms(difficulty_lvl=difficulty_lvl).all_terms()
        self.op_type = op_type

    @staticmethod
    def round_single_term_1_decimals(given_float):

        num = decimal.Decimal(str(given_float))
        return num.quantize(decimal.Decimal('.1'), decimal.ROUND_HALF_UP)

    def terms_to_rounded_numbers(self):
        """
        Ensures all terms have an appropriate number of decimals.

        :return: (list)
        """
        lst = []

        for t in self.terms_as_numbers:
            if not isinstance(t, int):
                t = self.round_single_term_1_decimals(given_float=t)

            lst.append(t)

        return lst

    def terms_as_strings(self):
        """
        Converts terms to strings.

        0 gets a random sign explicitly instead of using `{:+f}` for all terms' formatting
        since the latter can't achieve that.

        :return: (list)
        """
        lst = []

        for t in self.terms_to_rounded_numbers():

            if t > 0:
                lst.append('+{}'.format(t))
            elif t == 0:
                random_sign = random.choice(['+', '-'])
                # using abs() since sometimes a -0.0 can be given
                lst.append('{sign}{term}'.format(sign=random_sign, term=abs(t)))
            else:
                lst.append(str(t))

        return lst

    def operation_str(self):
        """
        Creates the operation string presented to the user.

        :return: (str)
        """

        terms_as_strings = self.terms_as_strings()

        if self.op_type == 'addition':
            # (whitespace between terms for better visibility)
            op_str = ' '.join(terms_as_strings)

        elif self.op_type == 'multiplication':
            op_str = ''
            for t in terms_as_strings:
                # (whitespace between terms for better visibility)
                if op_str:
                    op_str += ' '
                op_str += '({})'.format(t)

        else:
            raise NotImplemented('{}'.format(self.op_type))

        return op_str

    def expected_answer(self):

        if self.op_type == 'addition':
            result = 0
            for t in self.terms_to_rounded_numbers():
                result += t

        elif self.op_type == 'multiplication':
            result = 1
            for t in self.terms_to_rounded_numbers():
                result *= t

        else:
            raise NotImplemented('{}'.format(self.op_type))

        return result


if __name__ == '__main__':

    # VISUAL TESTS
    if 1:

        # --------------------------------------------------
        # all_terms()
        print('\n'+'-'*80)
        print('TERMS')

        def print_all_terms(difficulty_lvl):
            print('\nDifficulty {}'.format(difficulty_lvl))
            # (terms' lists printed for each difficulty lvl)
            terms_lsts_count = 3
            for _ in range(terms_lsts_count):
                print(Terms(difficulty_lvl=difficulty_lvl).all_terms())

        # (tests all difficulties)
        for d in range(1, TOTAL_DIFFICULTY_LVLS + 1):
            print_all_terms(difficulty_lvl=d)

        # --------------------------------------------------
        # operation_str() and answer
        print('\n'+'-'*80)
        print('OPERATION STRING')
        for d in range(1, TOTAL_DIFFICULTY_LVLS + 1):
            print('\nDifficulty: {}'.format(d))

            for operation in QuestionAndAnswer.OPERATIONS_TYPES:

                for _ in range(3):
                    inst = QuestionAndAnswer(difficulty_lvl=d, op_type=operation)
                    question = inst.operation_str()
                    answer = inst.expected_answer()
                    msg = '{q} = {a}'.format(q=question, a=answer)
                    print(msg)
