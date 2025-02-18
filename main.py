import telebot
from telebot import types
import sqlite3
import os
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telegram import WebAppInfo

# Global o'zgaruvchini aniqlash
active_chats = {}

# Bot tokeni
TOKEN = "7083428384:AAFrgLeJ4qEIu3ugtRnKcf2fWIjv1Yav97k"
bot = telebot.TeleBot(TOKEN)

# SQLite3 bazasi bilan ulanish va jadval yaratish
db_path = 'users.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path, check_same_thread=False)
else:
    conn = sqlite3.connect(db_path, check_same_thread=False)

cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        chat_id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        username TEXT,
        city TEXT
    )
''')
conn.commit()

# /start buyrug'iga javob berish uchun funksiya
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id    
    markup = InlineKeyboardMarkup()
    image_url = 'https://namozvaqti.uz/img/logo_new.png'
    
    # Rasmni yuborish
    bot.send_photo(chat_id, image_url)      
    
    # Web app URL va tugma
    web_app_url = 'https://namoz-vaqtlari-islomuz.netlify.app'   
    web_app_button = InlineKeyboardButton("🕌Namoz vaqtlari🕌", web_app=WebAppInfo(url=web_app_url))
    markup.add(web_app_button)
    
    # Foydalanuvchi ma'lumotlarini olish
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name or "Familiya mavjud emas"
    username = message.from_user.username or "Username mavjud emas"
    
    # Xabarni yuborish
    welcome_message = f"Assalomu alaykum, {first_name} {last_name}!\n" \
                      f"Username: @{username}"
    
    bot.send_message(chat_id, welcome_message, reply_markup=markup)


    # Foydalanuvchi ma'lumotlarini bazaga saqlash
    cursor.execute('SELECT * FROM users WHERE chat_id = ?', (chat_id,))
    result = cursor.fetchone()

    if result is None:
        # Foydalanuvchini bazaga qo'shish
        cursor.execute('INSERT INTO users (chat_id, first_name, last_name, username) VALUES (?, ?, ?, ?)', 
                       (chat_id, first_name, last_name, username))
        conn.commit()
        bot.send_message(chat_id, f"Salom, {first_name}! Shaharlardan birini tanlang:", reply_markup=create_inline_keyboard())
    else:
        bot.send_message(chat_id, f"Salom, {first_name}! Siz allaqachon ro'yxatdan o'tgansiz. Profilingizni ko'rish uchun\n👉/profil👈buyrug'idan foydalaning.")

# Inline tugma bosilganda ishlaydigan funksiya
@bot.callback_query_handler(func=lambda call: call.data in ["Toshkent","Angren","Andijon","Arnasoy","Ashxabod","Bekobod","Bishkek","Boysun","Buloqboshi","Burchmulla","Buxoro","Gazli","Guliston","Denov","Dehqonobod","Do'stlik","Dushanbe","Jalolobod","Jambul","Jizzax","Jomboy","Zarafshon","Zomin","Kattaqurg'on","Konibodom","Konimex","Koson","Kosonsoy","Marg'ilon","Mingbuloq","Muborak","Mo'ynoq","Navoiy","Namangan","Nukus","Nurota","Olmaota","Olot","Oltiariq","Oltinqo'l","Paxtabod","Pop","Rishton","Sayram","Samarqand","Tallimarjon","Taxtako'pir","Termiz","Tomdi","Toshhovuz","Turkiston","Turkmanobod","To'rtko'l","Uzunquduq","Urganch","Urgut","O'smat","Uchtepa","Uchquduq","Uchqo'rg'on","O'sh","O'gi'z","Farg'ona","Xazorasp","Xiva","Xonobod","Xonqa","Xo'jand","Xo'jaobod","Chimboy","Chimkent","Chortoq","Chust","Shahrijon","Sherobod","Shovot","Shumanay","Yangibozor","G'azalkent","G'allaorol","G'uzor","Qarshi","Qiziltepa","Qoravo'l","Qoravulbozor",
"Quva","Qumqo'rg'on","Qo'ng'irot","Qo'rg'ontepa","Qo'qon"
])

#bazaga saqlangan shaharni olish
def handle_city_selection(call):
    chat_id = call.message.chat.id
    city = call.data

    # Tanlangan shaharni yangilash
    cursor.execute('UPDATE users SET city = ? WHERE chat_id = ?', (city, chat_id))
    conn.commit()

    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, f"{city} viloyati tanlandi. Profilingizni ko'rish uchun\n👉/profil👈 tugmasidan foydalaning.", reply_markup=main_keyboard())

# Viloyatni tanlash uchun tugmalar yaratish
def create_inline_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    cities = ["Toshkent","Angren","Andijon","Arnasoy","Ashxabod","Bekobod","Bishkek","Boysun","Buloqboshi","Burchmulla","Buxoro","Gazli","Guliston","Denov","Dehqonobod","Do'stlik","Dushanbe","Jalolobod","Jambul","Jizzax","Jomboy","Zarafshon","Zomin","Kattaqurg'on","Konibodom","Konimex","Koson","Kosonsoy","Marg'ilon","Mingbuloq","Muborak","Mo'ynoq","Navoiy","Namangan","Nukus","Nurota","Olmaota","Olot","Oltiariq","Oltinqo'l","Paxtabod","Pop","Rishton","Sayram","Samarqand","Tallimarjon","Taxtako'pir","Termiz","Tomdi","Toshhovuz","Turkiston","Turkmanobod","To'rtko'l","Uzunquduq","Urganch","Urgut","O'smat","Uchtepa","Uchquduq","Uchqo'rg'on","O'sh","O'gi'z","Farg'ona","Xazorasp","Xiva","Xonobod","Xonqa","Xo'jand","Xo'jaobod","Chimboy","Chimkent","Chortoq","Chust","Shahrijon","Sherobod","Shovot","Shumanay","Yangibozor","G'azalkent","G'allaorol","G'uzor","Qarshi","Qiziltepa","Qoravo'l","Qoravulbozor",
    "Quva","Qumqo'rg'on","Qo'ng'irot","Qo'rg'ontepa","Qo'qon"
]
    buttons = [types.InlineKeyboardButton(text=city, callback_data=city) for city in cities]
    keyboard.add(*buttons)
    return keyboard

# /profil buyrug'iga javob berish uchun funksiya
@bot.message_handler(commands=['miniapp'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    web_app_url = 'https://islom.uz/lotin'   
    web_app_button = InlineKeyboardButton("Islom.uz sayti🕌", web_app=WebAppInfo(url=web_app_url))
    markup.add(web_app_button)
    bot.send_message(message.chat.id, "Assalomu alaykum.", reply_markup=markup)

@bot.message_handler(commands=['profil'])
@bot.message_handler(func=lambda message: message.text == "Profil")
def show_profile(message):
    chat_id = message.chat.id
    cursor.execute('SELECT first_name, last_name, username, city FROM users WHERE chat_id = ?', (chat_id,))
    result = cursor.fetchone()
    
    if result:
        first_name, last_name, username, city = result
        profile_text = (
            f"👤 Profil Ma'lumotlari:\n\n"
            f"👤 Ism: {first_name}\n"
            f"👤 Familiya: {last_name}\n"
            f"📧 Username: {username}\n"
            f"🆔 Chat ID: {chat_id}\n"
            f"🏙 Shahar: {city or 'Tanlanmagan'}\n"
        )
        bot.send_message(chat_id, profile_text, reply_markup=edit_city_button())
    else:
        bot.send_message(chat_id, "Profil ma'lumotlari topilmadi. Iltimos,\n👉/start👈buyrug'idan foydalanib qayta ro'yxatdan o'ting.")

def main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Profil"), types.KeyboardButton("Namoz Vaqtlari"))
    keyboard.add(types.KeyboardButton("Info"), types.KeyboardButton("Ehson"))
    keyboard.add(types.KeyboardButton("Admin bilan aloqa"))
    return keyboard

# Shaharni tahrirlash va chiqish uchun inline tugmalar yaratish
def edit_city_button():
    keyboard = types.InlineKeyboardMarkup()
    edit_button = types.InlineKeyboardButton(text="🏙 Shaharni tahrirlash", callback_data="edit_city")
    exit_button = types.InlineKeyboardButton(text="🚪 Chiqish", callback_data="exit")
    keyboard.add(edit_button, exit_button)
    return keyboard

# Shaharni qayta tanlash uchun inline tugma bosilganda ishlaydigan funksiya
@bot.callback_query_handler(func=lambda call: call.data == "edit_city")
def edit_city(call):
    chat_id = call.message.chat.id
    bot.send_message(chat_id, "Iltimos, yangi shaharni tanlang:", reply_markup=create_inline_keyboard())

# Chiqish tugmasi bosilganda foydalanuvchi ma'lumotlarini o'chirish
@bot.callback_query_handler(func=lambda call: call.data == "exit")
def exit_handler(call):
    chat_id = call.message.chat.id
    cursor.execute('DELETE FROM users WHERE chat_id = ?', (chat_id,))
    conn.commit()
    bot.send_message(chat_id, "Siz muvaffaqiyatli chiqdingiz. Ma'lumotlaringiz o'chirildi.")

# Namoz Vaqtlari tugmasi bosilganda ishlaydigan funksiya
@bot.message_handler(func=lambda message: message.text == "Namoz Vaqtlari")
def handle_namaz(message):
    chat_id = message.chat.id
    cursor.execute('SELECT city FROM users WHERE chat_id = ?', (chat_id,))
    result = cursor.fetchone()

    if result:
        city = result[0]
        bot.send_message(chat_id, f"{city} viloyati uchun namoz vaqtlari variantlarini tanlang:", reply_markup=create_variant_keyboard(city))
    else:
        bot.send_message(chat_id, "Iltimos, avval shaharni tanlang.")

# Variantlarni tanlash uchun tugmani yaratish
def create_variant_keyboard(city):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton(text="Bugungi taqvim", callback_data=f"today_{city}"),
        types.InlineKeyboardButton(text="Haftalik taqvim", callback_data=f"weekly_{city}")
    ]
    keyboard.add(*buttons)
    return keyboard

# Inline variant tugmasi bosilganda ishlaydigan funksiya
@bot.callback_query_handler(func=lambda call: call.data.startswith(("today_", "weekly_")))
def handle_variant_selection(call):
    try:
        chat_id = call.message.chat.id
        variant, city = call.data.split("_")
        if variant == "today":
            send_today_calendar(chat_id, city)
        elif variant == "weekly":
            send_weekly_calendar(chat_id, city)
    except Exception as e:
        bot.reply_to(call.message, f"Xatolik yuzaga keldi: {e}")

import requests

# Bugungi taqvimni olish
def send_today_calendar(chat_id, city):
    try:
        url = f"https://islomapi.uz/api/present/day?region={city}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if "times" in data:
                times = data["times"]
                response_message = f"Bugungi namoz vaqtlari ({city} uchun):\n"
                
                # O'zgartirilgan nomlar
                names = {
                    "tong_saharlik": "Bomdod",
                    "quyosh": "Quyosh",
                    "peshin": "Peshin",
                    "asr": "Asr",
                    "shom_iftor": "Shom",
                    "hufton": "Xufton"
                }
                
                for time, value in times.items():
                    if time in names:
                        response_message += f"{names[time]}: {value}\n"
                
                # Rasm URL manzili
                photo_url = "https://namozvaqti.uz/img/logo_new.png"
                
                # Xabar va rasmni kanalga yuborish
                bot.send_photo(chat_id, photo_url, caption=response_message)
            else:
                bot.send_message(chat_id, "Namoz vaqtlari topilmadi.")
        else:
            bot.send_message(chat_id, "Namoz vaqtini olishda xato yuz berdi.")
    except Exception as e:
        bot.send_message(chat_id, f"Xatolik yuzaga keldi: {e}")

# Haftalik taqvimni olish
def send_weekly_calendar(chat_id, city):
    try:
        url = f"https://islomapi.uz/api/present/week?region={city}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                response_message = f"Haftalik namoz vaqtlari ({city} uchun):\n"
                
                # Haftaning kunlari
                weekdays = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"]
                
                for index, day in enumerate(data):
                    date = day["date"].split(",")[0]
                    times = day["times"]
                    weekday = weekdays[index]  # Fetch the correct weekday name
                    response_message += f"\n{weekday} ({date}):\n"
                    
                    names = {
                        "tong_saharlik": "Bomdod",
                        "quyosh": "Quyosh",
                        "peshin": "Peshin",
                        "asr": "Asr",
                        "shom_iftor": "Shom",
                        "hufton": "Xufton"
                    }
                    
                    for time, value in times.items():
                        if time in names:
                            response_message += f"{names[time]}: {value}\n"

                # Rasm URL manzili
                photo_url = "https://namozvaqti.uz/img/logo_new.png"
                
                # Xabar va rasmni kanalga yuborish
                bot.send_photo(chat_id, photo_url, caption=response_message)
            else:
                bot.send_message(chat_id, "Haftalik namoz vaqtlari topilmadi.")
        else:
            bot.send_message(chat_id, "Namoz vaqtini olishda xato yuz berdi.")
    except Exception as e:
        bot.send_message(chat_id, f"Xatolik yuzaga keldi: {e}")



# Info tugmasi bosilganda ishlaydigan funksiya
@bot.message_handler(func=lambda message: message.text == "Info")
def show_info(message):
    info_message = (
        "📱 Bu bot, namoz vaqtlarini olish va foydalanuvchilarning profil ma'lumotlarini boshqarish uchun mo'ljallangan.\n\n"
        "👨‍💻 Mening muallifim - [Ibrohimov Izzatbek]\n"
        "Telegram: @izzatbek_ibrohimov\n"
        "(tel: +998919796959).\n"
        "🔗 Ushbu botdan foydalanish orqali siz turli shaharlar uchun namoz vaqtlarini ko'rishingiz mumkin."
    )
    bot.send_message(message.chat.id, info_message)

# Ehson tugmasi bosilganda ishlaydigan funksiya
@bot.message_handler(func=lambda message: message.text == "Ehson")
def handle_ehson(message):
    ehson_message = (
        "Ehsoningiz uchun rahmat! Siz quyidagi hisob raqamlariga ehson qilishingiz mumkin:\n"
        "1. uzcard:**** **** **** ****\n"
        "2. xumo: **** **** **** ****\n\n"
        "Sizga yordam kerakmi? Yana boshqa ma'lumotlarga ehtiyoj bormi?\n \nAdmin bilan aloqa tugmani bosing."
    )
    bot.send_message(message.chat.id, ehson_message)

# Help buyrug'iga javob berish uchun funksiya
@bot.message_handler(commands=['help'])
def show_help(message):
    help_message = (
        "🔍 Ushbu botdan foydalanish uchun:\n"
        "1. /start - Botni ishga tushirish va shaharni tanlash.\n"
        "2. /profil - O'z profil ma'lumotlaringizni ko'rish.\n"
        "3. Namoz Vaqtlari - Bugungi va haftalik namoz vaqtlari bilan tanishish.\n"
        "4. Info - Bot haqida ma'lumot olish.\n"
        "5. Ehson - Ehson qilish uchun raqamlarni ko'rish.\n"
        "6. /help - Botni qanday ishlatishni bilib olish.\n"
        "7. Admin bilan aloqa - Admin bilan aloqa o'rnatish.\n"
    )
    bot.send_message(message.chat.id, help_message)


# Admin chat ID
ADMIN_CHAT_ID = 6870812534
active_contacts = {}

# Admin bilan aloqa tugmasi bosilganda ishlaydigan funksiya
@bot.message_handler(func=lambda message: message.text == "Admin bilan aloqa")
def contact_admin(message):
    chat_id = message.chat.id
    cursor.execute('SELECT first_name, last_name, username, city FROM users WHERE chat_id = ?', (chat_id,))
    user_data = cursor.fetchone()

    if user_data:
        first_name, last_name, username, city = user_data
        profile_info = (
            f"Yangi aloqa so'rovi:\n"
            f"Ism: {first_name}\n"
            f"Familiya: {last_name}\n"
            f"Username: @{username}\n"
            f"Shahar: {city}\n"
            f"Chat ID: {chat_id}"
        )
        keyboard = types.InlineKeyboardMarkup()
        contact_button = types.InlineKeyboardButton(text="Aloqa o'rnatish", callback_data=f"start_contact_{chat_id}")
        reject_button = types.InlineKeyboardButton(text="Aloqani rad etish", callback_data=f"reject_contact_{chat_id}")
        keyboard.add(contact_button, reject_button)

        bot.send_message(ADMIN_CHAT_ID, profile_info, reply_markup=keyboard)
        bot.send_message(chat_id, "Adminga murojaatingiz yuborildi. Iltimos, javobni kuting.")
    else:
        bot.send_message(chat_id, "Profil ma'lumotlaringiz topilmadi. Iltimos, qaytadan urinib ko'ring.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("start_contact_"))
def start_contact(call):
    user_chat_id = call.data.split("_")[-1]
    active_contacts[user_chat_id] = call.message.chat.id
    bot.send_message(user_chat_id, "Siz admin bilan bog'landingiz.")
    bot.send_message(call.message.chat.id, "Aloqa o'rnatildi.")

    # Aloqani to'xtatish tugmalarini yuborish
    send_contact_stop_buttons(user_chat_id, ADMIN_CHAT_ID)

# Aloqani to'xtatish uchun inline tugmalar
def send_contact_stop_buttons(user_chat_id, admin_chat_id):
    keyboard = types.InlineKeyboardMarkup()
    
    # Tugma
    stop_contact_button = types.InlineKeyboardButton(
        text="Aloqani to'xtatish", 
        callback_data=f"stop_contact_{user_chat_id}_{admin_chat_id}"
    )
    
    keyboard.add(stop_contact_button)
    
    # Foydalanuvchiga xabar yuborish
    bot.send_message(
        user_chat_id, 
        "Aloqa o'rnatildi. Aloqani to'xtatish uchun tugmani bosing:", 
        reply_markup=keyboard
    )
    
    # Adminga xabar yuborish
    bot.send_message(
        admin_chat_id, 
        "Foydalanuvchi bilan aloqa o'rnatildi. Aloqani to'xtatish uchun tugmani bosing:", 
        reply_markup=keyboard
    )

# Foydalanuvchining xabarini admin bilan almashish
@bot.message_handler(func=lambda message: str(message.chat.id) in active_contacts)
def send_message_to_admin(message):
    user_chat_id = message.chat.id
    bot.send_message(ADMIN_CHAT_ID, f"Foydalanuvchi: {message.from_user.first_name}\n@{message.from_user.username}\n xabar yubordi: \n{message.text}")

# Admin xabarini foydalanuvchiga yuborish
@bot.message_handler(func=lambda message: message.chat.id == ADMIN_CHAT_ID)
def send_message_to_user(message):
    for user_chat_id in active_contacts.keys():
        bot.send_message(user_chat_id, f"Admin: {message.text}")

# Aloqani rad etish bosilganda ishlaydigan funksiya
@bot.callback_query_handler(func=lambda call: call.data.startswith("reject_contact_"))
def reject_contact(call):
    user_chat_id = call.data.split("_")[-1]  # Foydalanuvchi chat ID sini olish
    bot.send_message(user_chat_id, "Aloqa rad etildi.")
    bot.send_message(ADMIN_CHAT_ID, f"Foydalanuvchi (Chat ID: {user_chat_id}) aloqa o'rnatishni rad etdi.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("stop_contact_"))
def stop_contact(call):
    # Callback data'dan chat IDlarini olish
    user_chat_id, admin_chat_id = call.data.split("_")[2], call.data.split("_")[3]

    # Foydalanuvchini aloqa ro'yxatidan o'chirish
    if user_chat_id in active_contacts:
        del active_contacts[user_chat_id]
        
        # Foydalanuvchiga aloqa to'xtatilgani haqida xabar yuborish
        bot.send_message(user_chat_id, "Aloqa to'xtatildi.")
        
        # Adminga aloqa to'xtatilgani haqida xabar yuborish
        bot.send_message(admin_chat_id, f"Foydalanuvchi (Chat ID: {user_chat_id})bilan aloqa to'xtatildi.")
    else:
        bot.send_message(user_chat_id, "Aloqa avvaldan to'xtatilgan.")


# Botni ishga tushirish
import time
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(5) 

