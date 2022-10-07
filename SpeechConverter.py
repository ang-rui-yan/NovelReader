from gtts import gTTS
import os

from ConfigurationReader import read_config
from NovelManager import has_downloaded_audio
		
def convert_all_to_audio(novel):
	config = read_config("Data/config.txt")
	chapters = '{0}/{1}/text/'.format(
		config['novels'],
		novel)
	
	print(novel, ": Saving audio book")	
	for chapter in os.listdir(chapters):
		if not has_downloaded_audio(novel, chapter):
			read_from = '{0}/{1}/text/{2}'.format(
				config['novels'],
				novel,
				chapter)
				
			write_to = '{0}/{1}/speech/{2}.mp3'.format(
				config['novels'],
				novel,
				chapter.replace(".txt",""))
			
			file = open(read_from, "r").read().replace("\n", " ")
			speech = gTTS(
				text = str(file), 
				lang = 'en', 
				slow = False,
				tld = 'com')
			
			os.makedirs(os.path.dirname(write_to), exist_ok=True)
			speech.save(write_to)
			
			print(chapter, "downloaded")
		else:
			print(chapter.replace(".txt",".mp3"), "exists")
			
def convert_to_audio(novel, chapter_title):
	config = read_config("Data/config.txt")
	chapter = '{0}/{1}/text/{2}'.format(
		config['novels'],
		novel,
		chapter_title)
	if not has_downloaded_audio(novel, chapter_title):
		write_to = '{0}/{1}/speech/{2}.mp3'.format(
			config['novels'],
			novel,
			chapter_title.replace(".txt",""))
		file = open(chapter, "r").read().replace("\n", " ")
		speech = gTTS(
			text = str(file), 
			lang = 'en', 
			slow = False,
			tld = 'com')
			
		os.makedirs(os.path.dirname(write_to), exist_ok=True)
		speech.save(write_to)
			
		print(chapter_title, "downloaded")
	else:
		print(chapter_title.replace(".txt",".mp3"), "exists")