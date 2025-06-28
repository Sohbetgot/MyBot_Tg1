import telebot
import openai
import json
import time
from datetime import datetime, timedelta
from telebot import types

BOT_TOKEN = '7220349197:AAF6LxnRHGuDds3isgbFMKSER8rMquwx_hw'
OPENAI_API_KEY = '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'
ADMIN_KEY = 'DILPROMEYH4'

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

# --- USER DATA ---
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
        return int(time.time()) < user['premium']
    return False

# --- CHATGPT ---
def ask_chatgpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message['content'].strip()

# --- MENUS ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🤖 Sorag Başlamak?', '👤 PROFİL')
    markup.add('💎 PREMİUM ALMAK', '🌐 DIL UÝTGETMEK')
    return markup

def back_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('⬅️ Yza gaýt')
    return markup

def sorag_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🆓 Mugt Versiýa', '💎 Premium Versiýa')
    markup.add('⬅️ Yza gaýt')
    return markup

def lang_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🇹🇲 TÜRKMEN', '🇷🇺 RUS', '🇬🇧 ENGLISH')
    markup.add('⬅️ Yza gaýt')
    return markup

def admin_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('👤 Ulanyja Premium Bermek', '⬅️ Çykmak')
    return markup

# --- HANDLERS ---
@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    users = load_users()
    if user_id not in users:
        users[user_id] = {'name': message.from_user.first_name, 'used': 0, 'lang': 'tm'}
        save_users(users)
    bot.send_message(message.chat.id, "👋 Hoş geldiňiz!", reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == '⬅️ Yza gaýt')
def go_back(message):
    bot.send_message(message.chat.id, "🔙 Baş menýu:", reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == '🤖 Sorag Başlamak?')
def sorag_basla(message):
    bot.send_message(message.chat.id, "Görnüş saýlaň:", reply_markup=sorag_menu())

@bot.message_handler(func=lambda m: m.text == '🆓 Mugt Versiýa')
def mugt_sorag(message):
    user_id = str(message.from_user.id)
    users = load_users()
    user = users.get(user_id)
    if not is_premium(user):
        if user['used'] >= 3:
            bot.send_message(message.chat.id, "❌ Mugt limitiňiz gutardy!", reply_markup=back_menu())
            return
    bot.send_message(message.chat.id, "✍️ Soragyňyzy ýazyň:", reply_markup=back_menu())
    bot.register_next_step_handler(message, handle_sorag)

@bot.message_handler(func=lambda m: m.text == '💎 Premium Versiýa')
def premium_sorag(message):
    user_id = str(message.from_user.id)
    users = load_users()
    user = users.get(user_id)
    if is_premium(user):
        bot.send_message(message.chat.id, "✍️ Soragyňyzy ýazyň:", reply_markup=back_menu())
        bot.register_next_step_handler(message, handle_sorag)
    else:
        bot.send_message(message.chat.id, "🚫 Sizde Premium ýok!", reply_markup=back_menu())

@bot.message_handler(func=lambda m: m.text == '👤 PROFİL')
def profil(message):
    user_id = str(message.from_user.id)
    users = load_users()
    user = users.get(user_id)
    status = "✅ Платны Версиа" if is_premium(user) else "🆓 Безплатны Версиа"
    limit = "∞" if is_premium(user) else f"{user['used']}/3"
    text = f"👤 Profilim\n\n🆔 ID: {user_id}\n👤 Ady: {user['name']}\n💰 Statusy: {status}\n📊 Ulanyş: {limit}"
    bot.send_message(message.chat.id, text, reply_markup=back_menu())

@bot.message_handler(func=lambda m: m.text == '💎 PREMİUM ALMAK')
def premium_info(message):
    bot.send_message(message.chat.id, "Premium almak üçin: t.me/DaykaH4 bilen habarlaşyň!", reply_markup=back_menu())

@bot.message_handler(func=lambda m: m.text == '🌐 DIL UÝTGETMEK')
def change_lang(message):
    bot.send_message(message.chat.id, "Dil saýlaň:", reply_markup=lang_menu())

@bot.message_handler(func=lambda m: m.text in ['🇹🇲 TÜRKMEN', '🇷🇺 RUS', '🇬🇧 ENGLISH'])
def set_lang(message):
    lang_map = {
        '🇹🇲 TÜRKMEN': 'tm',
        '🇷🇺 RUS': 'ru',
        '🇬🇧 ENGLISH': 'en'
    }
    users = load_users()
    user_id = str(message.from_user.id)
    if user_id in users:
        users[user_id]['lang'] = lang_map[message.text]
        save_users(users)
    bot.send_message(message.chat.id, "✅ Dil üýtgedildi!", reply_markup=back_menu())

# --- AI Soraga jogap ---
def handle_sorag(message):
    user_id = str(message.from_user.id)
    users = load_users()
    user = users.get(user_id)
    bot.send_chat_action(message.chat.id, 'typing')
    try:
        answer = ask_chatgpt(message.text)
        bot.send_message(message.chat.id, answer, reply_markup=back_menu())
        if not is_premium(user):
            user['used'] += 1
            save_users(users)
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ýalňyşlyk: {e}", reply_markup=back_menu())

# --- Admin panel ---
admin_sessions = set()

@bot.message_handler(commands=['admin'])
def admin_start(message):
    if len(message.text.split()) == 2 and message.text.split()[1] == ADMIN_KEY:
        admin_sessions.add(message.from_user.id)
        bot.send_message(message.chat.id, "🔐 Admin panel açyldy!", reply_markup=admin_menu())
    else:
        bot.send_message(message.chat.id, "❌ Nädogry açarsöz!")

@bot.message_handler(func=lambda m: m.text == '👤 Ulanyja Premium Bermek' and m.from_user.id in admin_sessions)
def admin_premium(message):
    bot.send_message(message.chat.id, "Ulanyjy ID + gün giriziň: (meselem: 123456789 7)", reply_markup=back_menu())
    bot.register_next_step_handler(message, process_premium)

def process_premium(message):
    try:
        user_id, days = message.text.split()
        days = int(days)
        users = load_users()
        if user_id in users:
            now = int(time.time())
            users[user_id]['premium'] = now + days * 86400
            save_users(users)
            bot.send_message(message.chat.id, f"✅ {days} günlük Premium berildi!", reply_markup=admin_menu())
        else:
            bot.send_message(message.chat.id, "❌ Ulanyjy tapylmady!", reply_markup=admin_menu())
    except:
        bot.send_message(message.chat.id, "❌ Format ýalňyş. ID + gün ýazmaly!", reply_markup=admin_menu())

@bot.message_handler(func=lambda m: m.text == '⬅️ Çykmak' and m.from_user.id in admin_sessions)
def admin_exit(message):
    admin_sessions.discard(message.from_user.id)
    bot.send_message(message.chat.id, "🔒 Admin panelden çykdyň!", reply_markup=main_menu())

# --- Run bot ---
bot.infinity_polling()
