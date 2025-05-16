from telebot import types
import telebot
import os
from dotenv import load_dotenv

from database.repositories.user_repo import *
from models.user import User

load_dotenv()
token = os.getenv("TOKEN")
bot = telebot.TeleBot(token)
    
commStart = types.BotCommand(command='/start', description='Начать бота')
commHelp = types.BotCommand(command='/help', description='Помощь в использовании бота')
commMyProf = types.BotCommand(command='/my_profile', description='Мой профиль')
commChangeProf = types.BotCommand(command='/change_profile', description='Изменить профиль')

bot.set_my_commands([commStart, commHelp, commMyProf, commChangeProf])


with open('Rouder\introduction.txt', 'r', encoding='utf-8') as f:
    introduction = f.read()

with open('Rouder\pream.txt', 'r', encoding='utf-8') as f:
    preamble = f.read()

@bot.message_handler(commands=['start'])
def start(message):
    bot.set_chat_menu_button(message.chat.id, types.MenuButtonCommands('commands'))
    bot.send_message(message.chat.id, introduction)
    
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton('Да', callback_data='yes_indeed'),
        types.InlineKeyboardButton('Нет', callback_data='no_imnot')
    )
    bot.send_message(message.chat.id, preamble, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data in ['yes_indeed', 'no_imnot'])
def handle_introduction(call):
    bot.answer_callback_query(call.id)
    if call.data == 'yes_indeed':
        msg = bot.send_message(call.message.chat.id, "Как тебя зовут?")
        bot.register_next_step_handler(msg, get_name)
    else:
        bot.send_message(call.message.chat.id, "Жаль, возвращайся когда будешь готов!")

def get_name(message):
    user = User()
    user.telegram_id = message.chat.id
    user.name = message.text
    add_user(user)
    
    msg = bot.send_message(message.chat.id, "Какая у тебя фамилия?")
    bot.register_next_step_handler(msg, get_surname)

def get_surname(message):
    user = get_user(message.chat.id)
    if user:
        user.surname = message.text
        update_user(user)
        msg = bot.send_message(message.chat.id, "Отправь свою аватарку?")
        bot.register_next_step_handler(msg, get_avatar)

def get_avatar(message):
    user = get_user(message.chat.id)
    if user:
        photo = message.photo[-1]
        file_info = bot.get_file(photo.file_id)
        dowloaded_file = bot.download_file(file_info.file_path)
        save_path = f'Rouder\\avatars\\{message.chat.id}_user_avatar.{file_info.file_path.rsplit('.', 2)[1]}'
        with open(save_path, 'wb') as new_avatar:
            new_avatar.write(dowloaded_file)
        user.avatar = save_path
        update_user(user)
        #bot.reply_to(message, 'Аватар сохранён')
        msg = bot.send_message(message.chat.id, "Сколько тебе лет?")
        bot.register_next_step_handler(msg, get_age)

def get_interests(message):
    music = types.InlineKeyboardMarkup()
    music.add(
        types.InlineKeyboardButton('Рок/Альтернатива', callback_data='rock|alter'),
        types.InlineKeyboardButton('Электронная музыка/Рейвы', callback_data='electr|rave'),
        types.InlineKeyboardButton('Хип-хоп/R&B', callback_data='hiphop|RnB'),
        types.InlineKeyboardButton('Поп', callback_data='pop'),
        types.InlineKeyboardButton('Шансон', callback_data='shanson'),
        types.InlineKeyboardButton('Ничего', callback_data='nothing')
    )
    bot.send_message(message.chat.id, 'Какая у тебя музыкальная ориентация?', reply_markup=music)
    place = types.InlineKeyboardMarkup()
    place.add(
        types.InlineKeyboardButton('Кофейный сноб (спешиалти кофе)', callback_data='coffee'),
        types.InlineKeyboardButton('Вино и сырные вечера', callback_data='wine'),
        types.InlineKeyboardButton('Крафтовое пиво', callback_data='beer'),
        types.InlineKeyboardButton('Амбассадор ресторанов', callback_data='restaurant'),
        types.InlineKeyboardButton('Уличная еда (бургеры, тако, фалафель)', callback_data='streetfood'),
        types.InlineKeyboardButton('Ничего', callback_data='nothing')
    )
    bot.send_message(message.chat.id, 'Какой у тебя вкус к местам?', reply_markup=place)
    actives = types.InlineKeyboardMarkup()
    actives.add(
        types.InlineKeyboardButton('Настольные игры (Мафия, Монополия)', callback_data='boardgames'),
        types.InlineKeyboardButton('Квизы и интеллектуальные баттлы', callback_data='quizes'),
        types.InlineKeyboardButton('Караоке', callback_data='karaoke'),
        types.InlineKeyboardButton('Танцы', callback_data='dances'),
        types.InlineKeyboardButton('Спорт-трансляции (футбол, баскетбол)', callback_data='sports'),
        types.InlineKeyboardButton('Ничего', callback_data='nothing')
    )
    bot.send_message(message.chat.id, 'Что ты предпочитаешь в местах отдыха?', reply_markup=actives)
    pop_culter = types.InlineKeyboardMarkup()
    pop_culter.add(
        types.InlineKeyboardButton('Кино и сериалы', callback_data='cinema'),
        types.InlineKeyboardButton('Марвел/DC и комиксы', callback_data='comics'),
        types.InlineKeyboardButton('Аниме и манга', callback_data='anime'),
        types.InlineKeyboardButton('Ностальгия по 90-м/2000-м', callback_data='nostalgia'),
        types.InlineKeyboardButton('Книги и журналы', callback_data='books'),
        types.InlineKeyboardButton('Ничего', callback_data='nothing')
    )
    bot.send_message(message.chat.id, 'Какой у тебя вкус к популярной культуре?', reply_markup=pop_culter)
    lifestyle = types.InlineKeyboardMarkup()
    lifestyle.add(
        types.InlineKeyboardButton('ЗОЖ и велнес (смузи, йога)', callback_data='zoj'),
        types.InlineKeyboardButton('Путешествия и тревел-стори', callback_data='travel'),
        types.InlineKeyboardButton('Крипта и стартапы (Темщик)', callback_data='crypto'),
        types.InlineKeyboardButton('Мода и стиль (Подшаренный)', callback_data='fashion'),
        types.InlineKeyboardButton('Экология/Zero Waste', callback_data='zero_waste'),
        types.InlineKeyboardButton('Ничего', callback_data='nothing')
    )
    bot.send_message(message.chat.id, 'Какой у тебя вкус к жизни?', reply_markup=lifestyle)
    
def get_age(message):
    user = get_user(message.chat.id)
    if user:
        try:
            age = int(message.text)
            if age < 18:
                bot.send_message(message.chat.id, "Вам должно быть больше 18 лет!")
                return
            user.age = age
            update_user(user)
        except ValueError:
            msg = bot.send_message(message.chat.id, "Введите число!")
            bot.register_next_step_handler(msg, get_age)
            return
        
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton('Да', callback_data='confirm_yes'),
            types.InlineKeyboardButton('Нет', callback_data='confirm_no')
        )
        text = f"Тебе {age} лет, тебя зовут {user.name} {user.surname}?"
        bot.send_message(message.chat.id, text, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in ['confirm_yes', 'confirm_no'])
def handle_confirmation(call):
    user = get_user(call.message.chat.id)
    if call.data == 'confirm_yes':
        user.register = True
        update_user(user)
        msg = bot.send_message(call.message.chat.id, "Отлично! Регистрация завершена!")
        bot.answer_callback_query(call.id)
        bot.register_next_step_handler(msg, show_profile)
        
    else:
        delete_user(call.message.chat.id)
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "Давайте начнем заново!")
        msg = bot.send_message(call.message.chat.id, "Как тебя зовут?")
        bot.register_next_step_handler(msg, get_name)

@bot.message_handler(commands=['my_profile'])
def show_profile(message):
    user = get_user(message.chat.id)
    try:
        if (user.register == True):
            user_avatar = open(user.avatar, 'rb')
            bot.send_photo(message.chat.id, photo=user_avatar,caption=f'Имя: {user.name}\nФамилия: {user.surname}\nВозраст: {user.age}')
            #bot.send_message(message.chat.id,f'{user_avatar} \n Имя: {user.name} \n Фамилия: {user.surname} \n Возраст: {user.age}') # Картинка профиля, описание
        else:
            bot.send_message(message.chat.id, 'У вас ещё нет профиля. Напишите \start')
    except AttributeError:
        bot.send_message(message.chat.id, 'У вас ещё нет профиля. Напишите \start')

@bot.callback_query_handler(func=lambda call: call.data in ['music', 'place', 'actives', 'pop_culter', 'lifestyle'])
def handle_interests(call):
    user = get_user(call.message.chat.id)
    switcher = {
        'music': lambda: user.interests['music'].append(call.data),
        'place': lambda: user.interests['place'].append(call.data),
        'actives': lambda: user.interests['actives'].append(call.data),
        'pop_culter': lambda: user.interests['pop_culter'].append(call.data),
        'lifestyle': lambda: user.interests['lifestyle'].append(call.data),
        'nothing': lambda: None
    }
    func = switcher.get(call.data, lambda: None)
    func()

if __name__ == '__main__':
    bot.polling(none_stop=True)