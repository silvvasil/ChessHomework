"""
Made by Silvestrov Vasilii
import datetime
"""

import argparse
import sys
from PIL import Image
from pathlib import Path
from os import walk, listdir
from os.path import isfile, join


A4_SIZE = (2480, 3508)
TOP = 120
BOTTOM = 120
WHITE = (255, 255, 255)
PICTURE_SIZE = 960
EMPTY_HEIGHT = (A4_SIZE[1] - 3 * PICTURE_SIZE - TOP - BOTTOM) // 3
LEFT = RIGHT = EMPTY_WIDTH = (A4_SIZE[0] - 2 * PICTURE_SIZE) // 3
CORNERS = [
    (LEFT, TOP),
    (LEFT + PICTURE_SIZE + EMPTY_WIDTH, TOP),
    (LEFT, TOP + PICTURE_SIZE + EMPTY_HEIGHT),
    (LEFT + PICTURE_SIZE + EMPTY_WIDTH, TOP + PICTURE_SIZE + EMPTY_HEIGHT),
    (LEFT, TOP + 2 * (PICTURE_SIZE + EMPTY_HEIGHT)),
    (LEFT + PICTURE_SIZE + EMPTY_WIDTH, TOP + 2 * (PICTURE_SIZE + EMPTY_HEIGHT)),
]
BLOCK_SIZE = 6
BASE_DIR = 'chess.pdf'


def concat(images: list[Image]) -> Image:
    """

    Concatinate up to 6 images into A4 page

    A4 paper is 2480 x 3508 pixels

    Paddings are:
        top     ---  20 mm 
        bottom  ---  20 mm
        left    ---  30 mm
        right   ---  10 mm
    
    """

    assert len(images) <= 6

    resized_images = [image.resize((PICTURE_SIZE, PICTURE_SIZE)) for image in images]


    img = Image.new('RGB', A4_SIZE, WHITE)


    for index, image in enumerate(resized_images):
        img.paste(image, CORNERS[index])

    return img



def generate_pages(images : list[Image]) -> list[Image]:
    """
    Split images into pages of 6 images.
    """
    pages = []
    size = len(images)
    for i in range(0, size, BLOCK_SIZE):
        pages.append(concat(images[i:min(size, i + BLOCK_SIZE)]))
    return pages


def save_pdf(pages: list[Image], pdf_path: str) -> None:
    """
    Concatinate pages to pdf and save it to pdf_path
    """
    pages[0].save(
        pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=pages[1:]
    )



def main():
    """
    Parse command and concatinate images to pdf
    """

    parser = argparse.ArgumentParser(description='Process some filenames.')
    parser.add_argument('-f', dest='files', action='append', nargs='+',
                        help='filenames of images to concatinate to pdf')
    parser.add_argument('--save_to', dest='pdf_path', action='store', default=BASE_DIR,
                        help='path to save the result pdf')
    parser.add_argument('--no-files', dest='no_files', action='store_true')
    parser.set_defaults(no_files=False) 
    args = parser.parse_args(sys.argv[1:])
    
    images = []
    filenames = []
    if args.no_files:
        easy = ["easy/" + i for i in [f for f in listdir("easy/") if isfile(join("easy", f))]][1:]
        hard = ["hard/" + i for i in [f for f in listdir("hard/") if isfile(join("hard", f))]][1:]
        filenames = easy[:4] + hard[:2]     
    else:
        filenames = args.files[0]
    for f in filenames:
        images.append(Image.open(f))
        Path(f).rename('/'.join(f.split('/')[:-1]) + '/used/' + f.split('/')[-1]) 
    save_pdf(generate_pages(images), args.pdf_path)


if __name__ == '__main__':
    main()
