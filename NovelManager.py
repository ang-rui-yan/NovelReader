from ConfigurationReader import read_config
import os

config = read_config('Data/config.txt')

# Verify if novel has been downloaded before
def has_novel_downloaded(novel):
	formatted_novel = novel.replace(" ", "_")
	novels_location = config['novels'] 
	
	location = '{0}/{1}/image.png'.format(
		novels_location,
		formatted_novel)
	
	return os.path.exists(location) and \
		os.path.getsize(location) > 0	

def has_downloaded_text(novel, chapter):
	formatted_novel = novel.replace(" ", "_")
	formatted_chapter = chapter.replace(" ", "_")
	novels_location = config['novels'] 
	
	location = '{0}/{1}/text/{2}.txt'.format(
		novels_location,
		formatted_novel,
		formatted_chapter)
		
	return os.path.exists(location) and \
		os.path.getsize(location) > 0
		
def has_downloaded_audio(novel, chapter):
	location = '{0}/{1}/speech/{2}.mp3'.format(
			config['novels'],
			novel,
			chapter.replace(".txt",""))
		
	return os.path.exists(location) and \
		os.path.getsize(location) > 0