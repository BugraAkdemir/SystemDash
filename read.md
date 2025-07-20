# SystemDash

🔧 **SystemDash**, sisteminizin anlık CPU, RAM, işlemci sıcaklığı ve aktif işlem verilerini izleyen ve bunları REST API olarak sunan basit ama güçlü bir Python uygulamasıdır.

> ⚡ Gerçek zamanlı veriler | 🖥 Arayüzsüz arka plan izleme | 🌡️ LibreHardwareMonitor entegrasyonu

---

## 🚀 Özellikler

- ✅ CPU ve RAM kullanımını gösterir
- ✅ En fazla kaynak kullanan ilk 5 işlemi listeler
- ✅ CPU sıcaklığını görüntüler (Libre Hardware Monitor üzerinden)
- ✅ FastAPI tabanlı API sunar
- ✅ HTML arayüz desteği (opsiyonel)
- ✅ Platform: Windows (WMI desteği gereklidir)

---

## 🛠️ Kurulum

### 1. Gerekli Paketler

Python 3.7+ sisteminize yüklü olmalıdır.

```bash
pip install fastapi psutil wmi uvicorn
```

## 🚩 Çalıştırma

### Dosyanın Olduğu Klasöre Girin

Python 3.7+ sisteminize yüklü olmalıdır.

- Sağ Tıklayıp Terminalde Aç Diyip
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
- Portu Değiştirebilirsiniz

- Cmd'ye Girip
```bash
ipconfig
```
- Çıkan İp İle Kulanacağınız Cihaza Gidip Tarayıcıya
```
192.168."Senin İp":8000
```
- Bu Link İle Programı Kulanmaya Başlayabilirsin

## 🛑 Kapatma

### Kapatmak İçin

- Acılan Cmd Pencerisine Ctrl+c Veya Direk Olarak Kapatabilir
- Gizli Simgeleri Göstere Gelip LibreHardwareMonitor Adlı Programı Kapatabilrisiniz

---

### 👤 CR

> Developed by [Buğra Akdemir](https://github.com/bugraakdemir)