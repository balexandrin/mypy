import telebot

bot = telebot.TeleBot("1886341467:AAH2IJ6JdNf03hZC9-672AP3yW-4_V71K3g")

@bot.message_handler(content_types=['photo'])
def say_lmao(message):
    bot.reply_to(message, 'Nice meme XDD')


bot.polling(none_stop=True)