# -*- coding: utf-8 -*-

# Used for screenshots that match size of current screenshots in GooglePlay
if 0:
    from kivy.config import Config
    Config.set('graphics', 'width', '410')
    Config.set('graphics', 'height', '700')

from kivy.app import App
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.uix.label import Label as Label
from kivy.properties import ObjectProperty, DictProperty, NumericProperty, BooleanProperty, ListProperty, StringProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.clock import Clock
from kivy.uix.carousel import Carousel
from kivy import platform
from kivy.base import EventLoop

from functools import partial

import ast
import datetime
import copy

import arithmetics
import languages
import citations


__version__ = '1.5.7'

APP_NAME = 'MinusTimesMinus'


# ----------------------------------------------------------------------------------------------------------------------
THIRD_PARTIES_IMAGES_DIR = 'third_parties_images'
GOLD_COIN_SMALL_IM = '/'.join([THIRD_PARTIES_IMAGES_DIR, 'gold_coin_zeus_small.png'])
SILVER_COIN_IM_PATH = '/'.join([THIRD_PARTIES_IMAGES_DIR, 'athena_coin.png'])
COPPER_COIN_IM_PATH = '/'.join(['own_images', 'copper_coin.png'])


DIFF_TO_COIN_MAP = {
    '1': dict(
        coin_color='copper_coins',
        im_path=COPPER_COIN_IM_PATH
    ),
    '2': dict(
        coin_color='silver_coins',
        im_path=SILVER_COIN_IM_PATH
    ),
    '3': dict(
        coin_color='gold_coins',
        im_path=GOLD_COIN_SMALL_IM
    ),
}
# ----------------------------------------------------------------------------------------------------------------------
COLORS_TO_HEX_MAP = {
    'red': 'FF3232',
    'gold': 'FFAA00',
    'green': '00FF00',
    'blue': '1a1aff',
    'black': '000000'
}


def paint_text(text_str, color_str):
    """
    Adds markup around given text.
    Supports some colors by name instead of hexadecimal.

    :param text_str:
    :param color_str: (str) Hexadecimal or color name.
    :return: (str)
    """

    if color_str in COLORS_TO_HEX_MAP:
        color_str = COLORS_TO_HEX_MAP[color_str]

    return '[color={color_str}]{text_str}[/color]'.format(text_str=text_str,
                                                          color_str=color_str)


# ----------------------------------------------------------------------------------------------------------------------
class DropDownButton(Button):
    """
    Base class for dropdown containing buttons.

    Assumes dropdown container doesn't contain *boxes* with buttons,
    and that all buttons result in dropdown being closed.
    """
    def __init__(self, container_buttons_height_ratio=2., **kwargs):
        super(DropDownButton, self).__init__(**kwargs)
        self.container_buttons_height_ratio = container_buttons_height_ratio
        self.dropdown = DropDown()
        self.add_dropdown_contents()
        self.add_widget(self.dropdown)
        self.bind(on_release=self.dropdown.open)
        self.set_initial_dropdown_selection()
        self.dropdown.dismiss()

    def container_child_height(self):
        return self.container_buttons_height_ratio * self.height

    @property
    def container_children(self):
        return self.dropdown.container.children

    @property
    def first_button(self):
        return self.container_children[-1]

    def on_release(self, *args):
        super(DropDownButton, self).on_release(*args)
        for btn in self.container_children:
            btn.height = self.container_child_height()

    @staticmethod
    def content_button():
        """
        Returns instance of Button after applying specific params.

        :return: (Button instance)
        """
        return Button(size_hint_y=None,)

    def bind_to_on_release_and_add_container(self, btn):
        btn.bind(on_release=self.apply_on_release_effects)
        btn.bind(on_release=self.dropdown.dismiss)
        self.dropdown.add_widget(btn)

    # Abstract
    def add_dropdown_contents(self, *args):
        raise NotImplementedError

    # Abstract
    def apply_on_release_effects(self, btn):
        """
        Applies all `on_release` effects of a dropdown child
        excluding `dismiss`.

        :param btn: button instance
        :return: (None)
        """
        raise NotImplementedError

    # Abstract
    def set_initial_dropdown_selection(self):
        raise NotImplementedError


class OpButton(DropDownButton):

    OPERATION_TYPES_TO_DISPLAYED_STR_MAP = {
        'addition': 'Addition, subtraction',
        'multiplication': 'Multiplication'
    }

    operation_type = StringProperty()

    def __init__(self,  **kwargs):
        super(OpButton, self).__init__(**kwargs)

    def apply_on_release_effects(self, btn):
        self.operation_type = btn.operation_type
        self.text = btn.text

    def add_dropdown_contents(self):
        op_dct = self.OPERATION_TYPES_TO_DISPLAYED_STR_MAP
        for k in sorted(op_dct):
            v = op_dct[k]

            btn = self.content_button()
            self.bind_to_on_release_and_add_container(btn=btn)
            btn.operation_type = k
            btn.text = v

    def set_initial_dropdown_selection(self):
        self.apply_on_release_effects(btn=self.first_button)


class DifficultyButton(DropDownButton):

    difficulty_lvl = StringProperty()

    def add_dropdown_contents(self, *args):
        diff_dct = arithmetics.DIFFICULTY_TO_TERMS_COUNT_AND_TYPE_MAP
        for diff in sorted(diff_dct):

            btn = self.content_button()
            self.bind_to_on_release_and_add_container(btn=btn)
            btn.difficulty_lvl = diff
            btn.text = diff_dct[diff]['user_str']

    def apply_on_release_effects(self, btn):
        self.difficulty_lvl = btn.difficulty_lvl
        self.text = btn.text

    def set_initial_dropdown_selection(self):
        self.apply_on_release_effects(self.first_button)


class LanguageButton(DropDownButton):
    lang = StringProperty('english')

    def __init__(self,  **kwargs):
        super(LanguageButton, self).__init__(**kwargs)

    def add_dropdown_contents(self, *args):
        all_langs = languages.SUPPORTED_LANGUAGES
        for lang in sorted(all_langs):
            lang_obj = all_langs[lang]
            btn = self.content_button()
            self.bind_to_on_release_and_add_container(btn=btn)
            btn.lang_selected = lang
            btn.text = lang_obj.name_native

    def apply_on_release_effects(self, btn):
        self.text = btn.text
        self.lang = self.app.lang = btn.lang_selected

    def set_initial_dropdown_selection(self):
        self.text = languages.Message.selected_language


# ----------------------------------------------------------------------------------------------------------------------
class ConfinedTextLabel(Label):
    pass


# Class code below (including the corresponding in .kv file)
# by Alexander Taylor
# from https://github.com/kivy/kivy/wiki/Scrollable-Label
class ScrollLabel(ScrollView):
    pass


# ----------------------------------------------------------------------------------------------------------------------
class CoinImage(Image):
    DELAY = 1.
    ANIMATION_DURATION = .3

    def __init__(self, **kwargs):
        super(CoinImage, self).__init__(**kwargs)
        self.pos_hint = {'center_x': .5, 'center_y': .7}
        self.size_hint_x = .2


# ----------------------------------------------------------------------------------------------------------------------
class NumpadBaseButton(Button):
    def __init__(self, special_effect=None, **kwargs):
        super(NumpadBaseButton, self).__init__(**kwargs)
        self.special_effect = special_effect


class DecimalSeparatorButton(NumpadBaseButton):
    def __init__(self,  **kwargs):
        super(DecimalSeparatorButton, self).__init__(special_effect=Numpad.SEPARATOR_EFFECT_TXT, **kwargs)
        self.text = '.'     # Used for testing only; it's overwritten in kv


class ClearAnswerButton(NumpadBaseButton):
    def __init__(self,  **kwargs):
        super(ClearAnswerButton, self).__init__(special_effect=Numpad.CLEAR_ANSWER_EFFECT_TXT, **kwargs)


class CheckAnswerButton(NumpadBaseButton):
    CORRECT_TEXT = 'Correct!\nGood job.'
    CORRECT_TEXT = paint_text(text_str=CORRECT_TEXT, color_str='green')
    WRONG_TEXT = 'Are you sure?\nTry again.'
    WRONG_TEXT = paint_text(text_str=WRONG_TEXT, color_str='red')
    display_duration = CoinImage.ANIMATION_DURATION + CoinImage.DELAY

    user_answer = StringProperty()
    correct_answer_val = NumericProperty()
    user_answer_widget = ObjectProperty(Label())

    def __init__(self,  **kwargs):
        super(CheckAnswerButton, self).__init__(special_effect=Numpad.CHECK_ANSWER_EFFECT_TXT, **kwargs)

    def check_answer(self, given_a):
        if abs(given_a - self.correct_answer_val) < 1e-8:
            return True
        else:
            return False

    def set_answer_feed_label_text(self, answer_correctness, a_feed_label):
        if answer_correctness:
            txt = self.CORRECT_TEXT
        else:
            txt = self.WRONG_TEXT

        a_feed_label.text = txt
        Clock.schedule_once(lambda x: setattr(a_feed_label, 'text', ''), self.display_duration)

    def new_question(self, delay):
        Clock.schedule_once(self.q_display_obj.set_new_q_and_a, delay)
        Clock.schedule_once(self.numpad.reset_user_answer, delay)

    def apply_rewards(self):
        # Rewards for accuracy
        d = copy.deepcopy(self.app.store[self.op_type])
        d.update({self.difficulty_lvl: self.app.store[self.op_type][self.difficulty_lvl] + 1})
        self.app.store[self.op_type] = d
        self.app.store_answers['correct'] += 1

        # Rewards for consistency
        CheckRewardAndNote(store_visiting_dct=self.app.store_visiting).consecutive_days()

    def check_a_and_apply_effects(self, a_feed_label):
        if not self.user_answer:
            return
        try:
            given_a = ast.literal_eval(self.user_answer.strip('+'))
        except (ValueError, SyntaxError):
            return

        App.get_running_app().temp_disable_all_buttons(duration=self.display_duration)
        answer_correctness = self.check_answer(given_a=given_a)
        if answer_correctness:
            self.set_answer_feed_label_text(answer_correctness=answer_correctness, a_feed_label=a_feed_label)
            self.new_question(delay=self.display_duration)
            self.play_page.create_and_schedule_animation_gold_coin(diff_lvl=self.difficulty_lvl)
            self.apply_rewards()
        else:
            self.set_answer_feed_label_text(answer_correctness=answer_correctness, a_feed_label=a_feed_label)
            self.app.store_answers['wrong'] += 1


class Numpad(StackLayout):
    """
    Creates the numbers, comma and "check answer" buttons.
    """
    BUTTONS_SPACING = '2sp'
    CLEAR_ANSWER_EFFECT_TXT = 'CLEAR'  # This differs from button text because of different languages.
    CHECK_ANSWER_EFFECT_TXT = 'SUBMIT'
    SEPARATOR_EFFECT_TXT = 'SEPARATOR'
    # Max required numerical digits for any answer is 6;
    # more allowed so that user can test (wrong) answers having more digits.
    MAXIMUM_NUMERIC_DIGITS = 7
    user_answer = StringProperty()
    # TODO: reset user_answer on language change, otherwise it can cause minor bugs when checking below for separators

    def __init__(self,  **kwargs):
        super(Numpad, self).__init__(orientation='lr-tb', spacing=(self.BUTTONS_SPACING, self.BUTTONS_SPACING), **kwargs)
        self.add_contents()

    def reset_user_answer(self, *args):
        self.user_answer = ''

    def apply_button_effects(self, btn):
        btn_txt = btn.text

        # CLEAR ANSWER
        if btn.special_effect == self.CLEAR_ANSWER_EFFECT_TXT:
            self.reset_user_answer()
        # CHECK ANSWER
        elif btn.special_effect == self.CHECK_ANSWER_EFFECT_TXT:
            self.apply_check_solution_button()
        # SEPARATOR
        elif btn.special_effect == self.SEPARATOR_EFFECT_TXT:
            # Disallows second separator.
            if btn_txt in self.user_answer:
                return
            # Applies a '0' to the `user_answer` when no previous digit was given,
            # that is ''->'0' when first button pressed is a separator.
            if not self.user_answer.lstrip('+-'):
                self.user_answer += '0'
            self.user_answer += btn.text
        # PLUS, MINUS
        elif btn_txt in {'+', '-'}:
            # Applies sign to start of answer,
            # after removing previous sign (if any).
            self.user_answer = btn_txt + self.user_answer.lstrip('+-')
        # INTEGER
        else:
            if len(self.user_answer) < self.MAXIMUM_NUMERIC_DIGITS:
                self.user_answer += btn.text

    def number_or_sign_button(self, num_or_symbol):
        btn = NumpadBaseButton(text=str(num_or_symbol))
        btn.bind(on_release=self.apply_button_effects)
        return btn

    def decimal_separator_button(self):
        btn = DecimalSeparatorButton()
        btn.bind(on_release=self.apply_button_effects)
        return btn

    def clear_answer_button(self):
        btn = ClearAnswerButton()
        btn.bind(on_release=self.apply_button_effects)
        return btn

    def add_numbers(self):
        for n in xrange(1, 10):
            self.add_widget(self.number_or_sign_button(num_or_symbol=n))
        # ('0' comes after '9')
        self.add_widget(self.number_or_sign_button(num_or_symbol=0))

    def add_contents(self):
        self.add_widget(self.number_or_sign_button(num_or_symbol='-'))
        self.add_widget(self.number_or_sign_button(num_or_symbol='+'))
        self.add_widget(self.decimal_separator_button())
        self.add_widget(self.clear_answer_button())
        self.add_numbers()


# ----------------------------------------------------------------------------------------------------------------------
class RevealAnswerButton(Button):
    REVEAL_MODE = object()
    NEW_MODE = object()
    FUNCTIONALITY_MODES = {REVEAL_MODE, NEW_MODE}

    functionality_mode = ObjectProperty(REVEAL_MODE)

    def __init__(self,  **kwargs):
        super(RevealAnswerButton, self).__init__(**kwargs)

    def switch_functionality_to_new(self):
        self.functionality_mode = self.NEW_MODE
        self.text = 'New'
        self.background_color = 0,1,0,1

    def switch_functionality_to_reveal(self):
        self.functionality_mode = self.REVEAL_MODE
        self.text = 'Reveal'
        self.background_color = 1,0,0,1

    def switch_functionality(self):
        if self.functionality_mode is self.REVEAL_MODE:
            self.switch_functionality_to_new()
        else:
            self.switch_functionality_to_reveal()

    def apply_button_effects(self, *args):

        if self.functionality_mode is self.REVEAL_MODE:
            answer_in_red = paint_text(str(self.q_display.a_as_str()), 'red')
            self.a_feed_label.text = 'Correct answer is: {}'.format(answer_in_red)
            App.get_running_app().temp_disable_all_buttons(duration=None)
            self.disabled = False
            self.app.store_answers['skipped'] += 1

        else:
            App.get_running_app().enable_all_buttons()
            self.numpad.user_answer = ''
            self.a_feed_label.text = ''
            self.q_display.set_new_q_and_a()

        self.switch_functionality()


# ----------------------------------------------------------------------------------------------------------------------
class PlayPage(FloatLayout):

    def __init__(self,  **kwargs):
        super(PlayPage, self).__init__(**kwargs)

    def _start_coin_animation(self, _, coin_widg):
        animation = Animation(size_hint_x=.05, duration=CoinImage.ANIMATION_DURATION, t='in_out_quad')
        animation &= Animation(pos_hint=self.rewards_shortcut.pos_hint, duration=CoinImage.ANIMATION_DURATION, t='in_out_quad')
        animation.start(coin_widg)

    def _remove_widg(self, _, widg):
        self.remove_widget(widg)

    def create_and_schedule_animation_gold_coin(self, diff_lvl):
        im_path = DIFF_TO_COIN_MAP[str(diff_lvl)]['im_path']
        coin_im = CoinImage(source=im_path)
        self.add_widget(coin_im)
        Clock.schedule_once(
            partial(self._start_coin_animation, coin_widg=coin_im),
            CoinImage.DELAY)
        Clock.schedule_once(
            partial(self._remove_widg, widg=coin_im),
            CoinImage.DELAY + CoinImage.ANIMATION_DURATION)


# ----------------------------------------------------------------------------------------------------------------------
class QuestionDisplay(Label):
    difficulty_lvl = StringProperty('1')
    op_type = StringProperty(arithmetics.QuestionAndAnswer.OPERATIONS_TYPES[0])
    question_str = StringProperty()
    correct_answer_val = NumericProperty()

    def __init__(self, **kwargs):
        super(QuestionDisplay, self).__init__(text='', **kwargs)
        self.set_new_q_and_a()

    def new_q_and_a(self):
        inst = arithmetics.QuestionAndAnswer(difficulty_lvl=self.difficulty_lvl, op_type=self.op_type)
        q = inst.operation_str()
        a = inst.expected_answer()
        return q, a

    def set_new_q_and_a(self, *args):
        self.question_str, val = self.new_q_and_a()
        # NumericProperty doesn't accept Decimal,
        # and int answers should not be displayed as float in order to avoid confusing the user.
        if arithmetics.DIFFICULTY_TO_TERMS_COUNT_AND_TYPE_MAP[self.difficulty_lvl]['terms_type'] == 'int':
            pass
        else:
            val = (float(val))
        self.correct_answer_val = val

    def a_as_str(self):
        if self.correct_answer_val < 0:
            return str(self.correct_answer_val)
        else:
            return '+{}'.format(self.correct_answer_val)

# ----------------------------------------------------------------------------------------------------------------------
# List containing all wreath-rewards.
# Wreath-images that are used to display total wreaths earned,
# should not be stored here.
wreaths_lst = []


class WreathImage(Image):
    goal_complete = BooleanProperty(False)

    def __init__(self, store_in_wreath_list=True, **kwargs):
        super(WreathImage, self).__init__(**kwargs)
        if store_in_wreath_list:
            wreaths_lst.append(self)


class AllWreaths(BoxLayout):

    def __init__(self, **kwargs):
        super(AllWreaths, self).__init__(**kwargs)
        # (ensure enough time for creation of all wreaths before checking them)
        Clock.schedule_once(self.set_wreaths_lst_as_children, 1.5)

    def set_wreaths_lst_as_children(self, *args):
        # (old wreath controls the new wreath)
        for wreath in wreaths_lst:
            new_wreath = WreathImage(store_in_wreath_list=False)
            new_wreath.goal_complete = wreath.goal_complete
            wreath.linked_wreath = new_wreath
            wreath.bind(goal_complete=lambda old_l_self, val: setattr(old_l_self.linked_wreath, 'goal_complete', val))

            self.ids.wreaths_images_box.add_widget(new_wreath)

    def on_wreaths_lst(self, *args):
        for l in self.wreaths_lst:
            self.ids.wreaths_images_box.add_widget(l)


class MyProgressBar(Widget):
    filled_ratio = NumericProperty(.01)
    empty_ratio = NumericProperty(.01)


class CitationsBox(GridLayout):
    def __init__(self, **kwargs):
        super(CitationsBox, self).__init__(cols=2, **kwargs)
        self.create_citations()

    def create_citations(self):
        for im_file_name, citation_obj in citations.FIRST_IMAGE_TO_CITATION_MAP.items():
            im_widg = Image(source='/'.join([THIRD_PARTIES_IMAGES_DIR, im_file_name]),
                            size_hint=(.3,.3))
            self.add_widget(im_widg)
            self.add_widget(ConfinedTextLabel(text=citation_obj.full_text()))


# ----------------------------------------------------------------------------------------------------------------------
class CheckRewardAndNote(object):
    """Contains methods that CHECK if an action should REWARD the user,
    and NOTE his progress. Rewards are only noted;
    `on_store` triggers various rewards in their respective code-location.

    Only public methods of this class should be called
    since they incorporate full functionality (including e.g. checks).
    """
    _DAYS_TO_ACHIEV_NAME_MAP = {
        5: 'achiev_5_days',
        10: 'achiev_10_days',
        30: 'achiev_30_days',
    }

    def __init__(self, store_visiting_dct):
        self.store_visit_dct = store_visiting_dct
        self.days_achiev_dct = {
            days: self.store_visit_dct[name] for days, name in self._DAYS_TO_ACHIEV_NAME_MAP.items()}
        self.days_diff = self._days_from_previous_play()

    def set_consecutive_days(self, *args):
        if self.days_diff > 1:
            self.store_visit_dct['consecutive_days'] = 0

    def _check_and_apply_consecutive_days_achievs(self):
        for days, achiev_name in self._DAYS_TO_ACHIEV_NAME_MAP.items():

            # Already achieved
            achiev_val = self.days_achiev_dct[days]
            if achiev_val:
                continue

            # Check if requirements are fulfilled
            if self.store_visit_dct['consecutive_days'] == days:
                self.store_visit_dct[achiev_name] = 1
                # E.g. if (exactly) 20 days are complete,
                # then no point in checking for 10 or 30, etc.
                return

    def _days_from_previous_play(self):
        curr_d = datetime.date.today()
        prev_d_as_iso_str = self.store_visit_dct['last_day']
        if prev_d_as_iso_str:
            date_lst = prev_d_as_iso_str.split('-')
            date_lst = [int(i) for i in date_lst]
            prev_d = datetime.date(*date_lst)
            return (curr_d - prev_d).days
        else:
            # During reset last_day played becomes 0,
            # therefor the played "hasn't played" recently.
            return 999

    def consecutive_days(self):
        if all(self.days_achiev_dct.values()):
            return

        if self.days_diff == 0:
            return
        elif self.days_diff == 1:
            self.store_visit_dct['consecutive_days'] += 1
            self._check_and_apply_consecutive_days_achievs()
        else:
            # (minimum value is 1, not 0)
            self.store_visit_dct['consecutive_days'] = 1

        self.store_visit_dct['last_day'] = datetime.date.today().isoformat()


# ----------------------------------------------------------------------------------------------------------------------
class ResetRewardsButton(Button):
    def __init__(self, **kwargs):
        super(ResetRewardsButton, self).__init__(text='RESET', background_color=(1,0,0,1), **kwargs)
        self.popup_widg = None

    def create_popup(self, *args):
        self.popup_widg = Popup(title='[b]Reset everything?[/b] \n(this can [b]not[/b] be undone)',
                                size_hint=[.9, .3], separator_color=(0, 0, 0, 0))
        yes_button = Button(text='YES', background_color=[1, 0, 0, 1])
        yes_button.bind(on_release=self.popup_widg.dismiss)
        yes_button.bind(on_release=self.app.reset_store)
        no_button = Button(text='NO', background_color=[0, 2, 0, 1])
        no_button.bind(on_release=self.popup_widg.dismiss)
        popup_box = BoxLayout()
        popup_box.add_widget(yes_button)
        popup_box.add_widget(no_button)
        self.popup_widg.add_widget(popup_box)

    def on_release(self, *args):
        if not self.popup_widg:
            self.create_popup()
        self.popup_widg.open()


# ----------------------------------------------------------------------------------------------------------------------
class MemoRule(BoxLayout):
    # TODO refactor
    D = {
        'addition': {
            'english': 'When [b]adding[/b] two numbers:',
            'greek': u'Όταν [b]προσθέτεις[/b] δύο αριθμούς:'},
        'multiplication': {
            'english': 'When [b]multiplying[/b] two numbers:',
            'greek': u'Όταν [b]πολλαπλασιάζεις[/b] δύο αριθμούς:'},
        'add_same_sign': {
            'english': '[b]Same[/b] sign:\n\n\n[b]Keep[/b] sign\nand\n[b]Add[/b] them.',
            'greek': u'[b]Ίδιο[/b] πρόσημο:\n\n\n[b]Κρατάμε[/b] πρόσημο\nκαι\n[b]Προσθέτουμε[/b] \nτους αριθμούς.'},
        'add_diff_sign': {
            'english': '[b]Different[/b] sign:\n\n\nSign of [b]biggest[/b] number\nand\n[b]Subtract[/b] them.',
            'greek': u'[b]Διαφορετικό[/b] πρόσημο:\n\n\nπρόσημο [b]μεγαλυτέρου[/b] \nκαι\n[b]Αφαιρούμε[/b] \nτους αριθμούς.'},
        'mult_same_sign': {
            'english': '[b]Same[/b] sign:\n\n\n[b]Plus[/b] sign\nand\nMultiply them.',
            'greek': u'[b]Ίδιο[/b] πρόσημο:\n\n\n[b]Συν[/b] πρόσημο\nκαι\nΠολ/σιάζουμε \nτους αριθμούς.'},
        'mult_diff_sign': {
            'english': '[b]Different[/b] sign:\n\n\n[b]Minus[/b] sign\nand\nMultiply them.',
            'greek': u'[b]Διαφορετικό[/b] πρόσημο:\n\n\n[b]Πλην[/b] πρόσημο\nκαι\nΠολ/σιάζουμε \nτους αριθμούς.'}
    }

    def f(self, lang, txt_name):
        lang = lang or 'english'    # (lang is empty on initiation)
        return self.D[txt_name][lang]


# ----------------------------------------------------------------------------------------------------------------------
class MainWidget(Carousel):
    lang = StringProperty()

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        CheckRewardAndNote(store_visiting_dct=self.app.store_visiting).set_consecutive_days()


# ----------------------------------------------------------------------------------------------------------------------
DEFAULT_STORAGE_CONTENTS = {
    "multiplication": {"1": 0,
                       "3": 0,
                       "2": 0},
    "addition": {"1": 0,
                 "3": 0,
                 "2": 0},
    "answers": {"wrong": 0,
                "skipped": 0,
                "correct": 0},
    "visiting": {"achiev_10_days": 0,
                 "last_day": 0,
                 "consecutive_days": 0,
                 "achiev_30_days": 0,
                 "achiev_5_days": 0}}


class MinusTimesMinusApp(App):
    CONFIG_DEFAULTS = (
            ('language', {
                'selected_lang': languages.Message.DEFAULT_LANGUAGE,
            }),
        )

    # "store" is a DictProperty-copy of the actual store,
    # since as an ObjectProperty it wasn't tracking changes.
    store = DictProperty()
    # DictProperties are shallow copies,
    # so a separate property is needed in order to fire callbacks
    # (since nested value-changes are ignored)
    store_visiting = DictProperty()
    store_answers = DictProperty()
    total_coins = NumericProperty()
    buttons_disabled = BooleanProperty(False)
    lang = StringProperty()

    def __init__(self, **kwargs):
        super(MinusTimesMinusApp, self).__init__(**kwargs)

        # Storage file is checked/stored in different dir on androids
        # to avoid overwriting it during updates.
        storage_file = 'storage.json'
        if platform == 'android':
            storage_file = '/'.join([str(self.user_data_dir), storage_file])
        elif platform in ('ios', 'win'):
            raise NotImplementedError('Platform not implemented. Storage will be overridden on updates.')
        self.storage_file = storage_file
        self._store = JsonStore(storage_file)
        if not self._store:
            for k, v in DEFAULT_STORAGE_CONTENTS.items():
                self._store[k] = copy.deepcopy(v)

        self.store = copy.deepcopy(self._store._data)
        # DictProperties are shallow copies,
        # so a separate property is needed in order to fire callbacks
        # (since nested value-changes are ignored)
        self.store_visiting = copy.deepcopy(self._store._data['visiting'])
        self.store_answers = copy.deepcopy(self._store._data['answers'])

    def on_pause(self, *args):
        return True

    def on_start(self):
        EventLoop.window.bind(on_keyboard=self.keyboard_callback)

    def keyboard_callback(self, window, key, *args):
        if (platform() == 'android') and (key == 27):
            self.main_widg.load_previous()
            return True

    def set_tot_coins(self):
        tot = 0
        for op_type in arithmetics.QuestionAndAnswer.OPERATIONS_TYPES:
            for diff_lvl in DIFF_TO_COIN_MAP:
                tot += self.store[op_type][diff_lvl]
        self.total_coins = tot

    def update__store(self):
        for k1 in self.store:
            # (`update` doesn't work on Storage objects,
            # so a temp dict is used instead)
            temp_d = {}
            for k2, v in self.store[k1].items():
                temp_d.update({k2: v})
            self._store[k1] = temp_d

    def on_store_visiting(self, *args):
        self.store['visiting'] = self.store_visiting

    def on_store_answers(self, *args):
        self.store['answers'] = self.store_answers

    def on_store(self, *args):
        self.set_tot_coins()
        self.update__store()

    def reset_store(self, *args):
        dct = copy.deepcopy(self._store._data)
        for k1, d in dct.items():
            for k2 in d:
                dct[k1][k2] = 0
        self.store = dct
        self.store_visiting = dct['visiting']
        self.store_answers = dct['answers']

    def enable_all_buttons(self, *args):
        self.buttons_disabled = False

    def temp_disable_all_buttons(self, duration):
        """
        Disables temporarily all buttons.
        If duration is None, it doesn't re-enable them.
        """
        self.buttons_disabled = True
        if duration is None:
            return
        Clock.schedule_once(self.enable_all_buttons, duration)

    def on_lang(self, *args):
        self.config.set('language', 'selected_lang', self.lang)
        self.config.write()

    def tr(self, dct):
        """
        Returns the text corresponding to the selected language.
        :param dct: (dict) Languages as str keys, texts values.
        :return: (str)
        """
        return dct[self.app.lang]

    def build_config(self, config):
        for pair in self.CONFIG_DEFAULTS:
            config.setdefaults(*pair)

    def build(self):

        self.main_widg = MainWidget()
        self.main_widg.lang = self.config.get('language', 'selected_lang')
        self.set_tot_coins()
        return self.main_widg


if __name__ == '__main__':

    try:
        import IGNORE_BUILD_ensure_images_cited
    except ImportError:
        pass

    MinusTimesMinusApp().run()
