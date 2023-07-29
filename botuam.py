
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, MessageHandler, CommandHandler, CallbackQueryHandler, ConversationHandler, CallbackContext
import redis,time,requests,logging
from apscheduler.schedulers.background import BackgroundScheduler
schedulers = BackgroundScheduler()
TOKEN = "TOKEN"
QUESTION, NO,MENU_ALUMNO,RECORDAR,CALENDARIO,UAM,SISTEMAS,COMBI,PROFESOR= range(9)
r=redis.from_url('TOKEN')
db_keys=r.keys(pattern="*")

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
    schedulers.add_job(once, 'cron', hour='20', minute='36')
    schedulers.start()
    update.message.reply_text(f"Hola te voy notificar cada semana que te pague tu cuota")
def notify_off(update: Update, context: CallbackContext) -> None:
    #aqui se pausa el scheduler
    schedulers.pause()
    update.message.reply_text(f"Te dejare de notificar")
def question(update: Update, context: CallbackContext) -> None:

    buttons = [[
        InlineKeyboardButton("Si", callback_data = "si")
    ],
    [        
        InlineKeyboardButton("No",  callback_data="no")
    ]]

    keyboardMarkup = InlineKeyboardMarkup(buttons)

    update.message.reply_text("Bievenido al chat bot de uam lerma UAM eres alumno?", reply_markup=keyboardMarkup)

    return QUESTION

def si(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    buttons = [[
        InlineKeyboardButton("Recordatorio", callback_data = "recordar")
    ],
    [        
        InlineKeyboardButton("Calendario",  callback_data="calendario")
    ],
        [
        InlineKeyboardButton("UAM Lerma",  callback_data="uam")
        ]
    ,[
        InlineKeyboardButton("Ayuda",  callback_data="help")
    ],[
        InlineKeyboardButton("Salir",  callback_data="salir")
    ]
    
    ]

    keyboardMarkup = InlineKeyboardMarkup(buttons)

    query.edit_message_text(f"selecciona una opcion, registrate usando el comando /register", reply_markup=keyboardMarkup)

    return MENU_ALUMNO

def register(update, context):
    user_id=update.message.chat_id
    user_name=update.message.chat.username
    r.set(user_name,user_id)
    update.message.reply_text(f"Te has registrado correctamente")


def no(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    buttons = [[
        InlineKeyboardButton("Mal explicado", callback_data = "mal"),
        InlineKeyboardButton("Poco contenido",  callback_data="poco")
    ],
    [        
        InlineKeyboardButton("Otro motivo",  callback_data="otro")
    ]]

    keyboardMarkup = InlineKeyboardMarkup(buttons)

    query.edit_message_text(f"Oh, lo siento!. ¿Cúal es la razón?", reply_markup=keyboardMarkup)

    return NO

def razon(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(f"Gracias por responder.")

    return ConversationHandler.END

def recordar(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    buttons = [[
        InlineKeyboardButton("Atras",  callback_data="atras")
    ]
    ]
    keyboardMarkup = InlineKeyboardMarkup(buttons)
    query.edit_message_text(f"Para activar notifaciones usar /notify y para desactivar usar /notify_off", reply_markup=keyboardMarkup)
    return RECORDAR


def calendario(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    buttons = [[
        InlineKeyboardButton("Atras", callback_data = "atras")
    ]]
    keyboardMarkup = InlineKeyboardMarkup(buttons)
    query.edit_message_text(f"Este es el calendario de la UAM https://www.uam.mx/calendario/", reply_markup=keyboardMarkup)
    return CALENDARIO
def help(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(f"help")
    return MENU_ALUMNO
def uam(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    buttons = [[
        InlineKeyboardButton("Sistemas Escolares", callback_data = "sistemas"),
    ],
    [   
        InlineKeyboardButton("Horario de combi", callback_data = "combi")
    ],
    [   
        InlineKeyboardButton("Conoce a tu profesor", callback_data = "profesor")
    ],
    [   
        InlineKeyboardButton("Atras", callback_data = "atras")
    ]
        
    ]
    keyboardMarkup = InlineKeyboardMarkup(buttons)
    query.edit_message_text(f"selecciona una opcion", reply_markup=keyboardMarkup)
    return UAM
def sistemas(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    buttons = [[
        InlineKeyboardButton("Atras", callback_data = "atras_secundario")
    ]]
    keyboardMarkup = InlineKeyboardMarkup(buttons)
    query.edit_message_text(f"Este es el link de Sistemas escolares de la UAM Lerma http://www.ler.uam.mx/es/UAML/coordSistemasEscolares", reply_markup=keyboardMarkup)
    return SISTEMAS
def combi(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    buttons = [[
        InlineKeyboardButton("Atras", callback_data = "atras_secundario")
    ]]
    keyboardMarkup = InlineKeyboardMarkup(buttons)
    query.edit_message_text(f"Este es el link de Horario de combi de la UAM Lerma http://www.ler.uam.mx/es/UAML/transporte", reply_markup=keyboardMarkup)
    return COMBI
def profesor(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    buttons = [[
        InlineKeyboardButton("Atras", callback_data = "atras_secundario")
    ]]
    keyboardMarkup = InlineKeyboardMarkup(buttons)
    query.edit_message_text(f"Conoce a tus profesores de la UAM Lerma  https://www.misprofesores.com/escuelas/UAM-Lerma_3127 , https://www.misprofesores.com/escuelas/Psicologia-Biomedica-UAM-Lerma_9999", reply_markup=keyboardMarkup)
    return PROFESOR
def atras_secundario(update: Update, context: CallbackContext) -> None:
    return uam(update, context)
def atras(update: Update, context: CallbackContext) -> None:
    return si(update, context)
def salir(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(f"gracias por usar el bot")
    return ConversationHandler.END

def main() -> None:
    """Start the bot."""
    # Creamos Updater y le pasamos el token
    updater = Updater(TOKEN)

    # Obtenemos el dispatcher para registrar los handlers
    dispatcher = updater.dispatcher

    # Handlers
    entry_points = [CommandHandler("start", question)]
    states = {
        QUESTION:[
            CallbackQueryHandler(si, pattern=r'^si$'),
            CallbackQueryHandler(no, pattern=r'^no$')
        ],
        NO:[
            CallbackQueryHandler(razon)
        ],
        MENU_ALUMNO:[
            CallbackQueryHandler(recordar, pattern=r'^recordar$'),
            CallbackQueryHandler(calendario, pattern=r'^calendario$'),
            CallbackQueryHandler(uam, pattern=r'^uam$'),
            CallbackQueryHandler(help, pattern=r'^help$'),
            CallbackQueryHandler(salir, pattern=r'^salir$')
        ],
            RECORDAR:[

                CallbackQueryHandler(atras)
            ],

            CALENDARIO:[
                CallbackQueryHandler(atras)
            ],
            UAM:[ 
                CallbackQueryHandler(sistemas, pattern=r'^sistemas$'),
                CallbackQueryHandler(combi, pattern=r'^combi$'),
                CallbackQueryHandler(profesor, pattern=r'^profesor$'),
                CallbackQueryHandler(atras)
            ],
                SISTEMAS:[
                    CallbackQueryHandler(atras_secundario)
                ],
                COMBI:[
                    CallbackQueryHandler(atras_secundario)
                ],PROFESOR:[
                    CallbackQueryHandler(atras_secundario)
                ],

    }
    fallbacks = []

    dispatcher.add_handler(ConversationHandler(entry_points, states, fallbacks))
    dispatcher.add_handler(CommandHandler("notify", notify))
    ##desactivar notify
    dispatcher.add_handler(CommandHandler("notify_off", notify_off))
    #registramos el usario
    dispatcher.add_handler(CommandHandler("register", register))

    # Iniciar el bot
    updater.start_polling()

    #Mantener el proceso hasta que se pulse Ctrl + C
    updater.idle()


if __name__ == '__main__':
    main()