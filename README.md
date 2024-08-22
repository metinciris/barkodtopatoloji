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

1. `test.py` dosyasını çalıştırın.
2. Kamera açıldığında, barkodu kameraya tutun.
3. Barkod okunduğunda, eğer barkod bir patoloji numarasına aitse, ilgili resimden OCR teknolojisi ile isim okunur ve sesli olarak okunur.
4. Okunan isim ve barkoddan elde edilen hasta numarası, Enlil patoloji sistemine gönderilebilir.

İki ayrı dosya, birbiri ile bağlantılı olarak çalışabilir:
`ocr-isimoku-py` Hasta isminin olduğu alanı spesifik olarak okur. 
X ve Y kısımlarını kendinize göre düzeltebilirsiniz. 
FULLHD ekrana göre tanımlanmıştır.

`barkodnoenlilisimoku.py` barkodu kameradan alır, içinde "/" varsa patoloji numarası olduğunu anlar, Patoloji modülüne geçip ilgili yere yapıştırır ve arar. 
Hasta ismini okumak için üstteki dosyayı çalıştırır. 
Kod içinde bu yolu bilgisyardaki dosya yoluna göre düzenleyin.


## Notlar

- OCR işlemi için resmin yolunu belirlerken hasta numarasına göre bir dosya adı kullanılmaktadır. 
- Enlil sistemine veri gönderme kısmı için uygun API endpoint'inizi `requests.post` ile güncellemelisiniz.
- Barkod okuma, pyzbar kütüphanesi kullanılarak gerçekleştirilir.
```
