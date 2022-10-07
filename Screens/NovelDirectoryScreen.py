from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import OneLineAvatarListItem, ImageLeftWidget

import os
from ConfigurationReader import read_config


config = read_config('Data/config.txt')


class NovelDirectoryScreen(Screen):
	def __init__(self, **kwargs):
		super(NovelDirectoryScreen, self).__init__(**kwargs)
		pass
		
	def on_enter(self):
		self.ids.md_list.clear_widgets()
		 # Loop thru dir where novels are stored	
		for novel in os.listdir(config['novels']):
			
			image_source = '{0}/{1}/image.png'.format(
				config['novels'],
				novel)
			image = ImageLeftWidget(
				source=image_source)
				
			formatted_novel_name = novel.replace("-"," ").title()
			item = OneLineAvatarListItem(
				text=formatted_novel_name)
			item.bind(on_release=self.go_chapter_list)
			item.add_widget(image)
			
			self.ids.md_list.add_widget(item)
			
	def go_chapter_list(self, instance):
		app = App.get_running_app()
		novel_clicked = instance.text.lower().replace(" ","-")
		app.reading_novel = novel_clicked
		
		self.manager.transition.direction = 'left'
		self.manager.current = 'chapters'			