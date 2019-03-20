import main


_MIT_LICENCE = """Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""

_PROJECT_LICENCE_FIRST_LINE = "Copyright (c) 2016 Fermi Paradox (http://stackoverflow.com/users/4230591/fermi-paradox?tab=profile)"
_KIVY_LICENCE_FIRST_LINE = "Copyright (c) 2010-2016 Kivy Team and other contributors"

PROJECT_LICENCE = '{}\n\n{}'.format(_PROJECT_LICENCE_FIRST_LINE, _MIT_LICENCE)

KIVY_LICENCE = '{}\n\n{}'.format(_KIVY_LICENCE_FIRST_LINE, _MIT_LICENCE)

DISCLAIMER = '''\n\n\n[b]Disclaimer[/b]\n
The rewards exist only for cosmetic purposes, and have no real currency value.\n\n'''

ABOUT_TEXT = '[b]{} licence[/b]\n\n'.format(main.APP_NAME)
ABOUT_TEXT += '[size=12]{}[/size]\n\n\n'.format(PROJECT_LICENCE)
ABOUT_TEXT += '[b]Kivy licence[/b]\n\n'
ABOUT_TEXT += '[size=12]{}[/size]'.format(KIVY_LICENCE)
ABOUT_TEXT += DISCLAIMER

