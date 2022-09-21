import COVID19Py
import telebot
from telebot import types

token = "твой токен"

covid19 = COVID19Py.COVID19()
bot = telebot.TeleBot(token=token)

latest = covid19.getLatest()


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    st = types.KeyboardButton('Статистика')
    markup.add(st)
    send_mess = f"<b>Здравствуйте, {message.from_user.first_name}!</b>\n" \
                f"Бот выведет статистику по заболеваемости корона-вирусом в Украине\n" \
                f"Чтобы посмотреть статистику, введите любой текст"
    bot.send_message(message.chat.id, send_mess, parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def message(message):
    location = covid19.getLocationByCountryCode("UA")
    print(location)
    final_message = f"Данные по стране:\nНаселение: {location[0]['country_population']}\n" \
                f"Последнее обновление: {location[0]['last_updated'].split('T')[0]}\n" \
                f"Заболевших: {location[0]['latest']['confirmed']}\n" \
                f"Смертей: {location[0]['latest']['deaths']}\n" \
                f"Выздоровило: {location[0]['latest']['recovered']}\n"

    bot.send_message(message.chat.id, final_message, parse_mode='html')


bot.polling(none_stop=True)
