from unittest import TestCase


class TestOpButton(TestCase):

    def test_op_types_match_expected(self):
        from arithmetics import QuestionAndAnswer
        from main import OpButton
        self.assertFalse(set(OpButton.OPERATION_TYPES_TO_DISPLAYED_STR_MAP) - set(QuestionAndAnswer.OPERATIONS_TYPES))
