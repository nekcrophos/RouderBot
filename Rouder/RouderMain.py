from telebot import types
import telebot

token = '7297525185:AAFreqpsv-UU88Lb9XfKwxgoVEfDwbdSJ_w'
botRouder = telebot.TeleBot(token);

class User():
    id = '';
    name = '';
    surname = '';
    age = 0;

user = User();
users = [];

intrRile = open('introduction.txt', 'r', encoding='utf-8')
preamFile = open('pream.txt', 'r', encoding='utf-8')

@botRouder.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        introduction = intrRile.read()
        botRouder.send_message(message.from_user.id, introduction)
        
        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes_indeed');
        keyboard.add(key_yes);
        key_no = types.InlineKeyboardButton(text = 'Нет', callback_data='no_imnot');
        keyboard.add(key_no);
        botRouder.send_message(message.from_user.id, reply_markup=keyboard, text=preamFile.read())
    else:
        botRouder.send_message(message.from_user.id, 'Напиши /start');

def refistration(message):
    user.id = message.from_user.id
    if message.text == '/reg':
        botRouder.send_message(message.from_user.id, "Как тебя зовут?");
        botRouder.register_next_step_handler(message, get_name); #следующий шаг – функция get_name
    else:
        botRouder.send_message(message.from_user.id, 'Напиши /reg');

def get_name(message): #получаем фамилию
    user.name = message.text;
    botRouder.send_message(message.from_user.id, 'Какая у тебя фамилия?');
    botRouder.register_next_step_handler(message, get_surname);

def get_surname(message):
    user.surname = message.text;
    botRouder.send_message(message.from_user.id,'Сколько тебе лет?');
    botRouder.register_next_step_handler(message, get_age);

def get_age(message):
    while user.age == 0: #проверяем что возраст изменился
        try:
             user.age = int(message.text) #проверяем, что возраст введен корректно
        except Exception:
             botRouder.send_message(message.from_user.id, 'Цифрами, пожалуйста');

        if (user.age < 18):
            botRouder.send_message(message.from_user.id, 'Ваш возраст не соответвствует соглашению нашего бота')
            return
        
        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes');
        keyboard.add(key_yes);
        key_no = types.InlineKeyboardButton(text = 'Нет', callback_data='no');
        keyboard.add(key_no);

        question = 'Тебе '+str(user.age)+' лет, тебя зовут '+user.name+' '+ user.surname + '?';

        botRouder.send_message(message.from_user.id, text=question, reply_markup=keyboard);

@botRouder.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes": #call.data это callback_data, которую мы указали при объявлении кнопки
        users.append(user) #код сохранения данных, или их обработки
        botRouder.send_message(call.message.chat.id, 'Запомню : )');
        return;
    elif call.data == "no":
        ... #переспрашиваем
        botRouder.send_message(call.message.chat.id, 'Попрубуй ещё раз')
        return;

botRouder.polling(none_stop=True, interval=0)