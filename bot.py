
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

# Стадії розмови
NAME, VEHICLE, CARGO, DATE, ROUTE = range(5)

# Стартова команда
def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Вітаю! Введіть ім'я перевізника:")
    return NAME

# Збір інформації
def name(update: Update, context: CallbackContext) -> int:
    context.user_data['name'] = update.message.text
    update.message.reply_text("Введіть номер транспортного засобу:")
    return VEHICLE

def vehicle(update: Update, context: CallbackContext) -> int:
    context.user_data['vehicle'] = update.message.text
    update.message.reply_text("Введіть тип вантажу:")
    return CARGO

def cargo(update: Update, context: CallbackContext) -> int:
    context.user_data['cargo'] = update.message.text
    update.message.reply_text("Введіть дату та час відправлення (наприклад, 2025-01-25 14:00):")
    return DATE

def date(update: Update, context: CallbackContext) -> int:
    context.user_data['date'] = update.message.text
    update.message.reply_text("Введіть маршрут (звідки і куди):")
    return ROUTE

def route(update: Update, context: CallbackContext) -> int:
    context.user_data['route'] = update.message.text
    # Підтвердження даних
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

def main():
    updater = Updater("ВАШ_API_TOKEN", use_context=True)  # Замінити на реальний токен
    dispatcher = updater.dispatcher

    # Розмова
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

if name == '__main__':
    main()