import cv2
from pyzbar import pyzbar
import pyperclip
import pyautogui
import ctypes
import time
import os
import subprocess  # Dış dosya çalıştırmak için
import numpy as np
import pytesseract  # OCR için
import string
import re
  # bu versiyon ile ayarlanabilir numara yıl aralığı ile etiketten OCR yapılmaktadır. Barkod yoksa uygun etiket okuması ile kod çalışmaktadır.
def play_sound(text):
    """
    Metni sesli olarak okur eğer en az 4 karakter ve '/' içeriyorsa.
    """
    if len(text.strip()) >= 4 and "/" in text:  # Metin 4 karakter ve '/' içeriyorsa
        from gtts import gTTS
        tts = gTTS(text=text, lang='tr')
        tts.save("output.mp3")
        os.system("start output.mp3")

def play_beep():
    """
    Sistem hoparlörü ile bip sesi çalar.
    """
    os.system('cmd /c "echo \a"')

def find_enlil_window():
    """
    'Enlil - Patoloji' penceresinin pencere tanıtıcısını bulur.
    """
    hwnd = ctypes.windll.user32.FindWindowW(None, None)
    while hwnd:
        window_text = ctypes.create_unicode_buffer(512)
        ctypes.windll.user32.GetWindowTextW(hwnd, window_text, 512)
        if "Enlil - Patoloji" in window_text.value:
            return hwnd
        hwnd = ctypes.windll.user32.GetWindow(hwnd, 2)
    return None

def activate_enlil_window():
    """
    'Enlil - Patoloji' penceresini öne getirir ve GUI otomasyonu gerçekleştirir.
    """
    hwnd = find_enlil_window()
    if hwnd:
        ctypes.windll.user32.SetForegroundWindow(hwnd)
        time.sleep(0.8)
        pyautogui.click(211, 109)
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(0.5)
        pyautogui.click(147, 198)
        time.sleep(1)
        pyautogui.doubleClick(147, 198)
        time.sleep(0.5)
        subprocess.Popen(['python', 'C:\\Users\\user\\Documents\\python kodlarım\\ocr-isimoku.pyw'])
        time.sleep(2)
    else:
        print("Enlil penceresi bulunamadı.")
        time.sleep(3)

def decode_barcode(gray_frame, number_range=(15000, 25000), year_suffix='24'):
    """
    Verilen gri tonlamalı kareden barkodları çözer.
    Barkod bulunamazsa, belirli bir desene uyan metni bulmak için OCR yapar.

    Parametreler:
    - gray_frame: Gri tonlamalı görüntü karesi.
    - number_range: OCR'da aramak için sayı aralığı (örn: (15000, 25000)).
    - year_suffix: OCR'da aramak için yıl eki (örn: '24').

    Dönüş:
    - Barkod veya eşleşen metin bulunursa döndürür, aksi halde None.
    """
    # Kontrastı artırmak için histogram eşitleme
    gray_frame = cv2.equalizeHist(gray_frame)
    
    # Döndürme açıları (derece cinsinden)
    angles = [-10, -5, 0, 5, 10]
    
    for angle in angles:
        # Görüntüyü belirli bir açıyla döndür
        rotated = rotate_image(gray_frame, angle)
        # Barkodları tara
        barcodes = pyzbar.decode(rotated)
        for barcode in barcodes:
            barcode_data = barcode.data.decode("utf-8")
            if len(barcode_data) >= 4 and "/" in barcode_data:
                barcode_data = barcode_data.replace("/", "taksim")
                play_beep()
                play_sound(barcode_data)
                pyperclip.copy(barcode_data.replace("taksim", "/"))
                activate_enlil_window()
                return barcode_data
    
    # Barkod bulunamazsa, OCR yap
    ocr_text = perform_ocr(gray_frame, number_range, year_suffix)
    # OCR metni desene uyuyor mu kontrol et
    if ocr_text:
        # OCR metnini barkod gibi işle
        play_beep()
        play_sound(ocr_text)
        pyperclip.copy(ocr_text)
        activate_enlil_window()
        return ocr_text

    return None  # Barkod veya eşleşen metin bulunamadı

def perform_ocr(gray_frame, number_range=(15000, 25000), year_suffix='24'):
    """
    Verilen gri tonlamalı karede OCR yapar ve şu desene uyan metni arar:
    Belirtilen aralıkta bir sayı, ardından '/' ve belirtilen yıl eki.

    Parametreler:
    - gray_frame: Gri tonlamalı görüntü karesi.
    - number_range: Aranacak sayı aralığı (örn: (15000, 25000)).
    - year_suffix: Aranacak yıl eki (örn: '24').

    Dönüş:
    - Eşleşen metin bulunursa döndürür, aksi halde None.
    """
    # Pytesseract ile OCR yap
    ocr_result = pytesseract.image_to_string(gray_frame, lang='eng', config='--psm 6')
    # Yazdırılabilir karakterler dışındakileri kaldır
    ocr_result = ''.join(filter(lambda x: x in string.printable, ocr_result))
    # OCR sonucunda desenleri ara
    # Örnek desen: '12345/24'
    pattern = r'\b(\d+)/{year_suffix}\b'.format(year_suffix=year_suffix)
    matches = re.findall(pattern, ocr_result)
    for match in matches:
        # Sayı kısmını tamsayıya çevir ve istenen aralıkta mı kontrol et
        try:
            num = int(match)
            if number_range[0] <= num <= number_range[1]:
                # Eşleşen metni döndür
                return f"{num}/{year_suffix}"
        except ValueError:
            continue
    return None  # Eşleşen metin bulunamadı

def rotate_image(image, angle):
    """
    Görüntüyü verilen açıyla döndürür.

    Parametreler:
    - image: Döndürülecek görüntü.
    - angle: Görüntünün döndürüleceği açı (derece cinsinden).

    Dönüş:
    - Döndürülmüş görüntü.
    """
    # Görüntünün merkezini bul
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    # Rotasyon matrisi oluştur
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    # Görüntüyü döndür
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_LINEAR)
    return rotated

def main():
    global cap
    cap = cv2.VideoCapture(1)  # Kamera 1 otomatik olarak açılıyor
    if not cap.isOpened():
        print("Hata: Kamera 1 açılamadı.")
        return

    # Çözünürlüğü 640x480 olarak ayarla
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    # Ayarlanabilir sayı aralığı ve yıl eki
    number_range = (15000, 25000)
    year_suffix = '24'

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Kameradan görüntü alınamadı.")
            break

        # Görüntüyü 180 derece döndür
        frame = cv2.rotate(frame, cv2.ROTATE_180)

        # Gri tonlamalı görüntüye dönüştür
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Barkodu çöz veya OCR yap
        barcode_data = decode_barcode(gray, number_range, year_suffix)

        # Gri görüntüyü göster
        cv2.imshow('Camera', gray)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
