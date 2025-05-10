from handlers import introductionHandler

def run(bot):
    @bot.callback_query_handler(func=lambda call: call.data in ['confirm_yes', 'confirm_no'])
    def handle_confirmation(call):
        user = users.get(call.message.chat.id)
        if call.data == 'confirm_yes':
            bot.send_message(call.message.chat.id, "Отлично! Регистрация завершена!")
            bot.answer_callback_query(call.id)
            # Здесь можно сохранить пользователя в БД
        else:
            bot.send_message(call.message.chat.id, "Давайте начнем заново!")
            msg = bot.send_message(call.message.chat.id, "Как тебя зовут?")
            bot.register_next_step_handler(msg, get_name)