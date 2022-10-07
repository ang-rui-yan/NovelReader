import requests
import re
import os
from bs4 import BeautifulSoup
from plyer import tts

from ConfigurationReader import read_config, read_line_data
from SpeechConverter import convert_all_to_audio, convert_to_audio
from NovelManager import has_downloaded_text, has_novel_downloaded

config = read_config("Data/config.txt")
novels = read_line_data("Data/novels.txt")

def get_chapters_url(novel):
	print("Retrieving chapter list")
	latest_chapter = get_latest_chapter_number(novel)
	
	max_pages = (int(700) // 50)
	
	chapter_dict = []
	
	for page_no in range(1, max_pages+1):
		url = config['chapterList'].format(novel,page_no)
		print(url)
		
		page = requests.get(url)		
		
		soup = BeautifulSoup(page.content, 'html.parser')
		list_chapters = soup.findAll("ul", {"class":"list-chapter"})
		
		for ul in list_chapters:
			anchors = ul.select("li > a")
			for anchor in anchors:
				link = anchor['href']
				chapter_title = anchor['title']
				chapter_dict.append(
					{
						"title":chapter_title,
						"link":link[1:]
					})
				
	return chapter_dict
	
def get_content(page):
	soup = BeautifulSoup(page.content, 'html.parser')
	container = soup.find(id="chapter-content")
			
	return get_content_based_on_type(container)

def get_content_based_on_type(container):
	final_content = ""
	next_container = container.find_next_sibling("div")
	content = next_container.select("p")
	
	if not content:
		content = container.select("p")
	
	for paragraph in content:
		final_content += paragraph.text		
		final_content += "\n\n"
	
	return final_content
			

def get_latest_chapter_number(novel):
	url = config['overview'].format(novel)
	page = requests.get(url)
	
	if page.status_code == 404:
		return
	else:
		soup = BeautifulSoup(page.content, 'html.parser')
		chapter_list = soup.find("ul", {"class":"l-chapters"})
		latest_chapter = chapter_list.find("li").find(
			"span",
			{"class":"chapter-text"}).text
	
		latest_no = re.findall('\d+', latest_chapter)
		print("Latest chapter is",latest_no)
		return latest_no[0]

def save_novel_image(novel):
	if not has_novel_downloaded(novel):
		url = config['overview'].format(novel)
		page = requests.get(url)
		
		if page.status_code == 404:
			return
		else:
			soup = BeautifulSoup(page.content, 'html.parser')
			div_image = soup.find('div', 
				{"class":"book"})
			image = div_image.select('img')[0]
			image_url = '{0}/{1}'.format(
				config['website'],
				image['src'])
			print(image_url)
			response = requests.get(image_url)			
			save_to = '{0}/{1}/image.png'.format(
				config['novels'],
				novel)
			file = open(save_to, "wb")
			file.write(response.content)
			file.close()

def save_as_file(novel, chapter, content):
	formatted_novel = str(novel).replace(" ", "_")
	formatted_chapter = str(chapter).replace(" ", "_")
	novels_location = config['novels'] 
	
	location = '{0}/{1}/text/{2}.txt'.format(
		novels_location,
		formatted_novel,
		formatted_chapter)
	
	os.makedirs(os.path.dirname(location), exist_ok=True)
	
	text_file = open(location, "w")
	text_file.write(content)
	text_file.close()
	
	print(formatted_chapter, "has been saved")

def retrieve_novels():
	for novel in novels:
		print("Beginning to download",novel)
		save_novel_image(novel)
		chapter_list = get_chapters_url(novel)
		for chapter in chapter_list:
			if not has_downloaded_text(novel, chapter['title']):
				url = '{0}/{1}'.format(
					config['website'],
					chapter['link'])
				page = requests.get(url)
				print(url)
				
				if page.status_code == 404:
					print("Error")
					pass
				else:
					content = get_content(page)
					save_as_file(novel, chapter['title'], content)
			else:
				print(chapter['title'], "exists")
