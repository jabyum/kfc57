from telebot import types

def phone_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('Поделиться номером',
                                  request_contact=True)
    kb.add(button)
    return kb
def location_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('Поделиться локацией',
                                  request_location=True)
    kb.add(button)
    return kb
def main_menu_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu = types.KeyboardButton(text="🍴Меню")
    cart = types.KeyboardButton(text="🛒Корзина")
    feedback = types.KeyboardButton(text="✒️Отзыв")
    kb.add(menu, cart)
    kb.row(feedback)
    return kb
def products_in(products):
    kb = types.InlineKeyboardMarkup(row_width=2)
    # статичные кнопки
    cart = types.InlineKeyboardButton(text="Корзина", callback_data="cart")
    back = types.InlineKeyboardButton(text="Назад", callback_data="back")
    # динамичные кнопки
    all_products = [types.InlineKeyboardButton(text=f"{product[1]}", callback_data=f"prod_{products[0]}")
                    for product in products]
    kb.add(*all_products)
    kb.row(cart)
    kb.row(back)
    return kb
