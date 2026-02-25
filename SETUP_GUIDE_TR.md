# ELIXIR TECHNOLOGY - Kurulum ve Çalıştırma Rehberi

## 🔧 Hızlı Başlangıç

### Windows'ta Test Etmek (En Kolay Yol)

```bash
# PowerShell'de çalıştırın:
python -m pip install --upgrade pip
pip install kivy==2.3.0 kivymd==1.2.0 pillow numpy

# Sonra uygulamayı çalıştırın:
python main.py
```

### WSL2'de Android APK Oluşturmak (Önerilen - GitHub Actions)

#### Adım 1: WSL2 Kurulumu (İlk Seferinde)
```bash
# PowerShell'de (Admin):
wsl --install
wsl --set-default-version 2

# WSL'e girin:
wsl

# Linux'ta kurulum dosyasını çalıştırın:
chmod +x setup_wsl.sh
./setup_wsl.sh
```

#### Adım 2: Sanal Ortamı Etkinleştirme (Her Seferinde)
```bash
source ~/.venv-elixir/bin/activate

# Artık APK oluşturabilirsiniz:
cd /mnt/c/Users/erbay/OneDrive/Belgeler/GitHub/yeter
buildozer android debug
```

## ❌ Hata Çözümleri

### Hata: "externally-managed-environment" (WSL'de)
**Çözüm:** Sanal ortam (venv) kullanın
```bash
python3 -m venv ~/.venv-elixir
source ~/.venv-elixir/bin/activate
pip install buildozer cython==0.29.37
```

### Hata: "ls -la command not found" (PowerShell'de)
**Çözüm:** PowerShell'in kendi komutlarını kullanın
```powershell
# ❌ Yanlış:
ls -la

# ✅ Doğru:
Get-ChildItem -Force

# ✅ Kısa yazılışı:
dir -Force
```

### Hata: "mkdir -p command not found" (PowerShell'de)
**Çözüm:** PowerShell New-Item kullanın
```powershell
# ❌ Yanlış:
mkdir -p src/screens src/utils

# ✅ Doğru:
New-Item -ItemType Directory -Path "src/screens", "src/utils" -Force
```

### Hata: "buildozer: command not found" (Windows PowerShell'de)
**Çözüm:** Buildozer Windows'ta doğrudan kullanılamaz. WSL2 kullanın.

## 📁 Proje Yapısı (Doğru Format)

```
yeter/
├── main.py                    # Ana uygulama
├── buildozer.spec             # Android build ayarları
├── build.yml                  # GitHub Actions workflow
├── setup_windows.bat          # Windows kurulum
├── setup_wsl.sh               # WSL kurulum
│
├── src/
│   ├── main.py                # (Backup)
│   ├── components/            # Yeniden kullanılabilir bileşenler
│   ├── screens/               # Uygulamadaki ekranlar
│   │   ├── scan.py           # Yer altı görüntüleme
│   │   ├── pointer.py        # Bluetooth pointer
│   │   ├── compass.py        # Pusula
│   │   └── settings.py       # Ayarlar
│   └── utils/                 # Yardımcı fonksiyonlar
│
├── bin/                       # (Eğer gerekli ise)
│
└── .github/
    └── workflows/
        └── build.yml          # Otomatik APK üretim
```

## 🎯 Bir Sonraki Adımlar

1. **Windows'ta test edin**: `python main.py`
2. **Ekranları geliştirin**: `src/screens/` klasöründeki dosyaları düzenleyin
3. **GitHub'a push edin** (APK otomatik oluşacak)
4. Veya **WSL'de manuel APK oluşturun**: `buildozer android debug`

## 📦 Kurulan Paketler

- **kivy**: 2.3.0 - UI Framework
- **kivymd**: 1.2.0 - Material Design bileşenleri
- **buildozer**: 1.5.0 - Android APK oluşturucu
- **cython**: 0.29.37 - Performans optimizasyonu
- **pillow**: Görüntü işleme
- **numpy**: Sayısal hesaplama

## 🚀 GitHub Actions ile Otomatik APK Oluşturma

Push ettiğiniz zaman otomatik olarak APK oluşturulur:

1. Repository'yi GitHub'a push edin
2. "Actions" sekmesine gidin
3. "Build Elixir APK" workflow'u görün
4. İşlem bitince "Artifacts" bölümünden APK'yı indirin
