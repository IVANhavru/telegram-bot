
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Привіт! Я ваш Telegram-бот.")

def main():
    # Токен вашого бота
    updater = Updater("8154487693:AAGRNTAg9sWETGmbBDCQYbhWGFVSHzpZE9U", use_context=True)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
