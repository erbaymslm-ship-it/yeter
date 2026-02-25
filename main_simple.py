"""
ELIXIR TECHNOLOGY
Yerüstü Tarama Uygulaması - v1.0
Kivy 2.3.0 + KivyMD 1.2.0
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

# Pencere ayarları
Window.size = (1000, 700)
Window.title = "ELIXIR TECHNOLOGY - Yerüstü Tarama Sistemi"

# Renkler
class Colors:
    bg = get_color_from_hex("#050505")
    neon_blue = get_color_from_hex("#00F2FF")
    neon_red = get_color_from_hex("#FF0033")
    neon_green = get_color_from_hex("#00FF88")
    text_dim = get_color_from_hex("#4A8FA8")
    white = get_color_from_hex("#FFFFFF")

Window.clearcolor = Colors.bg


class ElixirApp(App):
    """Ana uygulama sınıfı"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "ELIXIR TECHNOLOGY"
        self.current_screen = "menu"
    
    def build(self):
        """Uygulamayı oluştur"""
        self.main_box = BoxLayout(orientation='vertical')
        self.screens = {}
        
        # İlk ekranı göster
        self.show_menu()
        
        return self.main_box
    
    def show_menu(self):
        """Ana menüyü göster"""
        self.main_box.clear_widgets()
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Başlık
        header = BoxLayout(orientation='vertical', size_hint_y=0.25, spacing=5)
        header.add_widget(Label(
            text='[⚡] ELIXIR TECHNOLOGY [⚡]',
            font_size='24sp',
            bold=True,
            color=Colors.neon_blue
        ))
        header.add_widget(Label(
            text='YERÜSTÜ TARAMA SİSTEMİ v1.0',
            font_size='14sp',
            color=Colors.text_dim
        ))
        header.add_widget(Label(
            text='━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━',
            font_size='12sp',
            color=Colors.neon_blue
        ))
        layout.add_widget(header)
        
        # Menü butonları
        buttons_layout = GridLayout(cols=2, spacing=12, size_hint_y=0.60)
        
        buttons = [
            ('📡\nYER ALTI\nGÖRÜNTÜLEME', 'scan', Colors.neon_blue),
            ('🎯\nPOINTER\nMOD', 'pointer', Colors.neon_green),
            ('🧭\nPUSSULA\nTTS', 'compass', Colors.neon_blue),
            ('⚙️\nAYARLAR', 'settings', Colors.neon_red),
        ]
        
        for text, screen_name, color in buttons:
            btn = Button(
                text=text,
                font_size='13sp',
                background_color=(0, 0, 0, 0)
            )
            btn.bind(on_press=lambda x, s=screen_name: self.show_screen(s))
            btn.color = color
            buttons_layout.add_widget(btn)
        
        layout.add_widget(buttons_layout)
        
        # Footer
        footer = BoxLayout(orientation='vertical', size_hint_y=0.15, spacing=3)
        footer.add_widget(Label(
            text='━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━',
            font_size='12sp',
            color=Colors.neon_blue
        ))
        footer.add_widget(Label(
            text='ELIXIR TECHNOLOGY © 2025 | Cyberpunk Scanner',
            font_size='11sp',
            color=Colors.text_dim
        ))
        layout.add_widget(footer)
        
        self.main_box.add_widget(layout)
    
    def show_screen(self, screen_name):
        """Ekranı değiştir"""
        self.main_box.clear_widgets()
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Başlık
        screen_titles = {
            'scan': ('🌍 YER ALTI GÖRÜNTÜLEME', 'Underground Scanning Mode', Colors.neon_blue),
            'pointer': ('📡 POINTER MOD', 'Bluetooth HC-05 Real-Time', Colors.neon_green),
            'compass': ('🧭 PUSULA', 'Turkish TTS Navigation', Colors.neon_blue),
            'settings': ('⚙️ AYARLAR', 'Application Settings', Colors.neon_red),
        }
        
        if screen_name in screen_titles:
            title, subtitle, color = screen_titles[screen_name]
            
            header = BoxLayout(orientation='vertical', size_hint_y=0.20, spacing=5)
            header.add_widget(Label(
                text=title,
                font_size='22sp',
                bold=True,
                color=color
            ))
            header.add_widget(Label(
                text=f'[ {subtitle} ]',
                font_size='12sp',
                color=Colors.text_dim
            ))
            layout.add_widget(header)
        
        # İçerik alanı (şimdilik placeholder)
        content = BoxLayout(orientation='vertical', size_hint_y=0.60, spacing=10)
        content.add_widget(Label(
            text='MODÜL GELİŞTİRİLİYOR...\n\n[Coming Soon]',
            font_size='16sp',
            color=Colors.text_dim
        ))
        layout.add_widget(content)
        
        # Geri butonu
        back_btn = Button(
            text='◀ MENÜYE DÖN',
            font_size='13sp',
            size_hint_y=0.15,
            background_color=(0, 0, 0, 0),
            color=Colors.neon_red
        )
        back_btn.bind(on_press=lambda x: self.show_menu())
        layout.add_widget(back_btn)
        
        self.main_box.add_widget(layout)


if __name__ == '__main__':
    app = ElixirApp()
    app.run()
