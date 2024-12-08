import telebot
from googletrans import Translator, LANGUAGES

API_TOKEN = '7739258677:AAFpSCokqjV_CzdYlUPzsCUE8L7YLi3lWdQ'  # Your API token
bot = telebot.TeleBot(API_TOKEN)
translator = Translator()

# Dictionary to store user preferences
user_languages = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    intro_message = (
        "👋 Welcome to the Telelingo Bot!\n\n"
        "This bot allows you to translate text between different languages effortlessly.\n"
        "Just send any text, and it will be translated to your preferred language!\n\n"
        "Here are some commands you can use:\n"
        "/help - Get information on how to use the bot\n"
        "/lang - See a list of available languages\n"
        "/setlang <language_code> - Set your preferred translation language\n"
    )
    bot.reply_to(message, intro_message)

@bot.message_handler(commands=['help'])
def show_help(message):
    commands = (
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/lang - List available languages\n"
        "/setlang <language_code> - Set your preferred language for translation\n"
        "Just send me any message to translate it!"
    )
    bot.reply_to(message, f"Available commands:\n{commands}")

@bot.message_handler(commands=['lang'])
def list_languages(message):
    languages = '\n'.join([f"{code}: {name}" for code, name in LANGUAGES.items()])
    bot.reply_to(message, f"Available languages:\n{languages}")

@bot.message_handler(commands=['setlang'])
def set_language(message):
    lang_code = message.text.split()[1] if len(message.text.split()) > 1 else None
    if lang_code in LANGUAGES:
        user_languages[message.from_user.id] = lang_code
        bot.reply_to(message, f"Language set to: {LANGUAGES[lang_code]}")
    else:
        bot.reply_to(message, "Invalid language code. Use /lang to see available languages.")

@bot.message_handler(func=lambda message: message.text and not message.text.startswith('/'))
def translate_message(message):
    user_id = message.from_user.id
    target_language = user_languages.get(user_id, 'en')  # Default to English if not set

    try:
        translated = translator.translate(message.text, dest=target_language)
        response = f"Original: {message.text}\nTranslated: {translated.text} ({translated.src} to {target_language})"
        bot.reply_to(message, response)
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

if __name__ == '__main__':
    print("Bot is running...")
    bot.polling()
