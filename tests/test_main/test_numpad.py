from unittest import TestCase


class Test_apply_button_effects(TestCase):
    def setUp(self):
        from main import Numpad, NumpadBaseButton, DecimalSeparatorButton, ClearAnswerButton
        self.Numpad = Numpad
        self.dot_btn = DecimalSeparatorButton()
        self.minus_btn = NumpadBaseButton(text='-')
        self.clear_btn = ClearAnswerButton()

    def test_dot_on_empty_user_answer(self):
        inst = self.Numpad()
        inst.apply_button_effects(btn=self.dot_btn)
        self.assertEqual('0.', inst.user_answer)

    def test_dot_on_non_empty_user_answer(self):
        inst = self.Numpad()
        inst.user_answer = '-4'
        inst.apply_button_effects(btn=self.dot_btn)
        self.assertEqual('-4.', inst.user_answer)

    def test_dot_on_answer_with_existing_dot(self):
        inst = self.Numpad()
        inst.user_answer = '+4.3'
        inst.apply_button_effects(btn=self.dot_btn)
        self.assertEqual('+4.3', inst.user_answer)

    def test_minus_to_no_sign(self):
        inst = self.Numpad()
        inst.user_answer = '4.3'
        inst.apply_button_effects(btn=self.minus_btn)
        self.assertEqual('-4.3', inst.user_answer)

    def test_minus_to_minus(self):
        inst = self.Numpad()
        inst.user_answer = '-4.3'
        inst.apply_button_effects(btn=self.minus_btn)
        self.assertEqual('-4.3', inst.user_answer)

    def test_minus_to_plus(self):
        inst = self.Numpad()
        inst.user_answer = '+4.3'
        inst.apply_button_effects(btn=self.minus_btn)
        self.assertEqual('-4.3', inst.user_answer)

    def test_clear(self):
        inst = self.Numpad()
        inst.user_answer = '+4.3'
        inst.apply_button_effects(btn=self.clear_btn)
        self.assertEqual('', inst.user_answer)
