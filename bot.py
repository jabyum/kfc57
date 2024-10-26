import telebot
import buttons as bt
import database as db
from geopy import Photon

geolocator = Photon(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")
bot = telebot.TeleBot(token="7595209141:AAFHyqefmWLIu7tZzZgd7GnyYFIiIkhyBxQ")

db.add_product("Бургер", 20000, "лучший бургер", 10, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSf2535-40OVw2m6L8Auogu_w8LFXJfvV_XNw&s")
db.add_product("Чизбургер", 25000, "лучший чизбургер", 10, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSf2535-40OVw2m6L8Auogu_w8LFXJfvV_XNw&s")
db.add_product("Хот-дог", 15000, "лучший хот-дог", 0, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSf2535-40OVw2m6L8Auogu_w8LFXJfvV_XNw&s")

@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Добро пожаловать в бот доставки!")
    checker = db.check_user(user_id)
    if checker == True:
        bot.send_message(user_id, "Главное меню: ", reply_markup=bt.main_menu_kb())
    elif checker == False:
        bot.send_message(user_id, "Введите своё имя для регистрации")
        print(message.text)
        bot.register_next_step_handler(message, get_name)
def get_name(message):
    user_id = message.from_user.id
    name = message.text
    print(message.text)
    bot.send_message(user_id, "Теперь поделитесь своим номером",
                     reply_markup=bt.phone_button())
    bot.register_next_step_handler(message, get_phone_number, name)
def get_phone_number(message, name):
    user_id = message.from_user.id
    if message.contact:
        phone_number = message.contact.phone_number
        print(phone_number)
        bot.send_message(user_id, "Отправьте свою локацию", reply_markup=bt.location_button())
        bot.register_next_step_handler(message, get_location, name, phone_number)
    else:
        bot.send_message(user_id, "Отправьте свой номер через кнопку в меню")
        bot.register_next_step_handler(message, get_phone_number, name)
def get_location(message, name, phone_number):
    user_id = message.from_user.id
    if message.location:
        latitude = message.location.latitude
        longitude = message.location.longitude
        address = geolocator.reverse((latitude, longitude)).address
        print(name, phone_number, address)
        db.add_user(name=name, phone_number=phone_number, user_id=user_id)
        bot.send_message(user_id, "Вы успешно зарегистрировались!")
        bot.send_message(user_id, "Главное меню: ", reply_markup=bt.main_menu_kb())
    else:
        bot.send_message(user_id, "Отправьте свою локацию через кнопку в меню")
        bot.register_next_step_handler(message, get_location, name, phone_number)
@bot.callback_query_handler(lambda call: call.data in ["cart", "back"])
def all_cals(call):
    user_id = call.message.chat.id
    if call.data == "cart":
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Ваша корзина: ")
    elif call.data == "back":
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Главное меню: ",
                         reply_markup=bt.main_menu_kb())


@bot.message_handler(content_types=["text"])
def main_menu(message):
    user_id = message.from_user.id
    if message.text == "🍴Меню":
        all_products = db.get_pr_id_name()
        bot.send_message(user_id, "Выберите продукт:", reply_markup=bt.products_in(all_products))
    elif message.text == "🛒Корзина":
        bot.send_message(user_id, "Ваша корзина: ")
    elif message.text == "✒️Отзыв":
        bot.send_message(user_id, "Напишите текст вашего отзыва: ")
        # регистер некст степ хендлер для отлова текста отзыва


bot.infinity_polling()

