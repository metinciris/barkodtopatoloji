import cv2
from pyzbar import pyzbar
import pyperclip
import pyautogui
import ctypes
import time
import os
import subprocess  # Dış dosya çalıştırmak için

def play_sound(text):
    if text.strip():  # Metin boş değilse okut
        from gtts import gTTS
        tts = gTTS(text=text, lang='tr')
        tts.save("output.mp3")
        os.system("start output.mp3")

def play_beep():
    os.system('cmd /c "echo \a"')

def find_enlil_window():
    hwnd = ctypes.windll.user32.FindWindowW(None, None)
    while hwnd:
        window_text = ctypes.create_unicode_buffer(512)
        ctypes.windll.user32.GetWindowTextW(hwnd, window_text, 512)
        if "Enlil - Patoloji" in window_text.value:
            return hwnd
        hwnd = ctypes.windll.user32.GetWindow(hwnd, 2)
    return None

def activate_enlil_window():
    hwnd = find_enlil_window()
    if hwnd:
        ctypes.windll.user32.SetForegroundWindow(hwnd)
        # Tam ekranı bozmadan pencereyi ön plana getiriyoruz.
        time.sleep(0.8)
        # Tıklama ve metin yapıştırma işlemleri
        pyautogui.click(211, 109)
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(0.5)
        pyautogui.click(147, 198)
        time.sleep(1)  # Çift tıklama arasında 1 saniye bekleme süresi
        pyautogui.doubleClick(147, 198)
        time.sleep(0.5)
        # OCR işlemi için dış dosya çalıştırma
        subprocess.Popen(['python', 'C:\\Users\\user\\Documents\\python kodlarım\\ocr-isimoku.pyw'])
        time.sleep(2)
    else:
        print("Enlil penceresi bulunamadı.")
        time.sleep(3)

def decode_barcode(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    barcodes = pyzbar.decode(gray)
    for barcode in barcodes:
        barcode_data = barcode.data.decode("utf-8")
        if "/" in barcode_data:
            barcode_data = barcode_data.replace("/", "taksim")
        play_beep()
        play_sound(barcode_data)
        if "taksim" in barcode_data:
            pyperclip.copy(barcode_data.replace("taksim", "/"))
            activate_enlil_window()
        return barcode_data

def main():
    global cap
    cap = cv2.VideoCapture(1)  # Kamera 1 otomatik olarak açılıyor
    if not cap.isOpened():
        print("Error: Could not open camera 1.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Kameradan görüntü alınamadı.")
            break
        cv2.imshow('Camera', frame)
        barcode_data = decode_barcode(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
