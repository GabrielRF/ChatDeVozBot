import configparser
from datetime import datetime
import logging.handlers
import msgs
import telebot
from telebot import types

config = configparser.ConfigParser()
config.read('chatdevozbot.conf')

TOKEN = config['CHATDEVOZBOT']['TOKEN']
ADMIN = ['creator', 'administrator']
COMMANDS = ['/iniciar', '/parar']

markup_talk = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_clean = types.ReplyKeyboardRemove(selective=False)

bot = telebot.TeleBot(TOKEN)

grupo = {}
usuario = {}

logger_info = logging.getLogger('InfoLogger')
logger_info.setLevel(logging.DEBUG)
handler_info = logging.handlers.TimedRotatingFileHandler(
    '/var/log/ChatDeVoz/chatdevoz.log', when='midnight', interval=1, backupCount=30, encoding='utf-8'
)
logger_info.addHandler(handler_info)

def log_text(message):
    logger_info.info(
        str(datetime.now()) +
        ' ' + str(message.chat.id) + ' \t' +
        str(message.message_id) + ' \t' + str(message.content_type)
    )

@bot.message_handler(commands=['iniciar'])
def bot_start(message):
    log_text(message)
    bot.send_chat_action(message.chat.id, 'typing')
    if message.chat.id < 0:
        status = bot.get_chat_member(message.chat.id, message.from_user.id).status
        if status in ADMIN:
            grupo[str(message.chat.id)] = str(message.from_user.id)
            try:
                #markup_talk.row(url="https://t.me/ChatDeVozBot?start=" + str(message.chat.id))
                talk_btn = types.InlineKeyboardMarkup()
                talk_btn.row(types.InlineKeyboardButton("✋", url="https://t.me/ChatDeVozBot?start=" + str(message.chat.id)))

                bot.send_message(message.from_user.id, msgs.start_admin, parse_mode='HTML')
                #bot.send_message(message.chat.id, '<b>Chat de voz iniciado!</b>\nQuer falar algo? Clique no botão ✋', parse_mode='HTML', reply_markup=markup_talk)
                msg = bot.send_message(message.chat.id, msgs.start_group, parse_mode='HTML', reply_markup=talk_btn)
                bot.pin_chat_message(message.chat.id, msg.message_id, disable_notification=True)
            except:
                bot.send_message(message.chat.id, msgs.start_user_unstarted, parse_mode='HTML')
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        bot.send_message(message.chat.id, msgs.start_bot_not_admin, parse_mode='HTML')

@bot.message_handler(commands=['parar'])
def bot_stop(message):
    log_text(message)
    bot.send_chat_action(message.chat.id, 'typing')
    try:
        if message.chat.id < 0:
            status = bot.get_chat_member(message.chat.id, message.from_user.id).status
            if status in ADMIN:
                bot.unpin_chat_message(message.chat.id)
                grupo[str(message.chat.id)] = None
                bot.send_message(message.chat.id, msgs.stop_group, parse_mode='HTML', reply_markup=markup_clean)
    except:
        pass
    bot.delete_message(message.chat.id, message.message_id)

@bot.message_handler(content_types=['voice'])
def get_voice_msg(message):
    log_text(message)
    bot.send_chat_action(message.chat.id, 'typing')
    try:
        msg = msgs.voice_forwarded.format(str(usuario[message.from_user.id]).replace('-100', ''))
        bot.forward_message(grupo[str(usuario[message.from_user.id])], message.chat.id, message.message_id)
        usuario[message.from_user.id] = None
        bot.reply_to(message, msg, parse_mode='HTML', disable_web_page_preview=True)
    except KeyError:
        bot.reply_to(message, msgs.voice_not_forwarded)

@bot.message_handler(commands=['start'])
def bot_start(message):
    log_text(message)
    bot.send_chat_action(message.chat.id, 'typing')
    if message.text.split('@')[0] in COMMANDS:
        return 0
    if '-100' in message.text:
        msg = bot.send_message(message.from_user.id, msgs.voice_start, parse_mode='HTML')
        usuario[message.from_user.id] = message.text.replace('/start ', '')
        bot.register_next_step_handler(msg, get_voice_msg)
    else:
        try:
            print(grupo[str(message.chat.id)])
        except:
            status = bot.get_chat_member(message.chat.id, message.from_user.id).status
            if message.chat.id < 0 and status in ADMIN:
                bot.reply_to(message, msgs.voice_not_started, parse_mode='HTML')
            elif message.chat.id < 0 and status not in ADMIN:
                bot.reply_to(message, msgs.voice_not_started_not_admin, parse_mode='HTML')
            else:
                bot.reply_to(message, msgs.start_user, parse_mode='HTML', disable_web_page_preview=True)
                bot.send_document(message.from_user.id, 'CgACAgEAAxkBAAPTYEexcA2G2cn6g2CdZS4MOVvm4ScAAhgBAAJhYUFGN48mu1WuJXMeBA')

bot.polling()
