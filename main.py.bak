from telegram import Update
from telegram.ext import Updater
from  telegram.ext import CommandHandler 
from  telegram.ext import MessageHandler 
from  telegram.ext import Filters
from telegram.ext import CallbackContext
import redis
import logging
import time,requests
from apscheduler.schedulers.background import BackgroundScheduler
schedulers = BackgroundScheduler()
TOKEN='5729870657:AAGpDBrS5mHVyAyMpzp_zKGogVyRQRKd4W0'
r=redis.from_url('redis://:p6276f73643cd377844153100d0c88f2a3b5d6b23c8b20ae56c48c8cbe6638c3b@ec2-3-217-237-190.compute-1.amazonaws.com:16889')
db_keys=r.keys(pattern='*')


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def once():
    for keys in db_keys:
        id=r.get(keys).decode("UTF-8")
        message='Hola recuerda pagarnos tu cuota'
        send_text='https://api.telegram.org/bot'+TOKEN+'/sendMessage?chat_id='+id+'&text='+message
        response=requests.get(send_text)
        print(response.json())
        time.sleep(1)
def notify(update:Update, context:CallbackContext) -> None:
    schedulers.add_job(once, 'cron', hour='18', minute='29')
    schedulers.start()
    update.message.reply_text(f"Hola te voy notificar cada semana que te pague tu cuota")
    #obtener la respuesta del usuario y guardar en una variable



def start(update, context):
    user_id=update.message.from_user.id
    user_name=update.message.from_user.name
    print(user_id)
    print(user_name)
    r.set(user_name,user_id)
    
    message='Hola '+user_name+'\n'+'Bienvenido a la plataforma haz quedado registrado'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)



def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def main():
    updater=Updater(TOKEN, use_context=True)
    dispatcher=updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))
    dispatcher.add_handler(CommandHandler('notify', notify))
    updater.start_polling()
    updater.idle()
if __name__ == '__main__':
    
    main()


