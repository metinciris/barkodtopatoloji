
```python
# Gerekli kütüphaneler
import cv2
import pytesseract
import pyzbar.pyzbar as pyzbar
import requests  # Enlil sistemi için gerekli
import pyttsx3

# Barkod okuma fonksiyonu
def barkod_oku():
    cap = cv2.VideoCapture(0)  # Kamera ile barkod tarama
    while True:
        _, frame = cap.read()
        decoded_objects = pyzbar.decode(frame)
        for obj in decoded_objects:
            barcode_data = obj.data.decode("utf-8")
            print(f"Detected Barcode: {barcode_data}")
            cv2.putText(frame, barcode_data, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
            cv2.imshow("Barcode Reader", frame)
            return barcode_data
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

# OCR ile isim okuma fonksiyonu
def isim_oku(resim_yolu):
    img = cv2.imread(resim_yolu)
    text = pytesseract.image_to_string(img)
    print(f"Detected Text: {text}")
    return text

# Sesli okuma fonksiyonu
def sesli_oku(metin):
    engine = pyttsx3.init()
    engine.say(metin)
    engine.runAndWait()

# Ana fonksiyon
def ana_fonksiyon():
    barkod = barkod_oku()
    sesli_oku(f"Barkod okundu: {barkod}")
    
    if "Patoloji Numarası" in barkod:  # Buraya patoloji numarasına özel bir kontrol eklenebilir
        # Enlil sistemi ile bağlantı
        # Bu kısımda barkoddan elde edilen hasta numarasını kullanarak isim okuma işlemi yapılacak
        hasta_no = barkod.split("-")[1]  # Örnek bir ayırma işlemi
        resim_yolu = f"{hasta_no}.jpg"  # Dosya yolunu hasta numarasına göre oluşturma
        isim = isim_oku(resim_yolu)
        sesli_oku(f"Hasta ismi: {isim}")
        
        # Enlil sistemine isim ve hasta numarası gönderme
        # requests.post("http://enlil/pathology/endpoint", data={"hasta_no": hasta_no, "isim": isim})
    else:
        sesli_oku("Bu barkod bir patoloji numarası ile ilişkili değil.")

if __name__ == "__main__":
    ana_fonksiyon()
```

### 2. Gerekli Kütüphanelerin Kurulması:
Kütüphanelerin kurulması için aşağıdaki komutları kullanabilirsiniz:

```bash
pip install opencv-python
pip install pytesseract
pip install pyzbar
pip install pyttsx3
pip install requests
```

### 3. README Dosyası:
Aşağıda, proje için bir README dosyası şablonu bulunmaktadır.

```markdown
# Enlil Patoloji Sistemi Entegrasyonu ile Barkod Okuma ve OCR İsim Okuma

Bu proje, bir barkod tarayıcı ve OCR teknolojisi kullanarak barkod numarasını ve hasta ismini okuyup, Enlil patoloji sistemine gönderen bir Python uygulamasıdır.

## Gerekli Kütüphaneler

Projenin çalışabilmesi için aşağıdaki Python kütüphanelerini kurmanız gerekmektedir:

```bash
pip install opencv-python
pip install pytesseract
pip install pyzbar
pip install pyttsx3
pip install requests
```

## Kullanım

1. `barkodnoenlilisimoku.pyw` dosyasını çalıştırın.
2. Kamera açıldığında, barkodu kameraya tutun.
3. Barkod okunduğunda, eğer barkod bir patoloji numarasına aitse, ilgili resimden OCR teknolojisi ile isim okunur ve sesli olarak okunur.
4. Okunan isim ve barkoddan elde edilen hasta numarası, Enlil patoloji sistemine gönderilebilir.

## Notlar

- OCR işlemi için resmin yolunu belirlerken hasta numarasına göre bir dosya adı kullanılmaktadır. 
- Enlil sistemine veri gönderme kısmı için uygun API endpoint'inizi `requests.post` ile güncellemelisiniz.
- Barkod okuma, pyzbar kütüphanesi kullanılarak gerçekleştirilir.
```
