# ELIXIR TECHNOLOGY 📡

> Cyberpunk Wireframe Android Tarama Uygulaması

## Özellikler
- 🌍 Yer Altı Görüntüleme (Grid + 2D/3D Isı Haritası)
- 📡 Pointer Mod (Bluetooth HC-05 gerçek zamanlı)
- 🧭 Pusula (Türkçe TTS)
- ⚙️ Ayarlar

## PC'de Test (Windows)
```bash
# PowerShell'de:
pip install kivy==2.3.0 kivymd==1.2.0 pillow
python main.py
```

## APK Build Seçenekleri

### Seçenek A: GitHub Actions (Önerilen - Kolay)
1. Bu repoyu GitHub'a push edin
2. Actions sekmesine gidin
3. "Build Elixir APK" workflow'u otomatik çalışacak
4. ✅ 10-15 dakika sonra Artifacts'tan APK'yı indirin

### Seçenek B: WSL2 ile Local Build (İleri Düzey)
```bash
# İlk seferinde:
wsl
chmod +x setup_wsl.sh
./setup_wsl.sh

# Sonraki sefer:
wsl
source ~/.venv-elixir/bin/activate
cd /mnt/c/Users/erbay/OneDrive/Belgeler/GitHub/yeter
buildozer android debug
```

## Proje Yapısı
```
elixir_app/
├── main.py              # Ana uygulama (Splash + Menü)
├── screens/
│   ├── scan.py          # Yer altı görüntüleme (yakında)
│   ├── pointer.py       # Pointer mod (yakında)
│   ├── compass.py       # Pusula (yakında)
│   └── settings.py      # Ayarlar (yakında)
├── buildozer.spec       # Android build ayarları
└── .github/
    └── workflows/
        └── build.yml    # Otomatik APK build
```

## Tema Renkleri
| Renk | Hex | Kullanım |
|------|-----|---------|
| Neon Blue | `#00F2FF` | Ana vurgu, butonlar |
| Laser Red | `#FF0033` | Uyarılar, geri butonu |
| Neon Green | `#00FF88` | Pointer mod |
| BG Dark | `#050505` | Arka plan |
