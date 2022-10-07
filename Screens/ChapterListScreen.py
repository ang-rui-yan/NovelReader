from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import OneLineListItem

import os
import re
from ConfigurationReader import read_config

config = read_config('Data/config.txt')


class ChapterListScreen(Screen):
	def __init__(self, **kwargs):
		super(ChapterListScreen, self).__init__(**kwargs)
		pass
		
	def on_enter(self):
		numbers = re.compile(r'(\d+)')

		def numericalSort(value):
			parts = numbers.split(value)
			parts[1::2] = map(int, parts[1::2])
			return parts

		self.ids.md_list.clear_widgets()
		app = App.get_running_app()
		novel_title = app.reading_novel
		self.ids.lblNovelTitle.text = novel_title.replace("-"," ").title()
		
		chapters_location = '{0}/{1}/text/'.format(
			config['novels'],
			novel_title)
			
		novel_details_location = '{0}/{1}/details.txt'.format(
			config['novels'],
			novel_title)
		novel_details = read_config(novel_details_location)
			
		chapter_list = []

		 # Loop thru dir where novels are stored	
		for chapter in sorted(os.listdir(chapters_location), key=numericalSort):
			formatted_chapter_name = chapter.replace("_", " ").replace(".txt","")		
			
			if novel_details['last_read'] == chapter:
				print(chapter)
				print(novel_details['last_read'])
				item = OneLineListItem(
					text=formatted_chapter_name,
					theme_text_color='Custom',
					text_color=[1,1,1,1],
					bg_color=[.5,.5,.5,1])
			else:
				item = OneLineListItem(
					text=formatted_chapter_name)
			item.bind(on_release=self.go_reader)
			
			self.ids.md_list.add_widget(item)
			chapter_list.append(chapter)
			
		app.chapter_list = chapter_list
			
	def go_reader(self, instance):
		app = App.get_running_app()
		chapter_clicked = instance.text.replace(" ","_") + ".txt"
		
		app.current_chapter_index = app.chapter_list.index(chapter_clicked)
		
		self.manager.transition.direction = 'left'
		self.manager.current = 'reader'		