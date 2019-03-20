# -*- coding: utf-8 -*-

# Multilingual support postpone indefinitely. Only Help has a language option.
# (Making `app` method that handles all strings that should contain property `lang` which comes from config",
# doesn't work either because `app` doesn't exist when widgets are initialized.)

"""
Besides differences in written language letters and words,
various languages use different marks as separators for decimals.

Also sometimes variations in the separators exist within the same country.

This module will focus mostly on the most prevalent cases.

An option to choose decimal separator mark could be created
but the selection should NOT be forced on the user
since they might be very inexperienced and not even know which is the correct mark.
"""


class LanguageNotImplemented(Exception):
    pass


SUPPORTED_LANGUAGES = {}


class Language(object):
    def __init__(self, name, name_native):
        self.name_native = name_native  # Language name spelled with characters of the language itself
        self.name = name
        SUPPORTED_LANGUAGES.update({self.name: self})


# In reality, separators differ for different english-speaking countries
# (e.g. eng_US, eng_ireland, eng_UK ..).
# Since this program is not expected to become very popular,
# the convention below should be ok.
# Alternatively, the user could be prompted to select his separator;
# the prompt should be in a very easy to understand form:
# e.g. "Three point one." Select the image that is accurate (used for separator blabla..)
english = Language(name='english', name_native='english')
greek = Language(name='greek',  name_native=u'ελληνικά')


class Message(object):
    DEFAULT_LANGUAGE = 'english'
    selected_language = DEFAULT_LANGUAGE

    def __init__(self, only_english=False, **kwargs):
        # Ensures required languages are implemented
        if only_english:
            if self.DEFAULT_LANGUAGE not in kwargs:
                raise LanguageNotImplemented(self.DEFAULT_LANGUAGE)
        langs_not_implemented = set(kwargs) - set(SUPPORTED_LANGUAGES)
        if langs_not_implemented:
            raise LanguageNotImplemented(langs_not_implemented)
        self.langs_msgs_dct = kwargs


PLAY = Message(
    english='Play',
    greek=u'Παιχνίδι',
)


ABOUT = Message(
    english='About',
    greek=u'Σχετικά',
)


HELP = Message(
    english='Help',
    greek=u'Βοήθεια',
)


REWARDS = Message(
    english='Rewards',
    greek=u'Βραβεία',
)


VERSION = Message(
    english='version',
    greek='έκδοση',
)


EASY = Message(
    english='easy',
    greek='εύκολα',
)


MEDIUM = Message(
    english='medium',
    greek='μέτρια',
)

HARD = Message(
    english='hard',
    greek='δύσκολα',
)

OPERATION_CATEGORIES = Message(
    english='Operation type',
    greek='Είδος πράξεων',
)

DIFFICULTY = Message(
    english='Difficulty',
    greek='Δυσκολία',
)

CLEAR = Message(
    english='Clear',
    greek='Σβήσιμο',
)

CHECK_ANSWER = Message(
    english='Check\nanswer',
    greek='Έλεγχος\nαπάντησης',
)

SEPARATOR_SYMBOL = Message(
    english='.',
    greek=',',
)


