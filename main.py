import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Telegram bot ma'lumotlari
TOKEN = "*********"

# Bir nechta Chat ID'larni shu yerga kiritasiz (vergul bilan ajratib)
CHAT_IDS = ["BIRINCHI_ODAMNING_CHAT_ID_SI", "IKKINCHI_ODAMNING_CHAT_ID_SI"]

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    for chat_id in CHAT_IDS:
        payload = {
            "chat_id": chat_id,
            "text": message
        }
        try:
            requests.post(url, json=payload)
        except Exception as e:
            print(f"Xabar yuborishda xatolik ({chat_id}):", e)

# Chrome profilini ulash (Ishga tushirishdan oldin barcha Chrome oynalarini yoping!)
options = Options()
options.add_argument(r"user-data-dir=C:\Users\bosiy\AppData\Local\Google\Chrome\User Data")
options.add_argument("profile-directory=Default")

try:
    driver = webdriver.Chrome(options=options)
except Exception as e:
    print("Xatolik: Kompyuterdagi barcha Chrome oynalarini yoping va qayta urinib ko'ring!")
    exit()

# TLScontact sahifasiga o'tish
driver.get("https://visas-de.tlscontact.com/workflow/appointment-booking/uzTAS2de/4901522")

input("Ochilgan brauzerda akkauntingizga kirib, kalendar sahifasiga o'tgach, PyCharm konsoliga o'tib Enter tugmasini bosing...")

while True:
    try:
        driver.refresh()
        time.sleep(7)  # Sahifa yuklanishini kutish

        page_text = driver.find_element(By.TAG_NAME, "body").text

        if len(page_text) < 200:
            print("Sahifa hali to'liq yuklanmadi, kutilmoqda...")
            continue

        # Soxta xabarlarning oldini olish uchun tekshiruv
        if "Hozircha bizda uchrashuv uchun joylar mavjud emas" not in page_text:
            time.sleep(3)
            page_text_retry = driver.find_element(By.TAG_NAME, "body").text

            if "Hozircha bizda uchrashuv uchun joylar mavjud emas" not in page_text_retry and len(page_text_retry) > 200:
                print("DIQQAT! Haqiqatan ham bo'sh joy paydo bo'ldi!")
                send_telegram_message("🚨 Diqqat! TLScontact da Germaniya vizasi uchun bo'sh slot chiqdi!")
                break
            else:
                print("Vaqtincha yuklanish xatosi, qidirish davom etmoqda...")
        else:
            print("Hozircha bo'sh joy yo'q, tekshirilmoqda...")

    except Exception as e:
        print("Xatolik yuz berdi:", e)
        time.sleep(5)