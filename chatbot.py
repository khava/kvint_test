import os

from telegram.ext import (
    CommandHandler,
    Filters,
    MessageHandler,
    Updater
)

from utils import ChatBot

PORT = int(os.environ.get('PORT', '8443'))
TELEGRAM_TOKEN = '5047769126:AAHK6j55fnPqi64-xNQWEJhDQ76OhQXLa48' # !!! Замените на свой
APP_NAME = 'https://chatbot-kvint.herokuapp.com/'

chatbot = ChatBot()

def start(update, context):
    chatbot.start()
    update.message.reply_text('👋🏻')
    update.message.reply_text('Какую вы хотите пиццу 🍕? Большую или маленькую?')


def stop(update, context):
    chatbot.stop()
    update.message.reply_text('Для того, чтобы сделать заказ введите команду /start')


def conversation(update, context):
    message = update.message.text.lower()

    if chatbot.state == 'get pizza size':
        if message == 'большую' or message == 'маленькую':
            chatbot.size = message
            chatbot.get_payment_method()
            update.message.reply_text('Как вы будете платить? Наличкой 💵 или картой 💳?')
        else:
            update.message.reply_text('Пожалуйста, выберите размер пиццы!')

    elif chatbot.state == 'get payment method':
        if message == 'наличкой' or message == 'картой':
            chatbot.payment = message
            chatbot.make_order()
            update.message.reply_text(f'Вы хотите {chatbot.size} пиццу, оплата - {chatbot.payment}?')
        else:
            update.message.reply_text('Пожалуйста, выберите способ оплаты!')

    elif chatbot.state == 'make an order':
        if message == 'да':
            chatbot.end_order()
            update.message.reply_text('Спасибо за заказ 😊!')
            update.message.reply_text('Для нового заказа введите команду /start')
        elif message == 'нет':
            chatbot.end_order()
            update.message.reply_text('Для того, чтобы сделать заказ введите команду /start')
        else:
            update.message.reply_text('Необходимо подтвердить или отменить заказ, если вы передумали делать заказ, пожалуйста, оставите бота командой /stop')
            update.message.reply_text(f'Вы хотите {chatbot.size} пиццу, оплата - {chatbot.payment}?')


if __name__ == '__main__':
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('stop', stop))
    dp.add_handler(MessageHandler(Filters.text, conversation))

    updater.start_polling()

    # For deploy on heroku
    # updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TELEGRAM_TOKEN, webhook_url=APP_NAME + TELEGRAM_TOKEN)
    updater.idle()
