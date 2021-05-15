import telebot

bot = telebot.TeleBot("1886341467:AAH2IJ6JdNf03hZC9-672AP3yW-4_V71K3g")

# Обрабатываются все сообщения содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, "Привет, " + message.chat.username)

# Обрабатывается все документы и аудиозаписи
@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    pass

#@bot.message_handler(content_types=['text'])
#def handle_docs_text(message):
#    bot.reply_to(message, "Превед, " + message.from_user.username + "!!!")

bot.polling(none_stop=True)