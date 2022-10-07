from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar

#from Screens.MenuScreen import MenuScreen
from Screens.NovelDirectoryScreen import NovelDirectoryScreen
from Screens.NovelReaderScreen import NovelReaderScreen
from Screens.AudioPlayerScreen import AudioPlayerScreen
from Screens.ChapterListScreen import ChapterListScreen

# Changes the screen to display below the toolbar
class DisplayScreenManager(ScreenManager):
	def __init__(self, **kwargs):
		super(DisplayScreenManager, self).__init__(**kwargs)
		
		self.add_widget(NovelDirectoryScreen(name='directory'))
		self.add_widget(ChapterListScreen(name='chapters'))
		self.add_widget(NovelReaderScreen(name='reader'))
		self.add_widget(AudioPlayerScreen(name='audio'))
		self.current = "directory"
		
		Window.bind(on_keyboard=self.on_key)
	
	def on_key(self, window, key, *args):
		if key == 27:  # the esc key
			if self.current_screen.name == "directory":
				return False
			elif self.current_screen.name == "chapters":
				self.current = "directory"
				self.transition.direction = "right"
				return True  # do not exit the app
			elif self.current_screen.name == "audio":
				self.current = "reader"
				self.transition.direction = "right"
			else:
				self.current = "chapters"
				self.transition.direction = "right"
				return True  # do not exit the app

# Provides consistent toolbar
class MainScreen(Screen):
	def __init__(self, **kwargs):
		super(MainScreen, self).__init__(**kwargs)
		
		layout = MDBoxLayout()
		layout.orientation = 'vertical'
		toolbar = MDTopAppBar()
		toolbar.id = 'toolbar'
		toolbar.title = "Wuxia Reader"
		
		layout.add_widget(toolbar)
		layout.add_widget(DisplayScreenManager())
		
		self.add_widget(layout)

# Set up all screens regardless
class WindowManager(ScreenManager):
	def __init__(self, **kwargs):
		super(WindowManager, self).__init__(**kwargs)
		Window.bind(on_keyboard=self.on_key)
	
	def on_key(self, window, key, *args):
		if key == 27:  # the esc key
			if self.current_screen.name == "":
				return False
			else:
				self.current = 'main'
				self.transition.direction = "right"
				return True  # do not exit the app


class NovelApp(MDApp):
	def build(self):
		screen = Builder.load_file("Screens/main.kv")
		return screen

if __name__ == '__main__':
	NovelApp().run()