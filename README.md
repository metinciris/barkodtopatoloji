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
3. Barkod sesli olarak okunur.
4. Barkoddan elde edilen hasta numarası, Enlil patoloji sistemine gönderilebilir.
5. Barkod içinde "/" geçiyorsa hasta numarası olduğunu anlar ve Enlil patoloji penceresini ön plana getirir.
6. Enlil patoloji sisteminde barkoda göre hasta bilgilerini bulur ve hasta ismini sesli okur.

Yukarıdaki dosya yerine, aynı işi gören iki ayrı py dosyası `barkodnoenlilisimoku.py` ve `ocr-isimoku-py` kullanabilirsiniz:
İki ayrı dosya, birbiri ile bağlantılı olarak çalışabilir:
`ocr-isimoku-py` Hasta isminin olduğu alanı spesifik olarak okur. 
X ve Y kısımlarını kendinize göre düzeltebilirsiniz. 
FULLHD ekrana göre tanımlanmıştır.

`barkodnoenlilisimoku.py` barkodu kameradan alır, içinde "/" varsa patoloji numarası olduğunu anlar, Patoloji modülüne geçip ilgili yere yapıştırır ve arar. 
Hasta ismini okumak için `ocr-isimoku-py` dosyayı çalıştırır. 
Kod içinde bu yolu bilgisyardaki dosya yoluna göre düzenleyin.

test2.py Bu kod, barkod olmayan ancak "?????/24" gibi numara ve "/" karakteri içeren yazıları da algılar ve barkod okunmuş gibi işlem yapar. Ayrıca, number_range ve year_suffix değişkenleri sayesinde sayı aralığı ve yıl ekini ileride kolayca değiştirebilirsiniz. Kodda her fonksiyon ve önemli adımlar için açıklamalar eklenmiştir.


## Notlar

- OCR işlemi için resmin yolunu belirlerken hasta numarasına göre bir dosya adı kullanılmaktadır. 
- Enlil sistemine veri gönderme kısmı için uygun API endpoint'inizi `requests.post` ile güncellemelisiniz.
- Barkod okuma, pyzbar kütüphanesi kullanılarak gerçekleştirilir.
- `ocr-isimoku-py` makro içeren fareniz varsa tuşa tanımlayıp hasta ismi kontrolünde ayrıca kullanabilirsiniz.
```
