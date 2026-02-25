"""
Scan Screen - Underground visualization with heat map
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class ScanScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(Label(text='UNDERGROUND SCAN\n(Coming Soon)', 
                             size_hint_y=1))
