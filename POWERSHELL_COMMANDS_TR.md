# PowerShell vs Unix Commands - Rehberi

Windows'ta çalışırken Unix komutları çalışmaz. İşte doğru PowerShell komutları:

## Dosya/Klasör İşlemleri

| Operasyon | Unix (Linux/Mac) | Windows PowerShell | Açıklama |
|-----------|---|---|---|
| Dosya listeleme | `ls` veya `ls -la` | `dir` veya `Get-ChildItem` | Gizli dosyları göster: `-Force` |
| Klasör oluştur | `mkdir -p dir1/dir2` | `New-Item -ItemType Directory -Path "dir1/dir2" -Force` | PowerShell `-Force` ile üst klasörleri oluştur |
| Klasörü değiştir | `cd dir` | `cd dir` | PowerShell'de `cd` da çalışır |
| Mevcut klasör | `pwd` | `Get-Location` veya `$PWD` | |
| Dosya sil | `rm file.txt` | `Remove-Item file.txt` | |
| Klasörü sil | `rm -r dirname` | `Remove-Item -Recurse dirname` | |
| Çıktı dosyaya | `command > file.txt` | `command | Out-File file.txt` | Append: `>> file.txt` |
| Ekle dosyaya | `echo "text" >> file.txt` | `"text" | Add-Content file.txt` | |

## Python İçin Doğru Komutlar

```powershell
# ✅ DOĞRU:
python main.py
pip install kivy
python -m pip list
python -m venv venv
.\venv\Scripts\Activate   # Virtual env aktive et

# ❌ YANLIŞ (Unix komutları):
python3 main.py          # Windows'ta 'python' kullan
pip3 install kivy         # Windows'ta 'pip' kullan
source venv/bin/activate  # WSL'de kullan, PowerShell'de değil
```

## WSL'de Çalışan Komutlar (Ubuntu/Linux)

Eğer `wsl` yazıp Linux'a geçtiyseniz, Unix komutları kullanın:

```bash
# ✅ WSL'de çalışır:
ls -la
mkdir -p src/screens
python3 main.py
source venv/bin/activate

# ❌ WSL'de çalışmaz:
Get-ChildItem  # PowerShell komutu
New-Item       # PowerShell komutu
```

## Hızlı Referans - Geleneksel Komutlar Türkçesi

PowerShell'de Unix komutlarını simule etmek istiyorsanız, alias kullanabilirsiniz:

```powershell
# İsteğe bağlı aliaslar ekleyin (Powershell profiline):
Set-Alias -Name ls -Value Get-ChildItem -Force
Set-Alias -Name rm -Value Remove-Item -Force
Set-Alias -Name pwd -Value Get-Location -Force
Set-Alias -Name mkdir -Value New-Item -Force -OptionName Directory
```

## Penceyi Kapat / Programı Durdur

```powershell
# Ctrl+C   # Çalışan programı durdur
# exit     # Terminal/WSL'den çık
```
