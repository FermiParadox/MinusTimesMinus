"""Used for citing all third party images.

An image could have several derivatives.
In that case all its derivatives have the same citation.
"""
ACCEPTABLE_LICENSES = {'cc0', 'public domain', 'cc by'}

IMAGES_CITED = set()    # File names
FIRST_IMAGE_TO_CITATION_MAP = {}


class ImageCitation(object):
    """
    Used for citing each individual work.
    Citation includes all related data along with extra requirements by the copyright owner.

    NOTE: Assumes the returned text will be displayed with markup enabled.
    """

    def __init__(self,
                 work_name,
                 creation_date,
                 licence,
                 adaptation,
                 file_names,
                 creator_name=None, creator_pseudonym=None,
                 url='',
                 extra_text='',
                 ignore=False):
        """
        Takes all needed data for the citation.
        Creator can be identified by either name or pseudonym.

        In case of a pseudonym, pseudonym related origin should be present.

        WARNING: In case of multiple files, start with original file
            since only the first image is displayed.

        :param work_name: (str)
        :param creator_name: (str)
        :param creator_pseudonym: (str) Pseudonym with pseudonym origin, e.g. "TallPony (wikipedia user)"
        :param creation_date: (str) Work creation date. e.g. 10-May-2015 (avoid displaying month as a number)
        :param url: (str)
        :param licence: (str) "cc0", "public domain" etc
        :param adaptation: (bool) Adapted (modified) or original work (refers to first file in file_names)
        :param file_names: (list) Names of all image files derived from the work.
        :param extra_text: (str) Extra text required by the copyright owner.
        :param ignore: (bool) Used if citation has been created but image is not included.
            Useful in case a previously discarded image is used again, in order to avoid creating 
            its citation all over again.
        """
        if not (creator_name or creator_pseudonym):
            raise ValueError('At least one of `creator_name` and `creator_pseudonym` should be provided.')
        if creator_name and creator_pseudonym:
            raise ValueError('Only one of `creator_name` and `creator_pseudonym` should be provided.')
        if licence not in ACCEPTABLE_LICENSES:
            raise ValueError('Licence not acceptable')

        self.file_names = file_names
        self.adaptation = adaptation
        self.licence = licence
        self.url = url
        self.creation_date = creation_date
        self.creator_name = creator_name
        self.creator_pseudonym = creator_pseudonym
        self._creator = creator_name or creator_pseudonym
        self.work_name = work_name
        self.extra_text = extra_text

        if not ignore:
            IMAGES_CITED.update(file_names)
            FIRST_IMAGE_TO_CITATION_MAP.update({file_names[0]: self})

    def full_text(self):
        """
        Final citation text.

        NOTE: Assumes markup is done by "[b]", "[size=8]", etc.
        """
        final_text = ("[b]{work_name}[/b] image by {creator} ({creation_date}). "
                      "\n[size=10]{url}[/size]").format(work_name=self.work_name,
                                                        creator=self._creator,
                                                        creation_date=self.creation_date,
                                                        url=self.url)

        if self.adaptation:
            final_text = 'My adaptation of ' + final_text

        if self.extra_text:
            final_text += '\n' + self.extra_text

        return '[size=12]{}[/size]'.format(final_text)


# (To be used for copy-pasting when creating new ImageCitation
# in order to avoid accidentally forgetting to change an arg value.)
"""
 = ImageCitation(
    work_name=,
    creation_date=,
    licence=,
    adaptation=,
    file_names=,
    creator_name=,
    creator_pseudonym=,
    url=,
    extra_text=)
"""

GOLD_ZEUS_COIN = ImageCitation(
    work_name='Zeus with a laurel crown, gold stater from Lampsacus',
    creation_date='2010',
    licence='public domain',
    adaptation=True,
    file_names=['gold_coin_zeus_small.png'],
    creator_name=None,
    creator_pseudonym='Jastrow (wikipedia user)',
    url='commons.wikimedia.org/wiki/File:Stater_Zeus_Lampsacus_CdM.jpg',
    extra_text='')

TICK_YES = ImageCitation(
    work_name='check',
    creation_date='Oct 18, 2013',
    licence='public domain',
    adaptation=False,
    file_names=['tick_yes.png', 'tick_no.png'],
    creator_name=None,
    creator_pseudonym='OpenClipart-Vectors (pixabay user)',
    url='https://pixabay.com/en/check-correct-green-mark-tick-157822/',
    extra_text='')

GOLD_LAUREL = ImageCitation(
    work_name='Golden laurel wreath',
    creation_date='April 2007',
    licence='public domain',
    adaptation=False,
    file_names=['gold_laurel_small.jpg', ],
    creator_name=None,
    creator_pseudonym='Andreas Praefcke (wikipedia user)',
    url='https://commons.wikimedia.org/wiki/File:Lorbeerkranz_Zypern_rem.jpg',
    extra_text='Golden laurel wreath, probably from Cyprus, 4th/3rd century BC; Reiss-Engelhorn-Museen, Mannheim, Germany')

SILVER_COIN = ImageCitation(
    work_name='Silver Tetradrachm of Athens 454-415 BC',
    creation_date='23 November 2010',
    licence='cc0',
    adaptation=False,
    file_names=['athena_coin.png', 'athena_coin_small.png'],
    creator_name=None,
    creator_pseudonym='yuichi (wikipedia user)',
    url='https://commons.wikimedia.org/wiki/File:Athens_owl_coin.jpg',
    extra_text='')


NAVAGIO = ImageCitation(
    work_name='zakhyntos shipwreck',
    creation_date='Sept. 11, 2011',
    licence='public domain',
    adaptation=True,
    file_names=['navagio_adapt.png'],
    creator_name=None,
    creator_pseudonym='ytora (pixabay user)',
    url='https://pixabay.com/en/zakhyntos-zakintosz-shipwreck-1432220/',
    extra_text
    ='')

if __name__ == '__main__':
    print()
    print(GOLD_ZEUS_COIN.full_text())
