"""
Pointer Screen - Bluetooth HC-05 real-time data
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class PointerScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(Label(text='POINTER MODE\n(Bluetooth HC-05)\n(Coming Soon)', 
                             size_hint_y=1))
