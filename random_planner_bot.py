# -*- coding: utf-8 -*-
import config
import datetime as dt
from emoji import emojize
import planner
import shelve
import telebot

bot = telebot.TeleBot(config.token)
db = shelve.open(config.dbname)
db['task'] = "#*(#*#(*#UJ" #random string
db['start_time'] = dt.datetime.now()
db.close()

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
    db = shelve.open(config.dbname)
    task = db['task']
    start_time = db['start_time']
    tree = planner.read_file_to_tree(open(config.filename))
    if message.text.lower() in ['next', 'n']:
        task = planner.get_next_task(tree)
        db['task'] = task
        db['start_time'] = dt.datetime.now()
        bot.send_message(message.chat.id, task)
    elif message.text.lower() ==  'done':
        tree = planner.read_file_to_tree(open(config.filename))
        task_info = planner.complete_task(task, config.filename, start_time, tree)
        smiley = emojize(":smile_cat:", use_aliases=True)
        bot.send_message(message.chat.id, 'Excellent work! ' + ' ' + task_info)
    elif message.text.lower() in ['postpone', 'pause']:
        task_info = planner.postpone_task(task, config.filename, start_time)
        bot.send_message(message.chat.id, 'Task_postponed: ' + task_info)
    elif message.text.lower() in ['test']:
        cake = emojize(":smile_cat:", use_aliases=True)
        bot.send_message(message.chat.id, 'Tested! ' + cake)
    db.close()

if __name__ == '__main__':
    bot.polling(none_stop=True)
