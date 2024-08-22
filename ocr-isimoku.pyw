import pytesseract
from PIL import ImageGrab
from gtts import gTTS
import os

# OCR için tesseract'ın yolunu belirleyin
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Ekran görüntüsünü fare tıklama koordinatlarına göre al
left, top, right, bottom = 327, 192, 484, 207
screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))

# OCR ile metni okuyun
text = pytesseract.image_to_string(screenshot, lang='tur')

# Metni küçük harfe çevir ve "I" harfini "ı" harfine değiştir
text = text.lower().replace("I", "ı")

# OCR sonucu text dosyasına yaz
with open("ocr_sonucu.txt", "w", encoding="utf-8") as file:
    file.write(text)

# Metni Türkçe olarak sese çevir
tts = gTTS(text=text, lang='tr')
tts.save("ocr_sonucu.mp3")

# Ses dosyasını otomatik olarak çal
os.system("start ocr_sonucu.mp3")
