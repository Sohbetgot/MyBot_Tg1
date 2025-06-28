from telebot import TeleBot, types
import json
import time
from datetime import datetime, timedelta

# BOT TOKEN GIRIZ
BOT_TOKEN = '7220349197:AAF6LxnRHGuDds3isgbFMKSER8rMquwx_hw'
bot = TeleBot(BOT_TOKEN)

# Faýllar bilen işleýän funksiýalar
def load_users():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except:
        return {}

def save_users(data):
    with open('users.json', 'w') as f:
        json.dump(data, f, indent=2)

def is_premium(user):
    if 'premium' in user:
        now = int(time.time())
        return now < user['premium']
    return False

def format_profile(user_id, user):
    premium_text = ""
    if is_premium(user):
        dt = datetime.fromtimestamp(user['premium']).strftime('%d.%m.%Y')
        premium_text = f"\n💰 Платны Версиа ✅\n📅 Действует до: {dt}\n🆓 Использовано вопросов: {user.get('used', 0)}/∞"
    else:
        premium_text = f"\n💰 Безплатны Версиа 🆓\n❌ Подписка не активна\n🆓 Использовано вопросов: {user.get('used', 0)}/3"

    return f"👤 Profilim\n\n🆔 ID: {user_id}\n👤 Имя: {user.get('name', 'N/A')}{premium_text}"

@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = str(message.from_user.id)
    users = load_users()
    if user_id not in users:
        users[user_id] = {'name': message.from_user.first_name, 'used': 0, 'lang': 'tm'}
        save_users(users)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🤖 Sorag Başlamak?', '👤 PROFİL')
    markup.add('💎 PREMİUM ALMAK', '🌐 DIL UÝTGETMEK')
    bot.send_message(message.chat.id, "👋 Hoş geldiňiz! Men size kömek etmäge taýýar!", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == '👤 PROFİL')
def profile_handler(message):
    user_id = str(message.from_user.id)
    users = load_users()
    user = users.get(user_id, {})
    bot.send_message(message.chat.id, format_profile(user_id, user))

@bot.message_handler(func=lambda m: m.text == '💎 PREMİUM ALMAK')
def premium_info(message):
    bot.send_message(message.chat.id, "Premium almak üçin 👉 t.me/DaykaH4 bilen habarlaşyň!\n7 günlük we 30 günlük wariantlar elýeterli.")

@bot.message_handler(func=lambda m: m.text == '🌐 DIL UÝTGETMEK')
def change_lang(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🇹🇲 TÜRKMEN', '🇷🇺 RUS', '🇬🇧 ENGLISH')
    bot.send_message(message.chat.id, "Dil saýlaň:", reply_markup=markup)

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
    bot.send_message(message.chat.id, "✅ Dil üstünlikli üýtgedildi!")

@bot.message_handler(func=lambda m: m.text == '🤖 Sorag Başlamak?')
def sorag_baslamak(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🆓 Mugt Versiýa', '💎 Premium Versiýa')
    bot.send_message(message.chat.id, "Haýsy görnüşde dowam etmek isleýärsiňiz?", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == '🆓 Mugt Versiýa')
def mugt_version(message):
    user_id = str(message.from_user.id)
    users = load_users()
    user = users.get(user_id)
    if is_premium(user):
        bot.send_message(message.chat.id, "Siz eýýäm Premium ulanyjy!")
        return

    if user['used'] >= 3:
        bot.send_message(message.chat.id, "❌ Mugt limitiňize ýetdiňiz. Premium alyň.")
    else:
        user['used'] += 1
        save_users(users)
        bot.send_message(message.chat.id, "✅ Sorag kabul edildi! (Mugt ulanyş)")

@bot.message_handler(func=lambda m: m.text == '💎 Premium Versiýa')
def premium_access(message):
    user_id = str(message.from_user.id)
    users = load_users()
    user = users.get(user_id)
    if is_premium(user):
        bot.send_message(message.chat.id, "✅ Premium sorag kabul edildi!")
    else:
        bot.send_message(message.chat.id, "🚫 Sizde Premium ýok. Ilki Premium alyň!")

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.text.split(' ', 1)[-1] == 'DİLPROMEYH4':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('👤 Ulanyja Premium Bermek', '⬅️ Çykmak')
        bot.send_message(message.chat.id, "🔐 Admin panel açyldy!", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "❌ Nädogry açar söz!")

@bot.message_handler(func=lambda m: m.text == '👤 Ulanyja Premium Bermek')
def premium_bermek(message):
    bot.send_message(message.chat.id, "Ulanyjy ID + gün ýaz: (meselem: 123456789 7)")
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
            bot.send_message(message.chat.id, f"✅ {days} gün Premium berildi!")
        else:
            bot.send_message(message.chat.id, "Ulanyjy tapylmady!")
    except:
        bot.send_message(message.chat.id, "❌ Nädogry format. ID + gün ýazmaly")

bot.polling()
