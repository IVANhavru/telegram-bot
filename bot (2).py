
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

# Етапи розмови
NAME, VEHICLE, CARGO, DATE, ROUTE = range(5)

# Команда старту
def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Вітаю! Введіть ім'я перевізника:")
    return NAME

# Обробка імені
def name(update: Update, context: CallbackContext) -> int:
    context.user_data['name'] = update.message.text
    update.message.reply_text("Введіть номер транспортного засобу:")
    return VEHICLE

# Обробка номера транспорту
def vehicle(update: Update, context: CallbackContext) -> int:
    context.user_data['vehicle'] = update.message.text
    update.message.reply_text("Введіть тип вантажу:")
    return CARGO

# Обробка вантажу
def cargo(update: Update, context: CallbackContext) -> int:
    context.user_data['cargo'] = update.message.text
    update.message.reply_text("Введіть дату і час відправлення (наприклад, 2025-01-26 14:00):")
    return DATE

# Обробка дати
def date(update: Update, context: CallbackContext) -> int:
    context.user_data['date'] = update.message.text
    update.message.reply_text("Введіть маршрут (звідки і куди):")
    return ROUTE

# Обробка маршруту
def route(update: Update, context: CallbackContext) -> int:
    context.user_data['route'] = update.message.text
    summary = f"""
Наряд створено:
Ім'я: {context.user_data['name']}
Транспорт: {context.user_data['vehicle']}
Вантаж: {context.user_data['cargo']}
Дата: {context.user_data['date']}
Маршрут: {context.user_data['route']}
    """
    update.message.reply_text(summary)
    return ConversationHandler.END

# Скасування
def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Операцію скасовано.")
    return ConversationHandler.END

# Основна функція
def main():
    # Вставте ваш API-токен тут
    updater = Updater("ВАШ_API_TOKEN", use_context=True)
    dispatcher = updater.dispatcher

    # Діалог
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, name)],
            VEHICLE: [MessageHandler(Filters.text & ~Filters.command, vehicle)],
            CARGO: [MessageHandler(Filters.text & ~Filters.command, cargo)],
            DATE: [MessageHandler(Filters.text & ~Filters.command, date)],
            ROUTE: [MessageHandler(Filters.text & ~Filters.command, route)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
