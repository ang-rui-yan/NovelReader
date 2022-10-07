from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivymd.uix.button import MDIconButton


from ConfigurationReader import read_config, update_config

config = read_config('Data/config.txt')

class NovelReaderScreen(Screen):
	def __init__(self, **kwargs):
		super(NovelReaderScreen, self).__init__(**kwargs)
		self.visible = True
		pass
		
	def on_enter(self):
		self.ids.scrlv.scroll_y = 1	
		
		app = App.get_running_app()
		self.chapter = app.chapter_list[app.current_chapter_index]
		
		self.novel = app.reading_novel
		self.ids.lblChapterTitle.text = self.chapter.replace("_"," ").replace(".txt","")
			
		chapter_location = '{0}/{1}/text/{2}'.format(
			config['novels'],
			self.novel,
			self.chapter)
		
		file = open(chapter_location, 'r', encoding="utf8")
		lines = file.read()
		self.ids.disp_text.text = lines
		
		self.update_last_read()
		
	def go_previous(self, *args):
		app = App.get_running_app()
		
		self.chapter = app.chapter_list[app.current_chapter_index - 1]
		app.current_chapter_index = app.current_chapter_index - 1
		
		chapter_location = '{0}/{1}/text/{2}'.format(
			config['novels'],
			self.novel,
			self.chapter)
		
		file = open(chapter_location, 'r', encoding="utf8")
		lines = file.read()
		
		self.ids.lblChapterTitle.text = self.chapter.replace("_"," ").replace(".txt","")
		self.ids.disp_text.text = lines
		self.ids.scrlv.scroll_y = 1
	
	def go_next(self, *args):
		app = App.get_running_app()
		
		self.chapter = app.chapter_list[app.current_chapter_index + 1]
		app.current_chapter_index = app.current_chapter_index + 1
		
		chapter_location = '{0}/{1}/text/{2}'.format(
			config['novels'],
			self.novel,
			self.chapter)
		
		file = open(chapter_location, 'r', encoding="utf8")
		lines = file.read()
		
		self.ids.lblChapterTitle.text = self.chapter.replace("_"," ").replace(".txt","")
		self.ids.disp_text.text = lines
		self.ids.scrlv.scroll_y = 1
		
	def set_sidebar_visibility(self):
		if self.visible:
			self.ids.controlsLayout.size_hint_y = None
			self.ids.controlsLayout.height = "0dp"
			for child in self.ids.controlsLayout.children:
					child.theme_text_color = "Custom"
					child.text_color = [0,0,0,0]
					
			self.ids.lblChapterTitle.size_hint_y = None
			self.ids.lblChapterTitle.height = "0dp"
		else:
			self.ids.lblChapterTitle.size_hint_y = .08
			self.ids.controlsLayout.size_hint_y =.08
			for child in self.ids.controlsLayout.children:
					child.theme_text_color = "Custom"
					child.text_color = [0,0,0,1]
		self.visible = not self.visible
		
	def go_audio_player(self):
		self.manager.transition.direction = 'left'
		self.manager.current = 'audio'
		
	def update_last_read(self):
		novel_details_location = '{0}/{1}/details.txt'.format(
			config['novels'],
			self.novel)
			
		novel_details = read_config(novel_details_location)
		novel_details['last_read'] = self.chapter
		
		update_config(novel_details_location, novel_details)