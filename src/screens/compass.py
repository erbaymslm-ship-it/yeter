"""
Compass Screen - Turkish TTS compass
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class CompassScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(Label(text='COMPASS (Turkish TTS)\n(Coming Soon)', 
                             size_hint_y=1))
