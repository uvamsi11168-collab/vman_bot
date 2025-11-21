import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import requests

BOT_TOKEN = "7680564992:AAFGEAkULeCJsMDKy23AvtK9HVRuqmtyuA8"
bot = telebot.TeleBot(BOT_TOKEN)

# -------------------------
# START COMMAND + MENU
# -------------------------
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("About")
    btn2 = KeyboardButton("Features")
    btn3 = KeyboardButton("Creator❤️")
    btn4 = KeyboardButton("Help")
    btn5 = KeyboardButton("Photo")
    btn6 = KeyboardButton("Audio")
    btn7 = KeyboardButton("Sticker")
    btn8 = KeyboardButton("Weather")
    btn9 = KeyboardButton("Movie")
    btn10 = KeyboardButton("YouTube")

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5, btn6)
    markup.add(btn7, btn8)
    markup.add(btn9, btn10)

    bot.reply_to(message,
                 "🔥 Vman_Bot Is Alive 😎\nSelect Option:", reply_markup=markup)

# -------------------------
# INLINE BUTTONS
# -------------------------
@bot.message_handler(commands=['links'])
def inline_buttons(message):
    inline = InlineKeyboardMarkup()
    b1 = InlineKeyboardButton("Open Website", url="https://google.com")
    b2 = InlineKeyboardButton("Share Bot", url=f"https://t.me/{bot.get_me().username}")
    b3 = InlineKeyboardButton("Contact Creator", url="https://t.me/Vamsi")

    inline.add(b1, b2)
    inline.add(b3)

    bot.send_message(message.chat.id, "Links Menu:", reply_markup=inline)

# --------------------------------
# BUTTON REPLIES
# --------------------------------
@bot.message_handler(func=lambda msg: msg.text in ["About", "Features", "Creator❤️", "Help"])
def button_reply(message):
    if message.text == "About":
        bot.reply_to(message, "🔥 This is Vman Bot – Fully Loaded Telegram Bot")
    elif message.text == "Features":
        bot.reply_to(message, "⭐ Auto Replies\n⭐ Buttons\n⭐ Media Replies\n⭐ Weather\n⭐ Movies\n⭐ YouTube Download")
    elif message.text == "Creator❤️":
        bot.reply_to(message, "Created by Vamsi 💖")
    elif message.text == "Help":
        bot.reply_to(message, "Use the menu to explore all features!")

# -------------------------
# PHOTO SENDER
# -------------------------
@bot.message_handler(func=lambda msg: msg.text == "Photo")
def send_photo(message):
    bot.send_photo(message.chat.id, "https://picsum.photos/400/300")

# -------------------------
# AUDIO SENDER
# -------------------------
@bot.message_handler(func=lambda msg: msg.text == "Audio")
def send_audio(message):
    bot.send_audio(message.chat.id,
                   "https://samplelib.com/lib/preview/mp3/sample-3s.mp3")

# -------------------------
# STICKER SENDER
# -------------------------
@bot.message_handler(func=lambda msg: msg.text == "Sticker")
def send_sticker(message):
    bot.send_sticker(message.chat.id,
                     "CAACAgUAAxkBAAEJZ5xlkN0eHEW1wq-yQ9YFjYcSQh0SIAAC8QUAAkHSkFbnXrhIRbkI8yME")

# -------------------------
# WEATHER CHECKER
# -------------------------
@bot.message_handler(func=lambda msg: msg.text == "Weather")
def weather_start(message):
    bot.reply_to(message, "City పేరు పంపండి (Example: Hyderabad)")

@bot.message_handler(func=lambda msg: True if msg.text not in 
["About","Features","Creator❤️","Help","Photo","Audio","Sticker","Movie","YouTube"] else False)
def weather_lookup(message):
    city = message.text
    api = f"https://wttr.in/{city}?format=3"
    try:
        result = requests.get(api).text
        bot.reply_to(message, f"🌤 Weather: {result}")
    except:
        bot.reply_to(message, "❌ Weather Error")

# -------------------------
# MOVIE SEARCH (IMDb)
# -------------------------
@bot.message_handler(func=lambda msg: msg.text == "Movie")
def movie_start(message):
    bot.reply_to(message, "Movie Name పంపండి!")

@bot.message_handler(func=lambda msg: msg.text and msg.text != "")
def movie_search(message):
    movie = message.text
    api = f"https://www.omdbapi.com/?t={movie}&apikey=564727fa"
    data = requests.get(api).json()

    if data["Response"] == "True":
        reply = f"""
🎬 *{data['Title']}*
⭐ Rating: {data['imdbRating']}
📅 Year: {data['Year']}
🎭 Actors: {data['Actors']}
📝 Plot: {data['Plot']}
"""
        bot.send_message(message.chat.id, reply)
    else:
        bot.send_message(message.chat.id, "❌ Movie Not Found")

# -------------------------
# YOUTUBE DOWNLOAD
# -------------------------
@bot.message_handler(func=lambda msg: msg.text == "YouTube")
def yt_start(message):
    bot.reply_to(message, "YouTube Link పంపండి")

@bot.message_handler(func=lambda msg: msg.text.startswith("http"))
def youtube_downloader(message):
    link = message.text
    bot.reply_to(message, f"📥 Download Link:\nhttps://api.onlinevideoconverter.pro/api/convert?url={link}")

# -------------------------
# GROUP WELCOME
# -------------------------
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for user in message.new_chat_members:
        bot.send_message(message.chat.id,
            f"🔥 Welcome {user.first_name}! Enjoy the group 😎")

# -------------------------
# BAD WORD FILTER
# -------------------------
bad_words = ["fuck", "sex", "bitch", "nude"]

@bot.message_handler(func=lambda msg: any(w in msg.text.lower() for w in bad_words))
def block_badwords(message):
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "⚠ Bad words not allowed!")

# -------------------------
# AUTO ECHO
# -------------------------
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, f"మీరు పంపింది: {message.text}")

# -------------------------
bot.polling()


