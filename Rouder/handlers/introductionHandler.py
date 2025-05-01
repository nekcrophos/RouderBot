def run(bot):
    @bot.callback_query_handler(func=lambda call: call.data in ['yes_indeed', 'no_imnot'])
    def handle_introduction(call):
        if call.data == 'yes_indeed':
            msg = bot.send_message(call.message.chat.id, "Как тебя зовут?")
            bot.register_next_step_handler(msg, get_name)
        else:
            bot.send_message(call.message.chat.id, "Жаль, возвращайся когда будешь готов!")

    def get_name(message):
        user = User()
        user.id = message.chat.id
        user.name = message.text
        users[message.chat.id] = user
        
        msg = bot.send_message(message.chat.id, "Какая у тебя фамилия?")
        bot.register_next_step_handler(msg, get_surname)

    def get_surname(message):
        user = users.get(message.chat.id)
        if user:
            user.surname = message.text
            msg = bot.send_message(message.chat.id, "Сколько тебе лет?")
            bot.register_next_step_handler(msg, get_age)

    def get_age(message):
        user = users.get(message.chat.id)
        if user:
            try:
                age = int(message.text)
                if age < 18:
                    bot.send_message(message.chat.id, "Вам должно быть больше 18 лет!")
                    return
                user.age = age
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