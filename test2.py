import telebot
import gettoken

bot = telebot.TeleBot(gettoken.token())

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет!\nЭтот бот предназначен для обмена ссылками на аудиокниги в открытом доступе.\nНадеюсь, что ты сможешь найти для себя тут что-нибудь интересное.\nИ буду очень благодарен, если ты добавишь ссылку на свою любимую аудиокнигу.', reply_markup=keyboard1)

bot.polling(none_stop=True)