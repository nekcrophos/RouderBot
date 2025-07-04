from collections import Counter
from itertools import count
from telebot import types
import telebot
import os
from dotenv import load_dotenv
from telebot.apihelper import ApiTelegramException
from geopy.geocoders import Nominatim 

import sys
sys.path.insert(1, 'Rouder\models')
sys.path.insert(1, 'Rouder\database')
from models.user import User
from models.interest import Interest
from models.theme import Theme
from models.city import City
from models.feedback import Feedback


load_dotenv()
token = os.getenv("TOKEN")
bot = telebot.TeleBot(token, threaded=True)

geolocator = Nominatim(user_agent="my_geopy_app")
global interests
interests = {'music': [], 'place': [], 'actives': [], 'pop_culter': [], 'lifestyle': []}
global users
users = {}
search_sessions = {}
# Настройка команд бота
commStart = types.BotCommand(command='/start', description='Начать бота')
commHelp = types.BotCommand(command='/help', description='Помощь в использовании бота')
commMyProf = types.BotCommand(command='/my_profile', description='Мой профиль')
commChangeProf = types.BotCommand(command='/change_profile', description='Изменить профиль')
commSearch = types.BotCommand(command='/search', description='Поиск партнеров')
bot.set_my_commands([commStart, commHelp, commMyProf, commChangeProf, commSearch])

# Загрузка текстов
with open('Rouder\\introduction.txt', 'r', encoding='utf-8') as f:
    introduction = f.read()
with open('Rouder\\pream.txt', 'r', encoding='utf-8') as f:
    preamble = f.read()

# Состояния пользователей
user_states = {}
user_choices = {}


@bot.message_handler(commands=['help'])
def help_handler(message):
    text = (
        "ℹ️ <b>Справка по боту</b>\n\n"
        "• /start — начать регистрацию или перезапустить бота\n"
        "• /help — показать это сообщение\n"
        "• /my_profile — посмотреть свой профиль\n"
        "• /change_profile — удалить текущий профиль и начать заново\n"
        "• /search — найти партнёров по вашим критериям\n\n"
        "<b>Как это работает:</b>\n"
        "1️⃣ При /start вы вводите имя, фамилию и отправляете фото.\n"
        "2️⃣ Выбираете свои интересы в 5 категориях.\n"
        "3️⃣ Указываете половые предпочтения и локацию.\n"
        "4️⃣ В /search бот предложит вам кандидатов (лайк/дизлайк).\n"
        "5️⃣ При взаимном лайке вы получите уведомление о совпадении.\n\n"
        "⚠️ <i>Имя и фамилия — только буквами, фото — обязательно как изображение.</i>"
    )
    bot.send_message(message.chat.id, text, parse_mode='HTML')


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
    user = users.get(message.chat.id)
    if user:
        show_profile(message)
    else:
        bot.send_message(message.chat.id, "Вы ещё не зарегистрированы. Для регистрации введите команду /start.")
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

    if message.text and message.text.isalpha():
        user.name = message.text
        msg = bot.send_message(message.chat.id, "Какая у тебя фамилия?")
        bot.register_next_step_handler(msg, get_surname)
    else:
        msg = bot.send_message(
            message.chat.id,
            "❌ Имя может состоять только из букв. Пожалуйста, введите ваше имя еще раз текстом."
        )
        bot.register_next_step_handler(msg, get_name)

def get_surname(message):
    user = users[message.chat.id]
    if user:
        if message.text and message.text.isalpha():
            user.surname = message.text
            msg = bot.send_message(message.chat.id, "Отправь свою аватарку")
            bot.register_next_step_handler(msg, get_avatar)
        else:
            msg = bot.send_message(message.chat.id, "❌ Фамилия может состоять только из букв. Пожалуйста, введите вашу фамилию еще раз.")
            bot.register_next_step_handler(msg, get_surname)
            

def get_avatar(message):
    user = users.get(message.chat.id)
    if not user:
        return

    # Если пришла фотография — сохраняем
    if message.photo:
        photo = message.photo[-1]
        file_info = bot.get_file(photo.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        save_path = f"Rouder\\avatars\\{message.chat.id}_user_avatar.{file_info.file_path.split('.')[-1]}"
        with open(save_path, 'wb') as new_avatar:
            new_avatar.write(downloaded_file)
        user.avatar = save_path
        start_interest_selection(message)
        return

    # Если пришёл документ или текст — ругаемся и просим фото снова
    bot.send_message(
        message.chat.id,
        "❌ Это не фотография. Пожалуйста, отправьте именно изображение (через кнопку «Прикрепить фото»)."
    )
    # ждем следующего шага снова в этой же функции
    bot.register_next_step_handler(message, get_avatar)

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

# пердпочтение в компании мужская или женская
def handle_gender_selection(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Мужской', callback_data='gender_male'), types.InlineKeyboardButton('Женский', callback_data='gender_female'),
                 types.InlineKeyboardButton('Не важно', callback_data='gender_unspecified'))
    bot.send_message(chat_id=message.chat.id, text="Какой пол ты предпочитаешь в компании?", reply_markup=keyboard)
    markup_gender = types.InlineKeyboardMarkup()
    markup_gender.add(types.InlineKeyboardButton("Мужской", callback_data='male'), types.InlineKeyboardButton("Женский", callback_data='female'))
    bot.send_message(chat_id=message.chat.id, text="Какого ты сам пола?", reply_markup=markup_gender)
    
        
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
    city_id = City.get_id(city)
    user.city = city_id
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
        handle_gender_selection(message)



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
                    caption=f"👤 {user.name} {user.surname}, {user.city.name}\n Пол: {user.gender} \n🔞 Возраст: {user.age}\n🎯 Интересы:\n{interests}"
                )
        except Exception as e:
            bot.send_message(message.chat.id, f"Ошибка загрузки профиля: {str(e)}")
    else:
        bot.send_message(message.chat.id, "Профиль не найден. Начните с /start")

# Функция для удаления профиля
@bot.message_handler(commands=['change_profile'])
def change_profile(message):
    user = User.get(User.telegram_id == message.chat.id)
    if user:
        user.delete_instance()
        bot.send_message(message.chat.id, "Профиль успешно удален. Вы можете начать заново с /start")
    else:
        bot.send_message(message.chat.id, "Профиль не найден. Начните с /start")


@bot.message_handler(commands=['search'])
def search(message):
    me = User.get_or_none(User.telegram_id == message.chat.id)
    if not me or not me.register:
        bot.send_message(message.chat.id, "❌ Вы не зарегистрированы. Сначала зарегистрируйтесь!")
        return

    # Мои интересы
    my_ids = list(map(lambda x: x.id, me.get_interests()))

    # Диапазон возраста
    min_age = max(18, me.age - 2)
    max_age = me.age + 2

    # Начальная выборка
    candidates = User.select().where(
        (User.id != me.id) &
        (User.register == True) &
        (User.age.between(min_age, max_age))
    )

    # 🔹 Добавим фильтрацию по полу компании
    if me.gender_pred == 'male_company':
        candidates = candidates.where(User.gender == 'male')
    elif me.gender_pred == 'female_company':
        candidates = candidates.where(User.gender == 'female')
    # Если 'any', не фильтруем по полу

    # Считаем совпадения
    scored = []
    for u in candidates:
        same_city = (u.city_id == me.city_id)
        age_diff   = abs(u.age - me.age)
        their_ids  = list(map(lambda x: x.id, u.get_interests()))
        common     = sum(i[0] == i[1] for i in zip(my_ids, their_ids))
        scored.append((u.id, same_city, age_diff, common))

    scored.sort(key=lambda x: (not x[1], x[2], -x[3]))

    if not scored:
        return bot.send_message(message.chat.id, "Никого не найдено")

    candidate_ids = [item[0] for item in scored]
    search_sessions[message.chat.id] = {
        'ids': candidate_ids,
        'idx': 0
    }

    show_candidate(message.chat.id)



def show_candidate(chat_id):
    sess = search_sessions.get(chat_id)
    if not sess:
        return

    idx = sess['idx']
    if idx >= len(sess['ids']):
        return bot.send_message(chat_id, "Показаны все варианты!")

    # Загружаем пользователя по ID «на лету»
    u = User.get_by_id(sess['ids'][idx])

    # (Можно заново пересчитать same_city, common и т.д. если нужны в подписи;
    #  здесь для простоты покажем только базовую инфу)
    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton("❤️ Лайк", callback_data='like'),
        types.InlineKeyboardButton("💔 Дизлайк", callback_data='dislike')
    )

    caption = f"👤 {u.name} {u.surname}, {u.city.name}\n Пол: {u.gender} \n🔞 {u.age} лет\nИнтересы:{u.get_themes_interests()}"

    try:
        with open(u.avatar, 'rb') as ph:
            bot.send_photo(chat_id, ph, caption=caption, reply_markup=kb)
    except:
        bot.send_message(chat_id, caption, reply_markup=kb)


@bot.callback_query_handler(func=lambda c: c.data in ['like', 'dislike'])
def on_feedback(call):
    chat_id = call.message.chat.id
    me = User.get(User.telegram_id == chat_id)
    sess = search_sessions.get(chat_id)
    if not sess:
        return bot.answer_callback_query(call.id, "Сессия не найдена.")

    idx = sess['idx']
    target_id = sess['ids'][idx]

    # Сохраняем реакцию
    liked = (call.data == 'like')
    Feedback.create(from_id=me.id, to_id=target_id, like=liked)

    # Если это лайк, проверяем, не лайкнул ли target нас раньше
    if liked:
        mutual = Feedback.get_or_none(
            (Feedback.from_id == target_id) &
            (Feedback.to_id == me.id) &
            (Feedback.like == True)
        )
        if mutual:
            # у нас совпадение!
            notify_match(me.id,      target_id)
            notify_match(target_id,  me.id)

    sess['idx'] += 1
    bot.answer_callback_query(call.id, "Принято!")
    try:
        bot.delete_message(chat_id, call.message.message_id)
    except:
        pass

    show_candidate(chat_id)


def notify_match(user_id, other_id):
    """Шлёт пользователю user_id уведомление о матче с other_id."""
    u = User.get_by_id(user_id)
    other = User.get_by_id(other_id)

    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton("Показать профиль", callback_data=f"show_match_{other_id}"),
        types.InlineKeyboardButton("Нет, позже",      callback_data="ignore_match")
    )
    bot.send_message(
        u.telegram_id,
        f"🎉 У вас взаимный лайк с @{get_username(other.telegram_id)}!",
        reply_markup=kb
    )


@bot.callback_query_handler(func=lambda c: c.data.startswith('show_match_'))
def on_show_match(call):
    # Парсим ID партнёра из callback_data
    other_id = int(call.data.split('_')[-1])
    you = User.get(User.telegram_id == call.message.chat.id)
    other = User.get_by_id(other_id)

    # Формируем подпись с Telegram-username для связи
    username = get_username(other.telegram_id)
    caption = (
        f"👤 {other.name} {other.surname} (@{username})\n"
        f"🌆 Город: {other.city.name}\n"
        f"🔞 Возраст: {other.age}\n"
        f"🎯 Интересы:\n"
        f"{other.get_themes_interests()}\n\n"
        f"Пиши @${username}, чтобы познакомиться!"
    )
    try:
        with open(other.avatar, 'rb') as ph:
            bot.send_photo(call.message.chat.id, ph, caption=caption)
    except:
        bot.send_message(call.message.chat.id, caption)

    bot.answer_callback_query(call.id)
    # Удалим уведомление о матче, чтобы не мешалось
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass


@bot.callback_query_handler(func=lambda c: c.data == 'ignore_match')
def on_ignore_match(call):
    # Просто удаляем notification
    bot.answer_callback_query(call.id, "Ок, позже напомню")
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass

def get_username(telegram_id: int) -> str:
    """Пытаемся достать Telegram-username через get_chat.
       Если нет — вернём telegram_id."""
    try:
        member = bot.get_chat(telegram_id)
        return member.username or str(telegram_id)
    except:
        return str(telegram_id)

@bot.callback_query_handler(func=lambda c: c.data in ['gender_male', 'gender_female', 'gender_unspecified'])
def set_gender(call):
    user =  users[call.message.chat.id]
    if call.data == 'gender_male':
        user.gender_pred = 'male_company'
        bot.send_message(call.message.chat.id, f"Предпочтение в анкетах установлено: мужская компания")
    elif call.data == 'gender_female':
        user.gender_pred = 'female_company'
        bot.send_message(call.message.chat.id, f"Предпочтение в анкетах установлено: женская компания")
    elif call.data == 'gender_unspecified':
        user.gender_pred = 'unspecified'
        bot.send_message(call.message.chat.id, f"Предпочтение в анкетах установлено: любая компания")


@bot.callback_query_handler(func=lambda c: c.data in ['male', 'female'])
def on_gender(call):
    user =  users[call.message.chat.id]
    if call.data == 'male':
        user.gender = 'male'
        bot.send_message(call.message.chat.id, f"Пол установлен: мужской")
    elif call.data == 'female':
        user.gender = 'female'
        bot.send_message(call.message.chat.id, f"Пол установлен: женский")
    msg = bot.send_message(call.message.chat.id, "Следующий шаг геолокация: ")
    get_location(msg)

if __name__ == '__main__':
    bot.polling(none_stop=True, skip_pending=True)
