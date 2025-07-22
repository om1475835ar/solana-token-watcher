import os, time, requests, random
from datetime import datetime
from telegram import Bot
from PIL import Image, ImageDraw, ImageFont

# الإعدادات من متغيرات البيئة
RPC_URL = os.getenv("RPC_URL")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = Bot(TOKEN=TELEGRAM_BOT_TOKEN)

def log(msg):
    print(f"{datetime.now().strftime('%H:%M:%S')} — {msg}")

def scan_tokens():
    # هنا منطق الفلترة التجريبي: توليد عملة افتراضية
    holders = random.randint(500, 2000)
    liquidity = random.randint(5000, 20000)
    twitter = random.randint(800, 2000)
    price = random.uniform(0.001, 1)
    name = f"TOKEN{random.randint(100,999)}"

    return {
        "name": name,
        "holders": holders,
        "liquidity": liquidity,
        "twitter": twitter,
        "price": round(price, 4)
    }

def create_image(token):
    img = Image.new("RGB", (400, 200), color=(30, 30, 30))
    d = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    d.text((10, 10), f"✅ {token['name']}", fill=(0,255,0), font=font)
    d.text((10, 40), f"Holders: {token['holders']}", fill=(255,255,255), font=font)
    d.text((10, 70), f"Liquidity: ${token['liquidity']}", fill=(255,255,255), font=font)
    d.text((10, 100), f"Twitter: {token['twitter']}", fill=(255,255,255), font=font)
    d.text((10, 130), f"Price: ${token['price']}", fill=(255,255,255), font=font)
    path = f"/tmp/{token['name']}.png"
    img.save(path)
    return path

def send_token_alert(token):
    text = (f"💎 Token found:\n"
            f"{token['name']} | Holders: {token['holders']} | Liquidity: ${token['liquidity']} | Twitter: {token['twitter']}")
    img = create_image(token)
    bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=open(img, "rb"), caption=text)

def main():
    log("Bot started!")
    while True:
        token = scan_tokens()
        if token["holders"] >= 800 and token["liquidity"] >= 10000 and token["twitter"] >= 1000:
            log(f"Found token {token['name']}")
            send_token_alert(token)
        time.sleep(1)

if __name__ == "__main__":
    main()
