from telebot import types
import telebot
import os
from dotenv import load_dotenv
from telebot.apihelper import ApiTelegramException
from geopy.geocoders import Nominatim 
from models.city import City

from database.repositories.user_repo import *
from models.user import User
from models.interest import Interest
from models.theme import Theme

load_dotenv()
token = os.getenv("TOKEN")
bot = telebot.TeleBot(token)

geolocator = Nominatim(user_agent="my_geopy_app")
global interests
interests = {'music': [], 'place': [], 'actives': [], 'pop_culter': [], 'lifestyle': []}
global users
users = {}
# Настройка команд бота
commStart = types.BotCommand(command='/start', description='Начать бота')
commHelp = types.BotCommand(command='/help', description='Помощь в использовании бота')
commMyProf = types.BotCommand(command='/my_profile', description='Мой профиль')
commChangeProf = types.BotCommand(command='/change_profile', description='Изменить профиль')
bot.set_my_commands([commStart, commHelp, commMyProf, commChangeProf])

# Загрузка текстов
with open('Rouder\\introduction.txt', 'r', encoding='utf-8') as f:
    introduction = f.read()
with open('Rouder\\pream.txt', 'r', encoding='utf-8') as f:
    preamble = f.read()

# Состояния пользователей
user_states = {}
user_choices = {}

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
@bot.message_handler(commands=['my_profile'])
def my_profile(message):
    show_profile(message)
    bot.send_message(message.chat.id, "Жаль, возвращайся когда будешь готов!")
@bot.callback_query_handler(func=lambda call: call.data in ['yes_indeed', 'no_imnot'])
def handle_introduction(call):
    bot.answer_callback_query(call.id)
    if call.data == 'yes_indeed':
        msg = bot.send_message(call.message.chat.id, "Как тебя зовут?")
        bot.register_next_step_handler(msg, get_name)
    else:
        bot.send_message(call.message.chat.id, "Жаль, возвращайся когда будешь готов!")

# Регистрация пользователя

def get_name(message):
    users[message.chat.id] = User()
    user = users[message.chat.id]
    user.telegram_id = message.chat.id
    user.name = message.text
    msg = bot.send_message(message.chat.id, "Какая у тебя фамилия?")
    bot.register_next_step_handler(msg, get_surname)

def get_surname(message):
    user = users[message.chat.id]
    if user:
        user.surname = message.text
        msg = bot.send_message(message.chat.id, "Отправь свою аватарку?")
        bot.register_next_step_handler(msg, get_avatar)

def get_avatar(message):
    user = users[message.chat.id]
    if user and message.photo:
        photo = message.photo[-1]
        file_info = bot.get_file(photo.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        save_path = f"Rouder\\avatars\\{message.chat.id}_user_avatar.{file_info.file_path.split('.')[-1]}"
        with open(save_path, 'wb') as new_avatar:
            new_avatar.write(downloaded_file)
        user.avatar = save_path
        start_interest_selection(message)

# Начало опроса по интересам

def start_interest_selection(message):
    chat_id = message.chat.id
    user_states[chat_id] = {
        'current_topic': 0,
        'topics': ['music', 'place', 'actives', 'pop_culter', 'lifestyle'],
        'selected': {}
    }
    user_choices[chat_id] = {topic: [] for topic in user_states[chat_id]['topics']}
    send_topic(chat_id)

# Отправка темы

def send_topic(chat_id):
    state = user_states.get(chat_id)
    if not state or state['current_topic'] >= len(state['topics']):
        return

    topic = state['topics'][state['current_topic']]
    markup = types.InlineKeyboardMarkup()
    next_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    next_keyboard.add(types.KeyboardButton('Следующая тема ➡️'))

    if topic == 'music':
        markup.add(
            types.InlineKeyboardButton('Рок/Альтернатива', callback_data='music_rock'),
            types.InlineKeyboardButton('Электронная музыка', callback_data='music_electro'),
            types.InlineKeyboardButton('Хип-хоп/R&B', callback_data='music_hiphop'),
            types.InlineKeyboardButton('Поп', callback_data='music_pop'),
            types.InlineKeyboardButton('Шансон', callback_data='music_shanson')
        )
        text = '🎵 Какая у тебя музыкальная ориентация?'
    elif topic == 'place':
        markup.add(
            types.InlineKeyboardButton('Кофейный сноб', callback_data='place_coffee'),
            types.InlineKeyboardButton('Вино и сыр', callback_data='place_wine'),
            types.InlineKeyboardButton('Крафтовое пиво', callback_data='place_beer'),
            types.InlineKeyboardButton('Рестораны', callback_data='place_restaurant'),
            types.InlineKeyboardButton('Уличная еда', callback_data='place_streetfood')
        )
        text = '🍽️ Какой у тебя вкус к местам?'
    elif topic == 'actives':
        markup.add(
            types.InlineKeyboardButton('Настольные игры', callback_data='actives_boardgames'),
            types.InlineKeyboardButton('Квизы', callback_data='actives_quizes'),
            types.InlineKeyboardButton('Караоке', callback_data='actives_karaoke'),
            types.InlineKeyboardButton('Танцы', callback_data='actives_dances'),
            types.InlineKeyboardButton('Спорт', callback_data='actives_sports')
        )
        text = '🎲 Что ты предпочитаешь в местах отдыха?'
    elif topic == 'pop_culter':
        markup.add(
            types.InlineKeyboardButton('Кино/сериалы', callback_data='pop_cinema'),
            types.InlineKeyboardButton('Комиксы', callback_data='pop_comics'),
            types.InlineKeyboardButton('Аниме', callback_data='pop_anime'),
            types.InlineKeyboardButton('Ностальгия', callback_data='pop_nostalgia'),
            types.InlineKeyboardButton('Книги', callback_data='pop_books')
        )
        text = '🎥 Какой у тебя вкус к поп-культуре?'
    else:  # topic == 'lifestyle'
        markup.add(
            types.InlineKeyboardButton('ЗОЖ', callback_data='life_zoj'),
            types.InlineKeyboardButton('Путешествия', callback_data='life_travel'),
            types.InlineKeyboardButton('Крипта', callback_data='life_crypto'),
            types.InlineKeyboardButton('Мода', callback_data='life_fashion'),
            types.InlineKeyboardButton('Экология', callback_data='life_ecology')
        )
        text = '🌱 Какой у тебя стиль жизни?'

    markup.add(types.InlineKeyboardButton('Пропустить тему', callback_data='skip'))
    bot.send_message(chat_id, text, reply_markup=markup)
    bot.send_message(chat_id, "Выбери несколько вариантов, затем нажми ➡️", reply_markup=next_keyboard)

# Получение местоположения
def get_location(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Поделись местоположением", reply_markup=keyboard)

    geolocator = Nominatim(user_agent = "name_of_your_app")
   
    # Возраст и подтверждение профиля

def get_age(message):
    user = users[message.chat.id]
    if user:
        try:
            age = int(message.text)
            print(age)
            if age < 18:
                bot.send_message(message.chat.id, "Вам должно быть больше 18 лет!")
                return
            user.age = age
            confirm_profile(message)
        except ValueError:
            msg = bot.send_message(message.chat.id, "Введите число!")
            bot.register_next_step_handler(msg, get_age)

def confirm_profile(message):
    print("confirm_profile")
    user = users[message.chat.id]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton('Да', callback_data='confirm_yes'),
        types.InlineKeyboardButton('Нет', callback_data='confirm_no')
    )
    bot.send_message(text = f"Тебе {user.age} лет, тебя зовут {user.name} {user.surname}?", reply_markup=keyboard, chat_id=message.chat.id)



@bot.message_handler(content_types=['location'])
def location (message):
    user = users[message.chat.id]
    latitude = message.location.latitude  
    longitude = message.location.longitude 

    # Определяем город с помощью обратного геокодирования  
    location = geolocator.reverse('{} {}'.format(message.location.latitude, message.location.longitude))
    address = location.raw['address']
    city = address.get('city', '')
    City.get_id(city)
    user.city = city
    bot.send_message(message.chat.id, "✅ Местоположение получено", reply_markup=types.ReplyKeyboardRemove())
    msg = bot.send_message(message.chat.id, "Сколько тебе лет?")
    bot.register_next_step_handler(msg, get_age)
    

# Обработка выбора интересов
@bot.callback_query_handler(func=lambda call: call.data in ['skip'] or call.data.startswith(('music_', 'place_', 'actives_', 'pop_', 'life_')))
def handle_interest(call):
    bot.answer_callback_query(call.id)
    chat_id = call.message.chat.id
    data = call.data

    if data == 'skip':
        handle_next_topic(call.message)
        return

    prefix, value = data.split('_', 1)
    # Маппинг префиксов
    category_map = {'pop': 'pop_culter', 'life': 'lifestyle'}
    category = category_map.get(prefix, prefix)

    if category in user_choices.get(chat_id, {}):
        if value in user_choices[chat_id][category]:
            user_choices[chat_id][category].remove(value)
        else:
            user_choices[chat_id][category].append(value)

    update_message_markup(call.message)

# Обновление разметки кнопок

def update_message_markup(message):
    chat_id = message.chat.id
    state = user_states.get(chat_id)
    if not state or state['current_topic'] >= len(state['topics']):
        return

    topic = state['topics'][state['current_topic']]
    if not message.reply_markup:
        return

    old = message.reply_markup.to_dict()['inline_keyboard']
    new_markup = types.InlineKeyboardMarkup()
    has_changes = False

    for row in old:
        buttons = []
        for btn in row:
            if btn['callback_data'] == 'skip':
                buttons.append(types.InlineKeyboardButton(text=btn['text'], callback_data='skip'))
                continue
            _, val = btn['callback_data'].split('_', 1)
            base_text = btn['text'].split('✓ ')
            base_text = base_text[1] if len(base_text) > 1 else base_text[0]
            if val in user_choices[chat_id][topic]:
                text = '✓ ' + base_text
            else:
                text = base_text
            if text != btn['text']:
                has_changes = True
            buttons.append(types.InlineKeyboardButton(text=text, callback_data=btn['callback_data']))
        new_markup.row(*buttons)

    if has_changes:
        try:
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=message.message_id, reply_markup=new_markup)
        except ApiTelegramException as e:
            if "message is not modified" not in str(e):
                raise e

@bot.message_handler(func=lambda m: m.text == 'Следующая тема ➡️')
def handle_next_topic(message):
    chat_id = message.chat.id
    state = user_states.get(chat_id)
    if not state:
        return

    if state['current_topic'] < len(state['topics']):
        topic = state['topics'][state['current_topic']]
        interests[topic] = user_choices[chat_id][topic]
    state['current_topic'] += 1

    if state['current_topic'] < len(state['topics']):
        bot.delete_message(chat_id, message.message_id)
        send_topic(chat_id)
    else:
        bot.send_message(chat_id, "✅ Выбор интересов завершен!", reply_markup=types.ReplyKeyboardRemove())
        get_location(message)



# Подтверждение регистрации

@bot.callback_query_handler(func=lambda call: call.data in ['confirm_yes', 'confirm_no'])
def handle_confirmation(call):
    bot.answer_callback_query(call.id)
    user = users[call.message.chat.id]
    if call.data == 'confirm_yes':
        user.register = True
        user.save()
        user.save_interests(user_choices[call.message.chat.id])
        bot.send_message(call.message.chat.id, "🎉 Регистрация завершена!")
        show_profile(call.message)
    else:
        bot.send_message(call.message.chat.id, "Давайте начнем заново!")
        start(call.message)

# Показ профиля

def show_profile(message):
    user = User.get(User.telegram_id == message.chat.id)
    if user and user.register:
        try:
            interests = user.get_themes_interests()
            with open(user.avatar, 'rb') as photo:
                bot.send_photo(
                    message.chat.id,
                    photo,
                    caption=f"👤 {user.name} {user.surname}, {user.city}\n🔞 Возраст: {user.age}\n🎯 Интересы:\n{interests}"
                )
        except Exception as e:
            bot.send_message(message.chat.id, f"Ошибка загрузки профиля: {str(e)}")
    else:
        bot.send_message(message.chat.id, "Профиль не найден. Начните с /start")

# Функция для удаления профиля

    
if __name__ == '__main__':
    bot.polling(none_stop=True)
