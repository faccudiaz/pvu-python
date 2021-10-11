import os
import pytz
import telebot
from datetime import datetime
from telegram.ext import Updater, MessageHandler, Filters
import datetime

my_secret = os.environ['API_KEY']
API_KEY = os.environ['API_KEY']
bot = telebot.TeleBot(API_KEY)
zone_ar = pytz.timezone('America/Argentina/Buenos_Aires')
id='1151584817'

updater = Updater(token=os.environ['API_KEY'], use_context=True)

def process_message(update, context):
    text = update.message.text
    if str(text).__contains__('#channel'):
        context.bot.send_message(
            chat_id=id,
            text=str(text).replace('#channel', 'dfsfdsfdsdfs')
        )
    if str(text).__contains__('start'):
        update.message.reply_text('Hola humano1')
    if str(text).__contains__('reminder'):
        send_reminder(text)

dp = updater.dispatcher
j = updater.job_queue
dp.add_handler(MessageHandler(filters=Filters.text, callback=process_message))
updater.start_polling()

def saludo_request(message):
  request = message.text.split()
  if len(request) < 2 or request[0].lower() not in "saludo":
    return False
  else:
    return True

@bot.message_handler(func=saludo_request)
def send_saludo(message):
  request = message.text.split()[1]
  data = request
  if data != '':
    print(data)
    bot.send_message(message.chat.id, data)

@bot.message_handler()
def send_time(message):
    currentTime = datetime.now(zone_ar)
    print(currentTime)
    bot.send_message(message.chat.id, currentTime)

def start(update, context):
    update.message.reply_text('Hola humano')

def once(context):
    # print(context.job.context.)
    print(context.job.context['name'])

    message = "ONCE " + context.job.context['name']
    context.bot.send_message(chat_id=id, text=message)

def morning(context):
    message = "Good Morning! Have a nice day!"
    context.bot.send_message(chat_id=id, text=message)

# def reminder_request(message):
#   request = message.text.split()
#   if len(request) < 2 or request[0].lower() not in "reminder":
#     return False
#   else:
#     return True

# @bot.message_handler(func=reminder_request)
def send_reminder(message):
  print('reminder')
  # data = message.split()[1]
  name = message.split()[1]
  hours = message.split()[2]
  minutes = message.split()[3]
  seconds = message.split()[4]
  # if data != '':
    # print('time', data)
  # j.run_once(once, 5)
  j.run_once(once, calcuate_time_in_seconds(hours, minutes, seconds),context={"name": name})
  bot.send_message(id, 'Enviando reminder de ' + name + ' en: ' + hours + 'hs ' + minutes + ' minutos ' + seconds + ' segundos')

def calcuate_time_in_seconds(hs, mins, secs):
  print(hs, mins, secs)
  secs_in_hours = 0
  secs_in_minutes = int(mins) * 60
  print(secs_in_hours)
  print(secs_in_minutes)
  print(int(secs_in_hours) + int(secs_in_minutes) + int(secs))
  return int(secs_in_hours) + int(secs_in_minutes) + int(secs)

if __name__ == '__main__':
    print('Bot is polling')
    t = datetime.time(3, 6, 00, 000000)
    j.run_daily(morning,t,days=(0, 1, 2, 3, 4, 5, 6),context=None,name=None)
    # j.run_daily(morning, days=(0, 1, 2, 3, 4, 5, 6), time=datetime.time(hour=10, minute=00, second=00))
    # j.run_once(once, 5, context={"chat_id": updater.message.chat_id, "text": updater.message.text, "custom_stuff": "some other text"})
    
    updater.idle()

bot.polling()