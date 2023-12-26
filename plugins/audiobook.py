import os
import re

from mutagen.mp4 import MP4
from preferences import logging


logger = logging.setup()

# Remove undesired term from title
def remove_unabridged(title):
	tag_title = title.replace("(Unabridged)", "").strip()
	return tag_title

# Remove illegal system characters from title
def remove_illegal_chars(tag_title):
	clean_title = re.sub(r'[<>:"/\\|?*]', '_', tag_title)
	return clean_title

# Organise m4b files into dir structure: ...target/Author/Audiobookname.m4b
def process(file_path, book_path):
	file = os.path.basename(file_path)

	try:
		audio = MP4(file_path)
		author = audio.get('\xa9ART', ["Unknown Author"])[0]
		title = audio.get('\xa9nam', file)[0]

		tag_title = remove_unabridged(title)
		clean_title = remove_illegal_chars(tag_title)

		audio['\xa9alb'] = tag_title # album tag
		audio['\xa9nam'] = tag_title # title tag
		audio.save()

	except:
		logger.error("Not a .mp4 file. Please check this is a real!")

	author_folder = os.path.join(book_path, author)
	if not os.path.exists(author_folder):
		os.makedirs(author_folder)

	return os.path.join(author_folder, f"{clean_title}.m4b")


if __name__ == '__main__':
    print("Please run 'butler.py'")