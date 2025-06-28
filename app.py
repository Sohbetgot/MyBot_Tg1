from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

USER_DATA = {}  # Ulanyjylaryň maglumatlaryny saklamak üçin

# Admin paroly
ADMIN_PASSWORD = "DİLPROMEYH4"
ADMIN_CHAT_ID = 8143084360  # Adminiň ID-nä ýerine ýetirip bilersiňiz

# Botuň başlangyç komandasy
def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    USER_DATA.setdefault(user_id, {
        'premium': False,
        'premium_type': None,
        'used_free': 0,
        'language': 'TÜRKMEN'  # Başlangyç dili
    })
    
    keyboard = [
        [InlineKeyboardButton("Sorag Başlamak", callback_data='start_question'),
         InlineKeyboardButton("Profil", callback_data='profile')],
        [InlineKeyboardButton("Premium Alma", callback_data='buy_premium'),
         InlineKeyboardButton("Dil Uýtgetmek", callback_data='change_language')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text("Hoş geldiňiz!", reply_markup=reply_markup)

# Sorag başlamak
def start_question(update: Update, context: CallbackContext) -> None:
    user_id = update.callback_query.from_user.id
    update.callback_query.answer()
    
    keyboard = [
        [InlineKeyboardButton("Mugt Version", callback_data='free_version'),
         InlineKeyboardButton("Premium Version", callback_data='premium_version')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.callback_query.message.reply_text("Sorag başlamak üçin saýlaň:", reply_markup=reply_markup)

# Mugt we Premium görnüşleri 
def free_version(update: Update, context: CallbackContext) -> None:
    user_id = update.callback_query.from_user.id
    USER_DATA[user_id]['used_free'] += 1
    # Mugt dolandyryş şemasyny ýerine ýetiriň
    update.callback_query.answer()
    update.callback_query.message.reply_text("Siz mugt hyzmatdan peýdalanyp başladyňyz.")

def premium_version(update: Update, context: CallbackContext) -> None:
    user_id = update.callback_query.from_user.id
    # Premium dolandyryş şemasyny ýerine ýetiriň
    update.callback_query.answer()
    update.callback_query.message.reply_text("Siz Premium hyzmatyna geçmek isleýänsiňiz.")

# Profil
def profile(update: Update, context: CallbackContext) -> None:
    user_id = update.callback_query.from_user.id
    user_data = USER_DATA[user_id]
    
    profile_msg = f"👤 Profilim\n\n"
    profile_msg += f"🆔 ID: {user_id}\n"
    profile_msg += f"👤 Ady: {update.callback_query.from_user.first_name}\n"
    profile_msg += f"💰 {('Платны Версиа ✅' if user_data['premium'] else 'Безплатны Версиа 🆓')}\n"
    profile_msg += f"❌ Подписка не активна" if not user_data['premium'] else "" 
    profile_msg += f"\n🆓 Использовано вопросов: {user_data['used_free']}/{3 if not user_data['premium'] else '∞'}"
    
    update.callback_query.answer()
    update.callback_query.message.reply_text(profile_msg)

# Premium almak
def buy_premium(update: Update, context: CallbackContext) -> None:
    update.callback_query.answer()
    update.callback_query.message.reply_text("Premium almak üçin t.me/DaykaH4 ýüz tutup bilersiňiz!")

# Dil uýtgetmek
def change_language(update: Update, context: CallbackContext) -> None:
    update.callback_query.answer()
    
    keyboard = [
        [InlineKeyboardButton("RUS", callback_data='set_language_RUS'),
         InlineKeyboardButton("TÜRKMEN", callback_data='set_language_TR'),
         InlineKeyboardButton("ENGLISH", callback_data='set_language_EN')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.callback_query.message.reply_text("Dil saýlaň:", reply_markup=reply_markup)

# Dili üýtgetmek gutusy
def set_language(update: Update, context: CallbackContext) -> None:
    user_id = update.callback_query.from_user.id
    language_map = {
        'set_language_RUS': 'RUS',
        'set_language_TR': 'TÜRKMEN',
        'set_language_EN': 'ENGLISH'
    }
    
    USER_DATA[user_id]['language'] = language_map[update.callback_query.data]
    update.callback_query.answer()
    update.callback_query.message.reply_text(f"Dil '{USER_DATA[user_id]['language']}' saýlandy.")

# Admin Panel
def admin_panel(update: Update, context: CallbackContext) -> None:
    # Admin panela giriş
    if update.message.text == ADMIN_PASSWORD:
        update.message.reply_text("Admin paneline hoş geldiňiz!")
        # Admin interfeýsini görkezmek üçin kod goşup bilersiňiz
    else:
        update.message.reply_text("Giriş başarsyz, dogry açar söz giriziň.")

def main() -> None:
    updater = Updater("7220349197:AAF6LxnRHGuDds3isgbFMKSER8rMquwx_hw")

    # Komandalar we düwmeleri goşmak
    updater.dispatcher.add_handler(CommandHandle("start", start))
    updater.dispatcher.add_handler(CallbackQueryHandler(start_question, pattern='start_question'))
    updater.dispatcher.add_handler(CallbackQueryHandler(free_version, pattern='free_version'))
    updater.dispatcher.add_handler(CallbackQueryHandler(premium_version, pattern='premium_version'))
    updater.dispatcher.add_handler(CallbackQueryHandler(profile, pattern='profile'))
    updater.dispatcher.add_handler(CallbackQueryHandler(buy_premium, pattern='buy_premium'))
    updater.dispatcher.add_handler(CallbackQueryHandler(change_language, pattern='change_language'))
    updater.dispatcher.add_handler(CallbackQueryHandler(set_language, pattern='set_language_RUS|set_language_TR|set_language_EN'))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, admin_panel))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
