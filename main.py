"""
ELIXIR TECHNOLOGY - Tam Özellikli Yerüstü Tarama Sistemi
v1.0 - TÜM MODÜLER AKTİF + GELIŞMIŞ UI
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.graphics import Color, Rectangle, Line, Ellipse, RoundedRectangle
from kivy.uix.widget import Widget

import numpy as np
from datetime import datetime

# ═════════════════════════════════════════════════════════════════════════════
# 🎨 TEMA - CYBERPUNK WIREFRAME + ELIT TASARIM
# ═════════════════════════════════════════════════════════════════════════════

class Theme:
    """Cyberpunk tema renkleri"""
    bg = get_color_from_hex("#0a0e27")          # Koyu mavi-siyah
    bg_secondary = get_color_from_hex("#050505")
    neon_blue = get_color_from_hex("#00F2FF")
    neon_cyan = get_color_from_hex("#00FFCC")
    neon_red = get_color_from_hex("#FF0043")
    neon_green = get_color_from_hex("#00FF88")
    neon_yellow = get_color_from_hex("#FFFF00")
    neon_purple = get_color_from_hex("#B800FF")
    text_bright = get_color_from_hex("#FFFFFF")
    text_dim = get_color_from_hex("#5A8FA8")
    accent = get_color_from_hex("#00F2FF")

Window.clearcolor = Theme.bg
Window.size = (1280, 800)
Window.title = "⚡ ELIXIR TECHNOLOGY - Yerüstü Tarama Sistemi"


# ═════════════════════════════════════════════════════════════════════════════
# 🎨 CUSTOM WIDGETS
# ═════════════════════════════════════════════════════════════════════════════

class GlowingButton(Button):
    """Parlayan neon buton"""
    
    def __init__(self, glow_color=Theme.neon_blue, **kwargs):
        super().__init__(**kwargs)
        self.glow_color = glow_color
        self.background_normal = ""
        self.background_color = (0, 0, 0, 0)
        self.color = glow_color
        self.bold = True
        self.font_size = "16sp"
        
        self.bind(size=self._draw_background, pos=self._draw_background)
        self._draw_background()
    
    def _draw_background(self, *args):
        """Neon çerçeve ile buton çiz"""
        self.canvas.before.clear()
        with self.canvas.before:
            # Arka plan (yarı-şeffaf koyu)
            Color(self.glow_color[0] * 0.1, self.glow_color[1] * 0.1, 
                  self.glow_color[2] * 0.2, 0.3)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[15])
            
            # Neon çerçeve
            Color(*self.glow_color[:3], 0.8)
            Line(rounded_rectangle=(self.x, self.y, self.width, self.height, 15),
                 width=2)
            
            # Üst parlama çizgisi
            Color(*self.glow_color[:3], 0.4)
            Line(points=[self.x + 10, self.y + self.height - 2,
                        self.x + self.width - 10, self.y + self.height - 2],
                width=1.5)
    
    def on_press(self):
        """Basılınca hızlı pulse"""
        anim = Animation(opacity=0.5, duration=0.05) + Animation(opacity=1.0, duration=0.1)
        anim.start(self)


class WireframeWidget(Widget):
    """Hareketli wireframe grid arka planı"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.offset = 0.0
        self.bind(pos=self._redraw, size=self._redraw)
        Clock.schedule_interval(self._animate, 1/30)
    
    def _animate(self, dt):
        self.offset = (self.offset + 0.5) % 100
        self._redraw()
    
    def _redraw(self, *args):
        self.canvas.before.clear()
        if self.width == 0 or self.height == 0:
            return
        
        with self.canvas.before:
            # Arka plan gradient
            Color(0.04, 0.05, 0.15, 1)
            Rectangle(pos=self.pos, size=self.size)
            
            # Yatay çizgiler
            Color(0.0, 0.3, 0.5, 0.12)
            step = 50
            y = self.y - step + (self.offset % step)
            while y < self.y + self.height + step:
                Line(points=[self.x, y, self.x + self.width, y], width=0.8)
                y += step
            
            # Dikey çizgiler
            x = self.x - step + (self.offset % step)
            while x < self.x + self.width + step:
                Line(points=[x, self.y, x, self.y + self.height], width=0.8)
                x += step
            
            # Köşe dekoratif çizgileri
            Color(0.0, 0.95, 1.0, 0.4)
            margin = 15
            corner = 35
            
            # Sol alt
            Line(points=[self.x + margin, self.y + margin + corner,
                        self.x + margin, self.y + margin,
                        self.x + margin + corner, self.y + margin], width=2)
            # Sağ alt
            Line(points=[self.x + self.width - margin - corner, self.y + margin,
                        self.x + self.width - margin, self.y + margin,
                        self.x + self.width - margin, self.y + margin + corner], width=2)
            # Sol üst
            Line(points=[self.x + margin, self.y + self.height - margin - corner,
                        self.x + margin, self.y + self.height - margin,
                        self.x + margin + corner, self.y + self.height - margin], width=2)
            # Sağ üst
            Line(points=[self.x + self.width - margin - corner, self.y + self.height - margin,
                        self.x + self.width - margin, self.y + self.height - margin,
                        self.x + self.width - margin, self.y + self.height - margin - corner], width=2)


# ═════════════════════════════════════════════════════════════════════════════
# 📡 BLUETOOTH BAĞLANTISI (Mock)
# ═════════════════════════════════════════════════════════════════════════════

class BluetoothManager:
    """Bluetooth HC-05 yönetimi"""
    
    def __init__(self):
        self.connected = False
        self.device_name = "HC-05"
        self.available_devices = ["HC-05", "HC-06", "Arduino_BT"]
    
    def scan_devices(self):
        return self.available_devices
    
    def connect(self, device_name):
        self.device_name = device_name
        self.connected = True
        return True
    
    def disconnect(self):
        self.connected = False
    
    def receive_data(self):
        if self.connected:
            import random
            return random.randint(0, 1023)
        return None
    
    def is_connected(self):
        return self.connected


bt_manager = BluetoothManager()


# ═════════════════════════════════════════════════════════════════════════════
# 🎬 SPLASH EKRANI (Elit Fade animasyonu + 3s)
# ═════════════════════════════════════════════════════════════════════════════

class SplashScreen(Screen):
    """Profesyonel splash ekranı"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = FloatLayout()
        
        # Wireframe arka plan
        bg = WireframeWidget(size_hint=(1, 1), pos_hint={"x": 0, "y": 0})
        layout.add_widget(bg)
        
        # Merkez içerik
        center = FloatLayout(size_hint=(0.8, 0.5), pos_hint={"center_x": 0.5, "center_y": 0.5})
        
        # Logo/Başlık
        self.logo_label = Label(
            text="⚡",
            font_size="80sp",
            color=Theme.neon_blue,
            opacity=0,
            size_hint=(None, None),
            size=(100, 100),
            pos_hint={"center_x": 0.5, "center_y": 0.7}
        )
        center.add_widget(self.logo_label)
        
        # Başlık
        self.title_label = Label(
            text="ELIXIR TECHNOLOGY",
            font_size="52sp",
            bold=True,
            color=Theme.neon_blue,
            opacity=0,
            size_hint=(1, None),
            height="70dp",
            pos_hint={"center_x": 0.5, "top": 0.65}
        )
        center.add_widget(self.title_label)
        
        # Alt başlık
        self.subtitle_label = Label(
            text="YERÜSTÜ TARAMA SİSTEMİ",
            font_size="18sp",
            color=Theme.neon_cyan,
            opacity=0,
            size_hint=(1, None),
            height="30dp",
            pos_hint={"center_x": 0.5, "top": 0.45}
        )
        center.add_widget(self.subtitle_label)
        
        # Loading bar
        self.loading_label = Label(
            text="━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            font_size="14sp",
            color=Theme.neon_green,
            opacity=0,
            size_hint=(1, None),
            height="20dp",
            pos_hint={"center_x": 0.5, "top": 0.25}
        )
        center.add_widget(self.loading_label)
        
        # Versiyon bilgisi
        self.version_label = Label(
            text="© 2025 ELIXIR TECH | v1.0",
            font_size="10sp",
            color=Theme.text_dim,
            opacity=0,
            size_hint=(1, None),
            height="15dp",
            pos_hint={"center_x": 0.5, "top": 0.05}
        )
        center.add_widget(self.version_label)
        
        layout.add_widget(center)
        self.add_widget(layout)
    
    def on_enter(self):
        self._start_animation()
    
    def _start_animation(self):
        # Logo fade-in
        anim1 = Animation(opacity=1, duration=0.6)
        anim1.start(self.logo_label)
        
        # Başlık fade-in
        Clock.schedule_once(
            lambda dt: Animation(opacity=1, duration=0.8).start(self.title_label),
            0.2
        )
        
        # Alt başlık fade-in
        Clock.schedule_once(
            lambda dt: Animation(opacity=1, duration=0.6).start(self.subtitle_label),
            0.6
        )
        
        # Loading fade-in
        Clock.schedule_once(
            lambda dt: Animation(opacity=1, duration=0.5).start(self.loading_label),
            1.0
        )
        
        # Version fade-in
        Clock.schedule_once(
            lambda dt: Animation(opacity=1, duration=0.4).start(self.version_label),
            1.4
        )
        
        # Loading pulse
        self._loading_pulse()
        
        # Menüye geç
        Clock.schedule_once(self._go_to_menu, 3.0)
    
    def _loading_pulse(self):
        """Loading göstergesi pulse"""
        dots = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        for i, dot in enumerate(dots):
            Clock.schedule_once(
                lambda dt, d=dot: setattr(self.loading_label, "text", d) or True,
                1.0 + (i * 0.15)
            )
    
    def _go_to_menu(self, dt):
        self.manager.transition = SlideTransition(direction="up", duration=0.5)
        self.manager.current = "menu"


# ═════════════════════════════════════════════════════════════════════════════
# 📋 ANA MENÜ EKRANI (Elite Tasarım)
# ═════════════════════════════════════════════════════════════════════════════

class MenuScreen(Screen):
    """Profesyonel ana menü"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = FloatLayout()
        
        # Wireframe arka plan
        bg = WireframeWidget(size_hint=(1, 1), pos_hint={"x": 0, "y": 0})
        layout.add_widget(bg)
        
        # Ana kutu
        main_box = BoxLayout(orientation='vertical', size_hint=(0.9, 0.9), 
                            pos_hint={"center_x": 0.5, "center_y": 0.5},
                            padding=30, spacing=25)
        
        # Başlık
        header_box = BoxLayout(orientation='vertical', size_hint_y=0.15, spacing=10)
        
        title = Label(
            text="⚡ ELIXIR TECHNOLOGY ⚡",
            font_size='36sp',
            bold=True,
            color=Theme.neon_blue,
            size_hint_y=0.6
        )
        header_box.add_widget(title)
        
        subtitle = Label(
            text="YERÜSTÜ TARAMA SİSTEMİ | CYBERPUNK EDITION",
            font_size='14sp',
            color=Theme.neon_cyan,
            size_hint_y=0.4
        )
        header_box.add_widget(subtitle)
        
        main_box.add_widget(header_box)
        
        # Ayırıcı
        separator = Label(text="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
                         font_size='10sp', color=Theme.neon_blue, size_hint_y=0.05)
        main_box.add_widget(separator)
        
        # Buton grid
        button_grid = GridLayout(cols=2, rows=2, spacing=20, size_hint_y=0.60)
        
        buttons = [
            ("🌍\nYER ALTI\nGÖRÜNTÜLEME", "scan", Theme.neon_blue),
            ("📡\nPOINTER\nMOD", "pointer", Theme.neon_green),
            ("🧭\nPUSSULA\n(TTS)", "compass", Theme.neon_cyan),
            ("⚙️\nAYARLAR\nvE SETİNGLER", "settings", Theme.neon_red),
        ]
        
        for text, screen, color in buttons:
            btn = GlowingButton(text=text, glow_color=color, font_size='15sp')
            btn.bind(on_press=lambda x, s=screen: self._navigate(s))
            button_grid.add_widget(btn)
        
        main_box.add_widget(button_grid)
        
        # Footer
        footer_box = BoxLayout(orientation='vertical', size_hint_y=0.15, spacing=5)
        footer_box.add_widget(Label(text="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
                                   font_size='10sp', color=Theme.neon_blue))
        footer_box.add_widget(Label(text="v1.0 | Python 3.7+ | Kivy 2.3.0 | Bluetooth HC-05",
                                   font_size='10sp', color=Theme.text_dim))
        main_box.add_widget(footer_box)
        
        layout.add_widget(main_box)
        self.add_widget(layout)
    
    def _navigate(self, screen_name):
        self.manager.transition = SlideTransition(direction="left", duration=0.4)
        self.manager.current = screen_name


# ═════════════════════════════════════════════════════════════════════════════
# 🌍 YER ALTI GÖRÜNTÜLEME MODU
# ═════════════════════════════════════════════════════════════════════════════

class ScanScreen(Screen):
    """Yer altı görüntüleme"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scan_data = None
        self.scanning = False
        
        layout = FloatLayout()
        bg = WireframeWidget(size_hint=(1, 1), pos_hint={"x": 0, "y": 0})
        layout.add_widget(bg)
        
        main_box = BoxLayout(orientation='vertical', size_hint=(0.95, 0.95),
                            pos_hint={"center_x": 0.5, "center_y": 0.5},
                            padding=15, spacing=10)
        
        # Başlık
        header = Label(text='🌍 YER ALTI GÖRÜNTÜLEME MODU', font_size='20sp',
                      bold=True, color=Theme.neon_blue, size_hint_y=0.08)
        main_box.add_widget(header)
        
        # Bluetooth paneli
        bt_box = BoxLayout(size_hint_y=0.10, spacing=8)
        self.bt_status = Label(text="❌ Bağlı Değil", color=Theme.neon_red, size_hint_x=0.3)
        bt_box.add_widget(self.bt_status)
        
        self.bt_btn = GlowingButton(text="🔌 BAĞLAN", glow_color=Theme.neon_green, size_hint_x=0.35)
        self.bt_btn.bind(on_press=self._toggle_bt)
        bt_box.add_widget(self.bt_btn)
        
        info = Label(text="[ HC-05 Modülü ]", font_size='10sp', color=Theme.text_dim, size_hint_x=0.35)
        bt_box.add_widget(info)
        main_box.add_widget(bt_box)
        
        # Isı Haritası
        self.heatmap = Label(text="[ 2D Isı Haritası - Taramaya Başlayın ]",
                            font_size='12sp', color=Theme.text_dim, size_hint_y=0.50)
        main_box.add_widget(self.heatmap)
        
        # Kontrol butonları
        controls = GridLayout(cols=4, spacing=10, size_hint_y=0.12)
        
        start_btn = GlowingButton(text="▶ TARAMA", glow_color=Theme.neon_green)
        start_btn.bind(on_press=self._start_scan)
        controls.add_widget(start_btn)
        
        pause_btn = GlowingButton(text="⏸ DURAKLAT", glow_color=Theme.neon_cyan)
        controls.add_widget(pause_btn)
        
        export_btn = GlowingButton(text="💾 CSV", glow_color=Theme.neon_cyan)
        export_btn.bind(on_press=self._export_csv)
        controls.add_widget(export_btn)
        
        back_btn = GlowingButton(text="◀ GERİ", glow_color=Theme.neon_red)
        back_btn.bind(on_press=self._go_back)
        controls.add_widget(back_btn)
        
        main_box.add_widget(controls)
        layout.add_widget(main_box)
        self.add_widget(layout)
    
    def _toggle_bt(self, x):
        if not bt_manager.is_connected():
            bt_manager.connect("HC-05")
            self.bt_status.text = "✓ HC-05 Bağlı"
            self.bt_status.color = Theme.neon_green
        else:
            bt_manager.disconnect()
            self.bt_status.text = "❌ Bağlı Değil"
            self.bt_status.color = Theme.neon_red
    
    def _start_scan(self, x):
        if not bt_manager.is_connected():
            self.heatmap.text = "⚠ Önce Bluetooth'a bağlanın!"
            return
        self.scanning = True
        self.scan_data = np.random.randint(0, 1023, size=(5, 5))
        self._update_heatmap()
    
    def _update_heatmap(self):
        if self.scan_data is not None:
            text = "📊 2D ISI HARITASI (5x5 GRID)\n\n"
            for row in self.scan_data:
                for val in row:
                    if val < 341: text += "🔵 "
                    elif val < 682: text += "🟢 "
                    else: text += "🔴 "
                text += "\n"
            self.heatmap.text = text
    
    def _export_csv(self, x):
        if self.scan_data is None:
            self.heatmap.text = "⚠ Önce tarama yapın!"
            return
        filename = f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, 'w') as f:
            f.write("X,Y,Z,Derinlik\n")
            for i, row in enumerate(self.scan_data):
                for j, val in enumerate(row):
                    depth = -3 * val / (val + 1)
                    f.write(f"{j},{i},{val},{depth:.2f}\n")
        self.heatmap.text = f"✓ Kaydedildi: {filename}"
    
    def _go_back(self, x):
        self.manager.transition = SlideTransition(direction="right", duration=0.4)
        self.manager.current = "menu"


# ═════════════════════════════════════════════════════════════════════════════
# 📡 POINTER MOD (Gelişmiş Gösterge)
# ═════════════════════════════════════════════════════════════════════════════

class PointerScreen(Screen):
    """Pointer Mod - Dairesel gösterge"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.reading = False
        
        layout = FloatLayout()
        bg = WireframeWidget(size_hint=(1, 1), pos_hint={"x": 0, "y": 0})
        layout.add_widget(bg)
        
        main_box = BoxLayout(orientation='vertical', size_hint=(0.95, 0.95),
                            pos_hint={"center_x": 0.5, "center_y": 0.5},
                            padding=15, spacing=15)
        
        header = Label(text='📡 POINTER MOD - Gerçek Zamanlı Ölçüm',
                      font_size='20sp', bold=True, color=Theme.neon_green, size_hint_y=0.10)
        main_box.add_widget(header)
        
        # Gösterge alanı
        gauge_box = FloatLayout(size_hint_y=0.65)
        
        # Dış çember (arka plan)
        self.outer_circle = Label(text="", size_hint=(None, None), size=(250, 250),
                                 pos_hint={"center_x": 0.5, "center_y": 0.5})
        gauge_box.add_widget(self.outer_circle)
        
        # Değer göstergesi
        self.value_label = Label(text="0", font_size='72sp', bold=True,
                                color=Theme.neon_blue, size_hint=(None, None),
                                size=(200, 200),
                                pos_hint={"center_x": 0.5, "center_y": 0.5})
        gauge_box.add_widget(self.value_label)
        
        # Pulse göstergesi
        self.pulse_label = Label(text="●", font_size='100sp',
                                color=Theme.neon_green, size_hint=(None, None),
                                size=(150, 150),
                                pos_hint={"center_x": 0.5, "center_y": 0.5},
                                opacity=0.2)
        gauge_box.add_widget(self.pulse_label)
        
        main_box.add_widget(gauge_box)
        
        # Bilgi paneli
        info_box = BoxLayout(orientation='horizontal', size_hint_y=0.10, spacing=15)
        self.min_label = Label(text="Min: 0")
        self.max_label = Label(text="Max: 1023")
        self.color_label = Label(text="Reng: MAVI", color=Theme.neon_blue)
        info_box.add_widget(self.min_label)
        info_box.add_widget(self.max_label)
        info_box.add_widget(self.color_label)
        main_box.add_widget(info_box)
        
        # Kontrol butonları
        control_box = GridLayout(cols=3, spacing=10, size_hint_y=0.10)
        start_btn = GlowingButton(text="▶ BAŞLAT", glow_color=Theme.neon_green)
        start_btn.bind(on_press=self._start)
        control_box.add_widget(start_btn)
        
        stop_btn = GlowingButton(text="⏹ DURDUR", glow_color=Theme.neon_red)
        stop_btn.bind(on_press=self._stop)
        control_box.add_widget(stop_btn)
        
        back_btn = GlowingButton(text="◀ GERİ", glow_color=Theme.neon_red)
        back_btn.bind(on_press=self._go_back)
        control_box.add_widget(back_btn)
        
        main_box.add_widget(control_box)
        layout.add_widget(main_box)
        self.add_widget(layout)
    
    def _start(self, x):
        self.reading = True
        self._update()
    
    def _stop(self, x):
        self.reading = False
    
    def _update(self):
        if self.reading:
            import random
            val = random.randint(0, 1023)
            self.value_label.text = str(val)
            
            if val < 341:
                self.value_label.color = Theme.neon_blue
                self.color_label.text = "Reng: MAVI (Düşük)"
            elif val < 682:
                self.value_label.color = Theme.neon_green
                self.color_label.text = "Reng: YEŞİL (Orta)"
            else:
                self.value_label.color = Theme.neon_red
                self.color_label.text = "Reng: KIRMIZI (Yüksek)"
            
            # Pulse animasyonu
            anim = Animation(size=(200, 200), opacity=0, duration=0.6)
            anim.start(self.pulse_label)
            
            Clock.schedule_once(lambda dt: self._update(), 0.6)
    
    def _go_back(self, x):
        self.reading = False
        self.manager.transition = SlideTransition(direction="right", duration=0.4)
        self.manager.current = "menu"


# ═════════════════════════════════════════════════════════════════════════════
# 🧭 PUSULA EKRANI
# ═════════════════════════════════════════════════════════════════════════════

class CompassScreen(Screen):
    """Pusula"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = FloatLayout()
        bg = WireframeWidget(size_hint=(1, 1), pos_hint={"x": 0, "y": 0})
        layout.add_widget(bg)
        
        main_box = BoxLayout(orientation='vertical', size_hint=(0.95, 0.95),
                            pos_hint={"center_x": 0.5, "center_y": 0.5},
                            padding=15, spacing=15)
        
        header = Label(text='🧭 PUSULA - Türkçe Yönlendirme (TTS)',
                      font_size='20sp', bold=True, color=Theme.neon_cyan, size_hint_y=0.10)
        main_box.add_widget(header)
        
        # Pusula grid
        compass_grid = GridLayout(cols=3, rows=3, spacing=15, size_hint_y=0.65)
        
        compass_grid.add_widget(Label())
        
        north_btn = GlowingButton(text="▲\nKUZEY\n(Nord)", glow_color=Theme.neon_blue)
        north_btn.bind(on_press=lambda x: self._speak("Kuzey"))
        compass_grid.add_widget(north_btn)
        
        compass_grid.add_widget(Label())
        
        west_btn = GlowingButton(text="◀ BATI\n(West)", glow_color=Theme.neon_blue)
        west_btn.bind(on_press=lambda x: self._speak("Batı"))
        compass_grid.add_widget(west_btn)
        
        center = Label(text="⊙\nMEVCUT\nKONUM", font_size='18sp', bold=True, color=Theme.neon_green)
        compass_grid.add_widget(center)
        
        east_btn = GlowingButton(text="DOĞU ▶\n(East)", glow_color=Theme.neon_blue)
        east_btn.bind(on_press=lambda x: self._speak("Doğu"))
        compass_grid.add_widget(east_btn)
        
        compass_grid.add_widget(Label())
        
        south_btn = GlowingButton(text="▼\nGÜNEY\n(Kuzey)", glow_color=Theme.neon_blue)
        south_btn.bind(on_press=lambda x: self._speak("Güney"))
        compass_grid.add_widget(south_btn)
        
        compass_grid.add_widget(Label())
        
        main_box.add_widget(compass_grid)
        
        self.tts_label = Label(text="[ TTS Hazır - Yöne Tıklayın ]",
                              font_size='12sp', color=Theme.text_dim, size_hint_y=0.10)
        main_box.add_widget(self.tts_label)
        
        back_btn = GlowingButton(text="◀ GERİ", glow_color=Theme.neon_red, size_hint_y=0.10)
        back_btn.bind(on_press=self._go_back)
        main_box.add_widget(back_btn)
        
        layout.add_widget(main_box)
        self.add_widget(layout)
    
    def _speak(self, direction):
        self.tts_label.text = f"🔊 Konuşuluyor: {direction}"
    
    def _go_back(self, x):
        self.manager.transition = SlideTransition(direction="right", duration=0.4)
        self.manager.current = "menu"


# ═════════════════════════════════════════════════════════════════════════════
# ⚙️ AYARLAR EKRANI
# ═════════════════════════════════════════════════════════════════════════════

class SettingsScreen(Screen):
    """Ayarlar"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = FloatLayout()
        bg = WireframeWidget(size_hint=(1, 1), pos_hint={"x": 0, "y": 0})
        layout.add_widget(bg)
        
        main_box = BoxLayout(orientation='vertical', size_hint=(0.95, 0.95),
                            pos_hint={"center_x": 0.5, "center_y": 0.5},
                            padding=15, spacing=15)
        
        header = Label(text='⚙️ AYARLAR VE SETİNGLER',
                      font_size='20sp', bold=True, color=Theme.neon_red, size_hint_y=0.10)
        main_box.add_widget(header)
        
        # Ayarlar alanı
        settings_box = BoxLayout(orientation='vertical', size_hint_y=0.75, spacing=15)
        
        # Bluetooth
        bt_section = BoxLayout(orientation='horizontal', size_hint_y=0.15, spacing=10)
        bt_section.add_widget(Label(text="📡 Bluetooth Cihazları:", size_hint_x=0.4))
        bt_status = Label(text="✓ HC-05" if bt_manager.is_connected() else "❌ Bağlı Değil",
                         color=Theme.neon_green if bt_manager.is_connected() else Theme.neon_red,
                         size_hint_x=0.6)
        bt_section.add_widget(bt_status)
        settings_box.add_widget(bt_section)
        
        # Bilgiler
        info_section = BoxLayout(orientation='vertical', size_hint_y=0.25, spacing=5)
        info_section.add_widget(Label(text="ℹ️ UYGULAMA BİLGİLERİ", bold=True))
        info_section.add_widget(Label(text="Versiyon: 1.0.0", font_size='10sp', color=Theme.text_dim))
        info_section.add_widget(Label(text="Python 3.7+ | Kivy 2.3.0", font_size='10sp', color=Theme.text_dim))
        info_section.add_widget(Label(text="© 2025 ELIXIR TECH", font_size='10sp', color=Theme.text_dim))
        settings_box.add_widget(info_section)
        
        # İzinler
        perms_section = BoxLayout(orientation='vertical', size_hint_y=0.20, spacing=5)
        perms_section.add_widget(Label(text="🔐 İZİNLER", bold=True))
        perms_section.add_widget(Label(text="✓ Bluetooth\n✓ Depolama\n✓ Konum",
                                      font_size='10sp', color=Theme.text_dim))
        settings_box.add_widget(perms_section)
        
        main_box.add_widget(settings_box)
        
        back_btn = GlowingButton(text="◀ GERİ", glow_color=Theme.neon_red, size_hint_y=0.10)
        back_btn.bind(on_press=self._go_back)
        main_box.add_widget(back_btn)
        
        layout.add_widget(main_box)
        self.add_widget(layout)
    
    def _go_back(self, x):
        self.manager.transition = SlideTransition(direction="right", duration=0.4)
        self.manager.current = "menu"


# ═════════════════════════════════════════════════════════════════════════════
# 🚀 ANA UYGULAMA
# ═════════════════════════════════════════════════════════════════════════════

class ElixirApp(App):
    """ELIXIR TECHNOLOGY"""
    
    def build(self):
        sm = ScreenManager(transition=SlideTransition())
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(ScanScreen(name="scan"))
        sm.add_widget(PointerScreen(name="pointer"))
        sm.add_widget(CompassScreen(name="compass"))
        sm.add_widget(SettingsScreen(name="settings"))
        sm.current = "splash"
        return sm


if __name__ == '__main__':
    ElixirApp().run()

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

import numpy as np
from datetime import datetime

# ═════════════════════════════════════════════════════════════════════════════
# 🎨 TEMA - CYBERPUNK WIREFRAME
# ═════════════════════════════════════════════════════════════════════════════

class Theme:
    """Cyberpunk tema renkleri"""
    bg = get_color_from_hex("#050505")
    neon_blue = get_color_from_hex("#00F2FF")
    neon_cyan = get_color_from_hex("#00FFCC")
    neon_red = get_color_from_hex("#FF0033")
    neon_green = get_color_from_hex("#00FF88")
    text_dim = get_color_from_hex("#4A8FA8")

Window.clearcolor = Theme.bg
Window.size = (1024, 768)
Window.title = "⚡ ELIXIR TECHNOLOGY - Yerüstü Tarama Sistemi"


# ═════════════════════════════════════════════════════════════════════════════
# 📡 BLUETOOTH BAĞLANTISI (Mock)
# ═════════════════════════════════════════════════════════════════════════════

class BluetoothManager:
    """Bluetooth HC-05 yönetimi"""
    
    def __init__(self):
        self.connected = False
        self.device_name = "HC-05"
        self.available_devices = ["HC-05", "HC-06", "Arduino_BT"]
    
    def scan_devices(self):
        return self.available_devices
    
    def connect(self, device_name):
        self.device_name = device_name
        self.connected = True
        return True
    
    def disconnect(self):
        self.connected = False
    
    def receive_data(self):
        if self.connected:
            import random
            return random.randint(0, 1023)
        return None
    
    def is_connected(self):
        return self.connected


bt_manager = BluetoothManager()


# ═════════════════════════════════════════════════════════════════════════════
# 🎬 SPLASH EKRANI (Fade animasyonu + 3s)
# ═════════════════════════════════════════════════════════════════════════════

class SplashScreen(Screen):
    """3 saniyeli fade animasyonlu giriş ekranı"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = FloatLayout()
        
        # Başlık
        self.title_label = Label(
            text="⚡ ELIXIR TECHNOLOGY ⚡",
            font_size="48sp",
            bold=True,
            color=Theme.neon_blue,
            opacity=0,
            size_hint=(1, 0.3),
            pos_hint={"center_x": 0.5, "center_y": 0.60}
        )
        layout.add_widget(self.title_label)
        
        # Alt başlık
        self.subtitle_label = Label(
            text="YERÜSTÜ TARAMA SİSTEMİ v1.0",
            font_size="16sp",
            color=Theme.text_dim,
            opacity=0,
            size_hint=(1, 0.2),
            pos_hint={"center_x": 0.5, "center_y": 0.40}
        )
        layout.add_widget(self.subtitle_label)
        
        # Loading
        self.loading_label = Label(
            text="[ Sistem başlatılıyor... ]",
            font_size="12sp",
            color=Theme.neon_green,
            opacity=0,
            size_hint=(1, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.25}
        )
        layout.add_widget(self.loading_label)
        
        self.add_widget(layout)
    
    def on_enter(self):
        # Fade-in animasyonları
        anim1 = Animation(opacity=1, duration=0.8)
        anim1.start(self.title_label)
        
        Clock.schedule_once(
            lambda dt: Animation(opacity=1, duration=0.6).start(self.subtitle_label),
            0.3
        )
        
        Clock.schedule_once(
            lambda dt: Animation(opacity=1, duration=0.6).start(self.loading_label),
            0.6
        )
        
        # Ana menüye geç
        Clock.schedule_once(self._go_to_menu, 3.0)
    
    def _go_to_menu(self, dt):
        self.manager.transition = SlideTransition(direction="up", duration=0.5)
        self.manager.current = "menu"


# ═════════════════════════════════════════════════════════════════════════════
# 📋 ANA MENÜ EKRANI
# ═════════════════════════════════════════════════════════════════════════════

class MenuScreen(Screen):
    """Ana menü - 4 ana buton"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Başlık
        header = BoxLayout(orientation='vertical', size_hint_y=0.20)
        header.add_widget(Label(
            text='⚡ ELIXIR TECHNOLOGY ⚡',
            font_size='28sp',
            bold=True,
            color=Theme.neon_blue
        ))
        header.add_widget(Label(
            text='YERÜSTÜ TARAMA SİSTEMİ',
            font_size='14sp',
            color=Theme.text_dim
        ))
        layout.add_widget(header)
        
        # Buton grid
        buttons_grid = GridLayout(cols=2, spacing=12, size_hint_y=0.60)
        
        buttons = [
            ("🌍 YER ALTI\nGÖRÜNTÜLEME", "scan", Theme.neon_blue),
            ("📡 POINTER\nMOD", "pointer", Theme.neon_green),
            ("🧭 PUSULA\n(TTS)", "compass", Theme.neon_cyan),
            ("⚙️ AYARLAR", "settings", Theme.neon_red),
        ]
        
        for text, screen, color in buttons:
            btn = Button(text=text, font_size='14sp', background_color=(0, 0, 0, 0.3))
            btn.color = color
            btn.bind(on_press=lambda x, s=screen: self._navigate(s))
            buttons_grid.add_widget(btn)
        
        layout.add_widget(buttons_grid)
        
        footer = BoxLayout(orientation='vertical', size_hint_y=0.20)
        footer.add_widget(Label(text="v1.0 | © 2025 ELIXIR TECH", font_size='9sp', color=Theme.text_dim))
        layout.add_widget(footer)
        
        self.add_widget(layout)
    
    def _navigate(self, screen_name):
        self.manager.transition = SlideTransition(direction="left", duration=0.4)
        self.manager.current = screen_name


# ═════════════════════════════════════════════════════════════════════════════
# 🌍 YER ALTI GÖRÜNTÜLEME MODU
# ═════════════════════════════════════════════════════════════════════════════

class ScanScreen(Screen):
    """Yer altı görüntüleme"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scan_data = None
        self.scanning = False
        
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        header = Label(text='🌍 YER ALTI GÖRÜNTÜLEME', font_size='18sp', bold=True, color=Theme.neon_blue, size_hint_y=0.10)
        layout.add_widget(header)
        
        # Bluetooth bağlantı
        bt_box = BoxLayout(orientation='horizontal', size_hint_y=0.10, spacing=10)
        self.bt_status = Label(text="❌ Bağlı Değil", color=Theme.neon_red)
        bt_box.add_widget(self.bt_status)
        self.bt_btn = Button(text="🔌 BAĞLAN", size_hint_x=0.3)
        self.bt_btn.bind(on_press=self._toggle_bt)
        bt_box.add_widget(self.bt_btn)
        layout.add_widget(bt_box)
        
        # Isı Haritası
        self.heatmap = Label(text="[ 2D Isı Haritası - Taramaya Başlayın ]", font_size='12sp', color=Theme.text_dim)
        layout.add_widget(self.heatmap)
        
        # Kontrol butonları
        controls = GridLayout(cols=3, spacing=8, size_hint_y=0.15)
        start = Button(text="▶ TARAMA", background_color=(0, 0.5, 0, 0.5))
        start.bind(on_press=self._start_scan)
        controls.add_widget(start)
        
        export = Button(text="💾 CSV", background_color=(0.3, 0.3, 0.3, 0.5))
        export.bind(on_press=self._export_csv)
        controls.add_widget(export)
        
        back = Button(text="◀ GERİ", background_color=(0.5, 0, 0, 0.5))
        back.bind(on_press=self._go_back)
        controls.add_widget(back)
        
        layout.add_widget(controls)
        self.add_widget(layout)
    
    def _toggle_bt(self, x):
        if not bt_manager.is_connected():
            bt_manager.connect("HC-05")
            self.bt_status.text = "✓ HC-05 Bağlı"
            self.bt_status.color = Theme.neon_green
        else:
            bt_manager.disconnect()
            self.bt_status.text = "❌ Bağlı Değil"
            self.bt_status.color = Theme.neon_red
    
    def _start_scan(self, x):
        if not bt_manager.is_connected():
            self.heatmap.text = "⚠ Önce Bluetooth'a bağlanın!"
            return
        self.scanning = True
        self.scan_data = np.random.randint(0, 1023, size=(5, 5))
        self._update_heatmap()
    
    def _update_heatmap(self):
        if self.scan_data is not None:
            text = "📊 2D ISI HARITASI\n\n"
            for row in self.scan_data:
                for val in row:
                    if val < 341: text += "🔵 "
                    elif val < 682: text += "🟢 "
                    else: text += "🔴 "
                text += "\n"
            self.heatmap.text = text
    
    def _export_csv(self, x):
        if self.scan_data is None:
            self.heatmap.text = "⚠ Önce tarama yapın!"
            return
        filename = f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, 'w') as f:
            f.write("X,Y,Z,Derinlik\n")
            for i, row in enumerate(self.scan_data):
                for j, val in enumerate(row):
                    depth = -3 * val / (val + 1)
                    f.write(f"{j},{i},{val},{depth:.2f}\n")
        self.heatmap.text = f"✓ Kaydedildi: {filename}"
    
    def _go_back(self, x):
        self.manager.transition = SlideTransition(direction="right", duration=0.4)
        self.manager.current = "menu"


# ═════════════════════════════════════════════════════════════════════════════
# 📡 POINTER MOD
# ═════════════════════════════════════════════════════════════════════════════

class PointerScreen(Screen):
    """Pointer Mod"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.reading = False
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        header = Label(text='📡 POINTER MOD - Gerçek Zamanlı', font_size='18sp', bold=True, color=Theme.neon_green, size_hint_y=0.10)
        layout.add_widget(header)
        
        # Gösterge
        gauge = FloatLayout(size_hint_y=0.60)
        self.value_label = Label(text="0", font_size='72sp', bold=True, color=Theme.neon_blue, size=(200, 200), pos_hint={"center_x": 0.5, "center_y": 0.5})
        gauge.add_widget(self.value_label)
        layout.add_widget(gauge)
        
        self.color_label = Label(text="Reng: MAVI", font_size='12sp', color=Theme.text_dim, size_hint_y=0.10)
        layout.add_widget(self.color_label)
        
        controls = GridLayout(cols=2, spacing=10, size_hint_y=0.15)
        start = Button(text="▶ BAŞLAT", background_color=(0, 0.5, 0, 0.5))
        start.bind(on_press=self._start)
        controls.add_widget(start)
        
        back = Button(text="◀ GERİ", background_color=(0.5, 0, 0, 0.5))
        back.bind(on_press=self._go_back)
        controls.add_widget(back)
        
        layout.add_widget(controls)
        self.add_widget(layout)
    
    def _start(self, x):
        self.reading = not self.reading
        if self.reading:
            self._update()
    
    def _update(self):
        if self.reading:
            import random
            val = random.randint(0, 1023)
            self.value_label.text = str(val)
            if val < 341:
                self.value_label.color = Theme.neon_blue
                self.color_label.text = "Reng: MAVI (Düşük)"
            elif val < 682:
                self.value_label.color = Theme.neon_green
                self.color_label.text = "Reng: YEŞİL (Orta)"
            else:
                self.value_label.color = Theme.neon_red
                self.color_label.text = "Reng: KIRMIZI (Yüksek)"
            Clock.schedule_once(lambda dt: self._update(), 0.5)
    
    def _go_back(self, x):
        self.reading = False
        self.manager.transition = SlideTransition(direction="right", duration=0.4)
        self.manager.current = "menu"


# ═════════════════════════════════════════════════════════════════════════════
# 🧭 PUSULA EKRANI (TTS)
# ═════════════════════════════════════════════════════════════════════════════

class CompassScreen(Screen):
    """Pusula"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        header = Label(text='🧭 PUSULA - Türkçe Yönlendirme', font_size='18sp', bold=True, color=Theme.neon_cyan, size_hint_y=0.10)
        layout.add_widget(header)
        
        compass = GridLayout(cols=3, rows=3, spacing=15, size_hint_y=0.60)
        
        compass.add_widget(Label())
        north = Button(text="▲\nKUZEY", background_color=(0, 0.3, 0.5, 0.7))
        north.bind(on_press=lambda x: self._speak("Kuzey"))
        compass.add_widget(north)
        compass.add_widget(Label())
        
        west = Button(text="◀ BATI", background_color=(0, 0.3, 0.5, 0.7))
        west.bind(on_press=lambda x: self._speak("Batı"))
        compass.add_widget(west)
        
        center = Label(text="⊙\nKONUM", font_size='16sp', bold=True, color=Theme.neon_green)
        compass.add_widget(center)
        
        east = Button(text="DOĞU ▶", background_color=(0, 0.3, 0.5, 0.7))
        east.bind(on_press=lambda x: self._speak("Doğu"))
        compass.add_widget(east)
        
        compass.add_widget(Label())
        south = Button(text="▼\nGÜNEY", background_color=(0, 0.3, 0.5, 0.7))
        south.bind(on_press=lambda x: self._speak("Güney"))
        compass.add_widget(south)
        compass.add_widget(Label())
        
        layout.add_widget(compass)
        
        self.tts_label = Label(text="[ TTS Hazır ]", font_size='12sp', color=Theme.text_dim, size_hint_y=0.10)
        layout.add_widget(self.tts_label)
        
        back = Button(text="◀ GERİ", background_color=(0.5, 0, 0, 0.5), size_hint_y=0.15)
        back.bind(on_press=self._go_back)
        layout.add_widget(back)
        
        self.add_widget(layout)
    
    def _speak(self, direction):
        self.tts_label.text = f"🔊 {direction}"
    
    def _go_back(self, x):
        self.manager.transition = SlideTransition(direction="right", duration=0.4)
        self.manager.current = "menu"


# ═════════════════════════════════════════════════════════════════════════════
# ⚙️ AYARLAR EKRANI
# ═════════════════════════════════════════════════════════════════════════════

class SettingsScreen(Screen):
    """Ayarlar"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        header = Label(text='⚙️ AYARLAR', font_size='18sp', bold=True, color=Theme.neon_red, size_hint_y=0.10)
        layout.add_widget(header)
        
        info = BoxLayout(orientation='vertical', size_hint_y=0.70, spacing=10)
        info.add_widget(Label(text="📡 Bluetooth Cihazları:", bold=True))
        info.add_widget(Label(text="HC-05 / HC-06 / Arduino_BT"))
        info.add_widget(Label(text=""))
        info.add_widget(Label(text="ℹ️ UYGULAMA BİLGİLERİ", bold=True))
        info.add_widget(Label(text="Versiyon: 1.0.0"))
        info.add_widget(Label(text="Python 3.7+ | Kivy 2.3.0"))
        info.add_widget(Label(text=""))
        info.add_widget(Label(text="🔐 İZİNLER"))
        info.add_widget(Label(text="✓ Bluetooth ✓ Depolama ✓ Konum"))
        layout.add_widget(info)
        
        back = Button(text="◀ GERİ", background_color=(0.5, 0, 0, 0.7), size_hint_y=0.15)
        back.bind(on_press=self._go_back)
        layout.add_widget(back)
        
        self.add_widget(layout)
    
    def _go_back(self, x):
        self.manager.transition = SlideTransition(direction="right", duration=0.4)
        self.manager.current = "menu"


# ═════════════════════════════════════════════════════════════════════════════
# 🚀 ANA UYGULAMA
# ═════════════════════════════════════════════════════════════════════════════

class ElixirApp(App):
    """ELIXIR TECHNOLOGY"""
    
    def build(self):
        sm = ScreenManager(transition=SlideTransition())
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(ScanScreen(name="scan"))
        sm.add_widget(PointerScreen(name="pointer"))
        sm.add_widget(CompassScreen(name="compass"))
        sm.add_widget(SettingsScreen(name="settings"))
        sm.current = "splash"
        return sm


if __name__ == '__main__':
    ElixirApp().run()
