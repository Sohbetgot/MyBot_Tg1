import telebot
from telebot import types
import json
import time
from datetime import datetime, timedelta

BOT_TOKEN = '7220349197:AAF6LxnRHGuDds3isgbFMKSER8rMquwx_hw'
ADMIN_KEY = 'DİLPROMEYH4'

bot = telebot.TeleBot(BOT_TOKEN)

# Ulanyjy maglumatlaryny ýükle we sakla funksiýalary
def load_users():
    try:
        with open('users.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_users(data):
    with open('users.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def is_premium(user):
    if user is None:
        return False
    if 'premium' in user:
        now = int(time.time())
        return now < user['premium']
    return False

def format_profile(user_id, user):
    if user is None:
        return "Ulanyjy tapylmady."
    premium_text = ""
    if is_premium(user):
        dt = datetime.fromtimestamp(user['premium']).strftime('%d.%m.%Y')
        premium_text = f"\n💰 Платны Версиа ✅\n📅 Действует до: {dt}\n🆓 Использовано вопросов: {user.get('used', 0)}/∞"
    else:
        premium_text = f"\n💰 Безплатны Версиа 🆓\n❌ Подписка не активна\n🆓 Использовано вопросов: {user.get('used', 0)}/3"

    return f"👤 Profilim\n\n🆔 ID: {user_id}\n👤 Имя: {user.get('name', 'N/A')}{premium_text}"

# --- MENÝULAR ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🤖 Sorag Başlamak?', '👤 PROFİL')
    markup.add('💎 PREMİUM ALMAK', '🌐 DIL UÝTGETMEK')
    return markup

def back_button_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('⬅️ Yza gaýt')
    return markup

def sorag_start_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🆓 Mugt Versiýa', '💎 Premium Versiýa')
    markup.add('⬅️ Yza gaýt')
    return markup

def dil_uytgetme_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🇹🇲 TÜRKMEN', '🇷🇺 RUS', '🇬🇧 ENGLISH')
    markup.add('⬅️ Yza gaýt')
    return markup

def admin_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('👤 Ulanyja Premium Bermek', '⬅️ Çykmak')
    return markup

# --- KOMANDALAR ---
@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = str(message.from_user.id)
    users = load_users()
    if user_id not in users:
        users[user_id] = {'name': message.from_user.first_name, 'used': 0, 'lang': 'tm'}
        save_users(users)
    bot.send_message(message.chat.id, "👋 Hoş geldiňiz! Men size kömek etmäge taýýar!", reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == '⬅️ Yza gaýt')
def back_handler(message):
    bot.send_message(message.chat.id, "Baş menýu:", reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == '🤖 Sorag Başlamak?')
def sorag_baslamak(message):
    bot.send_message(message.chat.id, "Haýsy görnüşde dowam etmek isleýärsiňiz?", reply_markup=sorag_start_menu())

@bot.message_handler(func=lambda m: m.text == '🆓 Mugt Versiýa')
def mugt_version(message):
    user_id = str(message.from_user.id)
    users = load_users()
    user = users.get(user_id)
    if user is None:
        users[user_id] = {'name': message.from_user.first_name, 'used': 0, 'lang': 'tm'}
        user = users[user_id]
        save_users(users)

    if is_premium(user):
        bot.send_message(message.chat.id, "Siz eýýäm Premium ulanyjy!", reply_markup=back_button_menu())
        return

    if user.get('used', 0) >= 3:
        bot.send_message(message.chat.id, "❌ Mugt limitiňize ýetdiňiz. Premium alyň.", reply_markup=back_button_menu())
    else:
        user['used'] = user.get('used', 0) + 1
        save_users(users)
        bot.send_message(message.chat.id, "✅ Sorag kabul edildi! (Mugt ulanyş)", reply_markup=back_button_menu())

@bot.message_handler(func=lambda m: m.text == '💎 Premium Versiýa')
def premium_access(message):
    user_id = str(message.from_user.id)
    users = load_users()
    user = users.get(user_id)
    if is_premium(user):
        bot.send_message(message.chat.id, "✅ Premium sorag kabul edildi!", reply_markup=back_button_menu())
    else:
        bot.send_message(message.chat.id, "🚫 Sizde Premium ýok. Ilki Premium alyň!", reply_markup=back_button_menu())

@bot.message_handler(func=lambda m: m.text == '👤 PROFİL')
def profile_handler(message):
    user_id = str(message.from_user.id)
    users = load_users()
    user = users.get(user_id)
    bot.send_message(message.chat.id, format_profile(user_id, user), reply_markup=back_button_menu())

@bot.message_handler(func=lambda m: m.text == '💎 PREMİUM ALMAK')
def premium_info(message):
    bot.send_message(message.chat.id, "Premium almak üçin 👉 t.me/DaykaH4 bilen habarlaşyň!\n7 günlük we 30 günlük wariantlar elýeterli.", reply_markup=back_button_menu())

@bot.message_handler(func=lambda m: m.text == '🌐 DIL UÝTGETMEK')
def change_lang(message):
    bot.send_message(message.chat.id, "Dil saýlaň:", reply_markup=dil_uytgetme_menu())

@bot.message_handler(func=lambda m: m.text in ['🇹🇲 TÜRKMEN', '🇷🇺 RUS', '🇬🇧 ENGLISH'])
def set_lang(message):
    lang_code = {
        '🇹🇲 TÜRKMEN': 'tm',
        '🇷🇺 RUS': 'ru',
        '🇬🇧 ENGLISH': 'en'
    }
    user_id = str(message.from_user.id)
    users = load_users()
    if user_id in users:
        users[user_id]['lang'] = lang_code[message.text]
        save_users(users)
    bot.send_message(message.chat.id, "✅ Dil üstünlikli üýtgedildi!", reply_markup=back_button_menu())

# --- ADMIN PANEL ---

admin_sessions = set()

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    parts = message.text.split()
    if len(parts) == 2 and parts[1] == ADMIN_KEY:
        admin_sessions.add(message.from_user.id)
        bot.send_message(message.chat.id, "🔐 Admin panel açyldy!", reply_markup=admin_menu())
    else:
        bot.send_message(message.chat.id, "❌ Nädogry açar söz!")

def is_admin(user_id):
    return user_id in admin_sessions

@bot.message_handler(func=lambda m: is_admin(m.from_user.id) and m.text == '👤 Ulanyja Premium Bermek')
def premium_bermek(message):
    bot.send_message(message.chat.id, "Ulanyjy ID + gün ýaz: (meselem: 123456789 7)", reply_markup=back_button_menu())
    bot.register_next_step_handler(message, process_premium)

def process_premium(message):
    try:
        user_id, days = message.text.split()
        days = int(days)
        users = load_users()
        if user_id in users:
            now = int(time.time())
            premium_until = users[user_id].get('premium', 0)
            if now > premium_until:
                users[user_id]['premium'] = now + days * 86400
            else:
                users[user_id]['premium'] += days * 86400
            save_users(users)
            bot.send_message(message.chat.id, f"✅ {days} gün Premium berildi!", reply_markup=admin_menu())
        else:
            bot.send_message(message.chat.id, "Ulanyjy tapylmady!", reply_markup=admin_menu())
    except:
        bot.send_message(message.chat.id, "❌ Nädogry format. ID + gün ýazmaly", reply_markup=admin_menu())

@bot.message_handler(func=lambda m: is_admin(m.from_user.id) and m.text == '⬅️ Çykmak')
def admin_exit(message):
    admin_sessions.discard(message.from_user.id)
    bot.send_message(message.chat.id, "Admin panelden çykdyň.", reply_markup=main_menu())

# --- Programma işledilýär ---
bot.infinity_polling()
