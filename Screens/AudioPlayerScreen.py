from kivy.app import App
from kivy.uix.screenmanager import Screen
import pygame.mixer

from ConfigurationReader import read_config

config = read_config('Data/config.txt')

class AudioPlayerScreen(Screen):
	def __init__(self, **kwargs):
		super(AudioPlayerScreen, self).__init__(**kwargs)
		
	def on_enter(self):
		app = App.get_running_app()
		self.novel = app.reading_novel
		self.chapter_list = app.chapter_list
		self.current_index = app.current_chapter_index
		
		location = '{0}/{1}/speech/{2}'.format(
			config['novels'],
			self.novel,
			self.chapter_list[self.current_index].replace(".txt",".mp3"))
		
		self.ids.lblChapterTitle.text = self.chapter_list[self.current_index]\
			.replace(".txt",".mp3")+ " is now playing."
		
		self.isPlaying = True
		try:
			pygame.mixer.init()
			pygame.mixer.music.load(location)
			#self.length = pygame.mixer.music.get_length()
	#		self.ids.audio_seeker.max = self.length
			pygame.mixer.music.play(0)
		except pygame.error:
			self.ids.lblChapterTitle.text = "No such file found"
		
	def play_pause(self):
		if self.isPlaying:
			self.ids.btnPlayPause.icon = 'play'
			self.paused_at = pygame.mixer.music.get_pos()
			pygame.mixer.music.pause()
		else:
			self.ids.btnPlayPause.icon = 'pause'
			pygame.mixer.music.unpause()
		self.isPlaying = not self.isPlaying