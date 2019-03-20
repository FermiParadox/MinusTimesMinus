import os
import citations

INCLUDED_IMAGES = set(os.listdir('third_parties_images'))
CITED_IMAGES = citations.IMAGES_CITED
FILES_NOT_CITED = INCLUDED_IMAGES - CITED_IMAGES
if INCLUDED_IMAGES - CITED_IMAGES:
    raise NotImplementedError('Following image files were not cited: {}'.format(FILES_NOT_CITED))

REDUNDANT_CITATIONS = CITED_IMAGES - INCLUDED_IMAGES
if REDUNDANT_CITATIONS:
    print('Found citations without their corresponding image: {}'.format(REDUNDANT_CITATIONS))