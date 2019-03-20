from unittest import TestCase


class TestQuestion(TestCase):

    def setUp(self):

        from decimal import Decimal
        from arithmetics import QuestionAndAnswer
        from arithmetics import DIFFICULTY_TO_TERMS_COUNT_AND_TYPE_MAP

        self.positive_float_to_expected_1st_decimal_rounded = {
            0.0049: Decimal('0.0'),
            0: Decimal('0'),
            0.005: Decimal('0.0'),
            2.255: Decimal('2.3'),
            9.999: Decimal('10'),
            0.004: Decimal('0'),
        }

        self.negative_float_to_expected_2nd_decimal_rounded = {
            -k: -v for k, v in self.positive_float_to_expected_1st_decimal_rounded.items()}

        self.QuestionAndAnswer = QuestionAndAnswer
        self.DIFF_DCT = DIFFICULTY_TO_TERMS_COUNT_AND_TYPE_MAP

    def test_positive_round_single_term_2_decimals(self):

        for given_float, expected in self.positive_float_to_expected_1st_decimal_rounded.items():
            self.assertEqual(self.QuestionAndAnswer.round_single_term_1_decimals(given_float=given_float), expected)

    def test_negative_round_single_term_2_decimals(self):

        for given_float, expected in self.negative_float_to_expected_2nd_decimal_rounded.items():
            self.assertEqual(self.QuestionAndAnswer.round_single_term_1_decimals(given_float=given_float), expected)

    def test_sings_count_in_multiplication(self):
        for d in self.DIFF_DCT:
            for _ in xrange(10000):
                inst = self.QuestionAndAnswer(difficulty_lvl=d, op_type='multiplication')
                question = inst.operation_str()
                signs_in_q = question.count('+') + question.count('-')

                self.assertEqual(signs_in_q, self.DIFF_DCT[d]['terms_count'])