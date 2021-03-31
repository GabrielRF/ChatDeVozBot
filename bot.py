import configparser
from datetime import datetime
import logging.handlers
import msgs
import sqlite3
import telebot
import time
from telebot import types

config = configparser.ConfigParser()
config.read('chatdevozbot.conf')

TOKEN = config['CHATDEVOZBOT']['TOKEN']
ADMIN = ['creator', 'administrator']
COMMANDS = ['/iniciar', '/parar']
db = 'ChatDeVoz'
table = 'ChatDeVoz'

bot = telebot.TeleBot(TOKEN)

usuario = {}

logger_info = logging.getLogger('InfoLogger')
logger_info.setLevel(logging.DEBUG)
handler_info = logging.handlers.TimedRotatingFileHandler(
    '/var/log/ChatDeVoz/chatdevoz.log', when='midnight', interval=1, backupCount=30, encoding='utf-8'
)
logger_info.addHandler(handler_info)

markup_btn = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_btn.row('/Participar')
markup_clean = types.ReplyKeyboardRemove(selective=False)

def create_group_table(groupid):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    aux = ('''CREATE TABLE {} (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        userid TEXT);
    ''').format(groupid)
    cursor.execute(aux)

def select_info(table, col, arg):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    aux = ('''SELECT * FROM {} WHERE
       {} ="{}"''').format(table, col, arg)
    cursor.execute(aux)
    data = cursor.fetchone()
    conn.close()
    return data

def select_all(table):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    aux = ('''SELECT userid FROM {}''').format(table)
    cursor.execute(aux)
    data = cursor.fetchall()
    conn.close()
    return data

def add_group(groupid, adminid, pinid):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    aux = ('''INSERT INTO {} (groupid, adminid, pinid)
        VALUES ('{}', '{}', '{}')''').format(table, groupid, adminid, pinid)
    cursor.execute(aux)
    conn.commit()
    conn.close()

def add_sub(groupid, userid):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    aux = ('''INSERT INTO g{} (userid)
        VALUES ('{}')''').format((groupid*-1), userid)
    cursor.execute(aux)
    conn.commit()
    conn.close()

def del_sub(groupid, userid):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    aux = ('''DELETE FROM g{}
        WHERE userid = {}''').format((groupid*-1), userid)
    cursor.execute(aux)
    conn.commit()
    conn.close()

def del_group(groupid):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    aux = ('''DELETE FROM {}
        WHERE groupid = {}''').format(table, groupid)
    cursor.execute(aux)
    conn.commit()
    conn.close()

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
        group = select_info('ChatDeVoz', 'groupid', message.chat.id)
        print(group)
        if status in ADMIN:
            try:
                bot.send_message(message.from_user.id, msgs.start_admin, parse_mode='HTML')
                msg = bot.send_message(message.chat.id, msgs.start_group, parse_mode='HTML', reply_markup=markup_btn)
                if not group:
                    bot.pin_chat_message(message.chat.id, msg.message_id, disable_notification=True)
                    add_group(message.chat.id, message.from_user.id, msg.message_id)
                else:
                    del_group(group[1])
                    add_group(message.chat.id, message.from_user.id, group[3])
            except:
                bot.send_message(message.chat.id, msgs.start_user_unstarted, parse_mode='HTML')
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        # bot.send_message(message.chat.id, msgs.start_bot_not_admin, parse_mode='HTML')
        pass

@bot.message_handler(commands=['Participar'])
def bot_start(message):
    try:
        msg = bot.send_message(message.from_user.id, msgs.voice_start, parse_mode='HTML')
        usuario[message.from_user.id] = message.chat.id
    except:
        group = select_info('ChatDeVoz', 'groupid', message.chat.id)
        print(group)
        if group:
            msg = bot.send_message(message.chat.id, msgs.voice_group_send.format(message.from_user.id, message.chat.id), parse_mode='HTML', disable_web_page_preview=True)
            try:
                bot.delete_message(message.chat.id, group[2])
            except:
                pass
        else:
            bot.send_message(message.chat.id, msgs.voice_not_started_not_admin.format(message.from_user.id), parse_mode='HTML', disable_web_page_preview=True)
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

@bot.message_handler(commands=['parar'])
def bot_stop(message):
    log_text(message)
    bot.send_chat_action(message.chat.id, 'typing')
    try:
        if message.chat.id < 0:
            status = bot.get_chat_member(message.chat.id, message.from_user.id).status
            if status in ADMIN:
                group = select_info('ChatDeVoz', 'groupid', message.chat.id)
                del_group(group[1])
                bot.send_message(message.chat.id, msgs.stop_group, parse_mode='HTML', reply_markup=markup_clean)
                bot.unpin_chat_message(message.chat.id, message_id=group[3])
    except:
        pass
    bot.delete_message(message.chat.id, message.message_id)

@bot.message_handler(content_types=['voice', 'video_note'])
def get_voice_msg(message):
    if message.chat.id < 0:
        return 0
    log_text(message)
    bot.send_chat_action(message.chat.id, 'typing')
    try:
        group = select_info('ChatDeVoz', 'groupid', str(usuario[message.from_user.id]))
        print(group)
        msg = msgs.voice_forwarded.format(
            str(usuario[message.from_user.id]).replace('-100', ''),
            group[2]
        )
        bot.forward_message(group[2], message.chat.id, message.message_id)
        usuario[message.from_user.id] = None
        bot.reply_to(message, msg, parse_mode='HTML', disable_web_page_preview=True)
    except:
        bot.reply_to(message, msgs.voice_not_forwarded, parse_mode='HTML')

@bot.message_handler(commands=['start'])
def bot_start(message):
    log_text(message)
    bot.send_chat_action(message.chat.id, 'typing')
    if message.text.split('@')[0] in COMMANDS:
        return 0
    if '-100' in message.text:
        msg = bot.send_message(message.from_user.id, msgs.voice_start, parse_mode='HTML')
        usuario[message.from_user.id] = message.text.replace('/start ', '')
    else:
        try:
            print(select_info('ChatDeVoz', 'groupid', str(usuario[message.chat.id])))
        #if not select_info('groupid', str(usuario[message.from_user.id])):
        except:
            status = bot.get_chat_member(message.chat.id, message.from_user.id).status
            if message.chat.id < 0 and status in ADMIN:
                bot.reply_to(message, msgs.voice_not_started, parse_mode='HTML')
            elif message.chat.id < 0 and status not in ADMIN:
                bot.reply_to(message, msgs.voice_not_started_not_admin, parse_mode='HTML')
            else:
                bot.reply_to(message, msgs.start_user, parse_mode='HTML', disable_web_page_preview=True)
                bot.send_document(message.from_user.id, 'CgACAgEAAxkBAAPTYEexcA2G2cn6g2CdZS4MOVvm4ScAAhgBAAJhYUFGN48mu1WuJXMeBA')

@bot.message_handler(commands=['MeAvise'])
def bot_notify(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass
    if message.chat.id < 0:
        try:
            bot.send_chat_action(message.from_user.id, 'typing')
        except:
            bot.send_message(message.chat.id, msgs.start_user_unstarted, parse_mode='HTML')
            return 0
        groupid = 'g' + str(message.chat.id*-1)
        try:
            try:
                user = select_info(groupid, 'userid', message.from_user.id)
            except sqlite3.OperationalError:
                create_group_table(groupid)
                user = select_info(groupid, 'userid', message.from_user.id)
            if not user:
                print('Adicionado')
                add_sub(message.chat.id, message.from_user.id)
                bot.send_message(message.from_user.id, msgs.voice_sub.format(message.chat.title), parse_mode='HTML')
            else:
                print('Removido')
                del_sub(message.chat.id, message.from_user.id)
                bot.send_message(message.from_user.id, msgs.voice_unsub.format(message.chat.title), parse_mode='HTML')
        except:
            pass

#@bot.message_handler(content_types=['voice_chat_started'])
@bot.message_handler(commands=['Notificar'])
def voice_notify(message):
    status = bot.get_chat_member(message.chat.id, message.from_user.id).status
    if status in ADMIN:
        i = 0
        groupid = 'g' + str(message.chat.id*-1)
        users = select_all(groupid)
        for user in users:
            msg = msgs.voice_started.format(message.chat.title, str(message.chat.id).replace('-100', ''), message.message_id)
            try:
                bot.send_message(user[0], msg, parse_mode='HTML', disable_web_page_preview=True)
                time.sleep(0.2)
                i = i+1
            except:
                del_sub(message.chat.id, message.from_user.id)
                pass
        try:
            bot.send_message(message.chat.id, msgs.notified.format(i), parse_mode='HTML')
        except:
            pass
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

bot.polling()
