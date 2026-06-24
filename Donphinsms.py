import requests
import re
import time
import json
from datetime import datetime

# ============================================================
# 🔧 কনফিগারেশন
# ============================================================
API_URL = "http://51.83.6.7:20040/dolphin"
API_TOKEN = "aace31b6898a4f078a3134f1062d96bdb88ab526ed1952e16eb04df4019193ef"
BOT_TOKEN = "5929619535:AAGsgoN5pYczsKWOGqVWTrslk0qJr2jJVYA"
CHAT_ID = "-1001153782407"

NUMBER_BOT = "https://t.me/Updateotpnew_bot"
MAIN_CHANNEL = "https://t.me/updaterange"

# ============================================================
# 📌 শর্ট নাম (সার্ভিস অনুযায়ী)
# ============================================================
SERVICE_NAMES = {
    "whatsapp": "WA",
    "telegram": "TG",
    "facebook": "FB",
    "messenger": "MSG",
    "imessage": "IM",
    "signal": "SG",
    "viber": "VB",
    "line": "LN",
    "wechat": "WC",
    "instagram": "IG",
    "twitter": "TW",
    "tiktok": "TK",
    "snapchat": "SC",
    "linkedin": "LI",
    "youtube": "YT",
    "reddit": "RD",
    "bank": "BNK",
    "bkash": "BK",
    "nagad": "NG",
    "rocket": "RK",
    "paypal": "PP",
    "stripe": "ST",
    "google pay": "GP",
    "apple pay": "AP",
    "google": "GO",
    "amazon": "AM",
    "apple": "AP",
    "microsoft": "MS",
    "uber": "UB",
    "airbnb": "AB",
    "spotify": "SP",
    "netflix": "NF",
    "bolt": "BLT",
}

def get_service_short_name(sender):
    if not sender:
        return "OTP"
    sender_lower = sender.lower()
    for key, short in SERVICE_NAMES.items():
        if key in sender_lower:
            return short
    if len(sender) <= 3:
        return sender.upper()
    return f"{sender[:2]}{sender[-1]}".upper()

# ============================================================
# 🌍 কান্ট্রি ফ্লাগ
# ============================================================
COUNTRY_DATA = {
    "880": "🇧🇩",
    "91": "🇮🇳",
    "92": "🇵🇰",
    "94": "🇱🇰",
    "977": "🇳🇵",
    "93": "🇦🇫",
    "95": "🇲🇲",
    "856": "🇱🇦",
    "855": "🇰🇭",
    "84": "🇻🇳",
    "60": "🇲🇾",
    "65": "🇸🇬",
    "62": "🇮🇩",
    "63": "🇵🇭",
    "66": "🇹🇭",
    "1": "🇺🇸",
    "44": "🇬🇧",
    "61": "🇦🇺",
    "81": "🇯🇵",
    "82": "🇰🇷",
    "86": "🇨🇳",
    "49": "🇩🇪",
    "33": "🇫🇷",
    "39": "🇮🇹",
    "34": "🇪🇸",
    "7": "🇷🇺",
    "55": "🇧🇷",
    "52": "🇲🇽",
    "966": "🇸🇦",
    "971": "🇦🇪",
    "965": "🇰🇼",
    "20": "🇪🇬",
    "27": "🇿🇦",
    "234": "🇳🇬",
    "254": "🇰🇪",
    "263": "🇿🇼",
}

def get_country_flag(phone_number):
    if not phone_number:
        return "🌍"
    digits = re.sub(r'\D', '', str(phone_number))
    for code in sorted(COUNTRY_DATA.keys(), key=len, reverse=True):
        if digits.startswith(code):
            return COUNTRY_DATA[code]
    return "🌍"

# ============================================================
# 📡 API ফাংশন
# ============================================================
def fetch_sms(limit=50):
    url = f"{API_URL}?token={API_TOKEN}"
    try:
        resp = requests.get(url, timeout=15)
        
        if resp.status_code != 200:
            print(f"❌ HTTP Error: {resp.status_code}")
            return []
        
        if not resp.text or resp.text.strip() == "":
            print("❌ খালি রেসপন্স")
            return []
        
        try:
            data = resp.json()
        except json.JSONDecodeError:
            print(f"❌ JSON Parse Error")
            return []
        
        if isinstance(data, list):
            print(f"✅ API থেকে {len(data)}টি রেকর্ড পাওয়া গেছে")
            return data
        else:
            print(f"❌ অজানা ফরম্যাট")
            return []
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

# ============================================================
# 🔍 OTP এক্সট্র্যাক্ট
# ============================================================
def extract_otp(text):
    if not text:
        return None
    patterns = [
        r'\b(\d{4,8})\b',
        r'OTP[:\s]*(\d{4,8})',
        r'code[:\s]*(\d{4,8})',
        r'পিন[:\s]*(\d{4,8})',
        r'verification[:\s]*(\d{4,8})',
        r'your code[:\s]*(\d{4,8})',
        r'সাইন[:\s]*(\d{4,8})',
        r'verification code[:\s]*(\d{4,8})',
        r'পাসওয়ার্ড[:\s]*(\d{4,8})',
        r'is[:\s]*(\d{4,8})',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    return None

# ============================================================
# 📝 মেসেজ ফরম্যাট (পুরো নম্বর সহ)
# ============================================================
def format_otp_message(sms):
    """
    ডলফিন API ফরম্যাট: [Sender, Number, Message, Time]
    """
    if not isinstance(sms, list) or len(sms) < 4:
        return None
    
    sender = sms[0] if sms[0] else "UNKNOWN"
    number = sms[1] if sms[1] else ""
    text = sms[2] if sms[2] else ""
    time_str = sms[3] if len(sms) > 3 else ""
    
    otp = extract_otp(text)
    if not otp:
        return None
    
    service = get_service_short_name(sender)
    flag = get_country_flag(number)
    
    # 🔥 পরিবর্তন: পুরো নম্বর দেখাচ্ছে
    message = f"{flag} {service} 💚 {number}"
    
    keyboard = {
        "inline_keyboard": [
            [{"text": f"📋 {otp} (কপি)", "copy_text": {"text": otp}}],
            [
                {"text": "🔢 Number Bot", "url": NUMBER_BOT},
                {"text": "📢 Main Channel", "url": MAIN_CHANNEL}
            ]
        ]
    }
    return message, keyboard

# ============================================================
# 📨 টেলিগ্রামে পাঠানো
# ============================================================
def send_telegram_message(message, keyboard=None):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        if keyboard:
            payload["reply_markup"] = keyboard
        
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code == 200:
            print(f"✅ {message}")
            return True
        else:
            print(f"❌ Telegram Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Send Error: {e}")
        return False

# ============================================================
# 🚀 স্টার্ট মেসেজ
# ============================================================
def send_start_message():
    message = "✅ বট সফলভাবে রান হয়েছে (ডলফিন API)"
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "🔢 Number Bot", "url": NUMBER_BOT},
                {"text": "📢 Main Channel", "url": MAIN_CHANNEL}
            ]
        ]
    }
    send_telegram_message(message, keyboard)

# ============================================================
# 🔄 মেইন লজিক
# ============================================================
sent_ids = set()

def send_todays_otp():
    global sent_ids
    print("📋 আজকের OTP সংগ্রহ করা হচ্ছে...")
    
    sms_list = fetch_sms()
    if not sms_list:
        print("📭 কোনো OTP পাওয়া যায়নি")
        return
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    todays_sms = []
    for sms in sms_list:
        if isinstance(sms, list) and len(sms) >= 4:
            sms_time = sms[3] if sms[3] else ""
            if today in sms_time:
                todays_sms.append(sms)
    
    if not todays_sms:
        print(f"📭 আজকের ({today}) কোনো OTP নেই")
        return
    
    print(f"📋 মোট {len(todays_sms)}টি OTP পাওয়া গেছে (আজকের)")
    todays_sms.reverse()
    
    sent_count = 0
    for sms in todays_sms[:20]:
        result = format_otp_message(sms)
        if result:
            message, keyboard = result
            if send_telegram_message(message, keyboard):
                sms_id = f"{sms[1]}_{sms[2][:20]}"
                sent_ids.add(sms_id)
                sent_count += 1
                time.sleep(0.5)
    
    print(f"📨 আজকের মোট {sent_count}টি OTP ফরওয়ার্ড করা হয়েছে")
    time.sleep(2)

def process_and_forward():
    global sent_ids
    
    sms_list = fetch_sms()
    if not sms_list:
        return
    
    sms_list.reverse()
    
    sent_count = 0
    for sms in sms_list[:10]:
        if not isinstance(sms, list) or len(sms) < 4:
            continue
        
        sms_id = f"{sms[1]}_{sms[2][:20]}"
        if sms_id in sent_ids:
            continue
        
        result = format_otp_message(sms)
        if result:
            message, keyboard = result
            if send_telegram_message(message, keyboard):
                sent_ids.add(sms_id)
                sent_count += 1
                time.sleep(0.5)
    
    if sent_count > 0:
        print(f"📨 মোট {sent_count}টি নতুন OTP পাঠানো হয়েছে")
    
    if len(sent_ids) > 1000:
        sent_ids = set(list(sent_ids)[-500:])

# ============================================================
# 🔥 বট রান
# ============================================================
if __name__ == "__main__":
    print("🚀 বট চালু হচ্ছে (ডলফিন API)...")
    print(f"📡 API URL: {API_URL}")
    
    send_start_message()
    print("✅ 'বট সফলভাবে রান হয়েছে' মেসেজ গ্রুপে পাঠানো হয়েছে!")
    
    print("⏳ আজকের OTP চেক করা হচ্ছে...")
    send_todays_otp()
    
    print("⏳ নতুন OTP মনিটরিং শুরু হচ্ছে (প্রতি ২ সেকেন্ডে)...")
    print("🛑 বন্ধ করতে Ctrl+C প্রেস করুন")
    
    while True:
        process_and_forward()
        time.sleep(2)