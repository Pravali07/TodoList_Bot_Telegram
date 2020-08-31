from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
import logging
import json
import os
PORT = int(os.environ.get('PORT',5000))
TOKEN = 'give your API Key here'
updater = Updater(token = TOKEN,use_context = True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


tasks = {}
#start command
def start(update,context):
    context.bot.send_message(chat_id = update.effective_chat.id,text="Hi! I'm a Todo bot"+'\n'+"Type /help to see what I can do.")
start_handler = CommandHandler('start',start)
dispatcher.add_handler(start_handler)


#help command
def help(update, context):
    help_msg = '''You can manage your Todo List using the following Commands.

Commands:
/add - adds todos to the list
/view - lists all todos 
/done - mark todos as complete
/delete - deletes todo from the list
/completed - lists all completed todos
/add_help - help command for /add
/view_help - help command for /view
/done_help - help command for /done
/delete_help - help command for /delete
/complete_help - help command for /completed
'''
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_msg)
help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)


#add_help command
def add_help(update,context):
    msg = '''Usage of /add command

Enter a Todo you want to add to the list without any leading and trailing whitespaces.

Example:
/add Eat some bread
'''
    context.bot.send_message(chat_id = update.effective_chat.id, text = msg)
addHelp_handler = CommandHandler('add_help',add_help)
dispatcher.add_handler(addHelp_handler)


#adding todos to the list
def addTask(update,context):
    task = ' '.join( str(a) for a in context.args).upper()
    t = task.strip()
    if t:
        user = update.message.chat.first_name
        if user in tasks.keys():
            tasks[user].append(t)
        else:
            l = []
            l.append(t)
            tasks[user] = l
        context.bot.send_message(chat_id = update.message.chat_id, text = "The Todo "+t+" added to the list, and You can view your Todo List using /view command.")
    else:
        context.bot.send_message(chat_id = update.message.chat_id, text = "Enter a valid Todo, use /add_help command for help.")
task_handler = CommandHandler('add',addTask)
dispatcher.add_handler(task_handler)


#view_help command
def view_help(update,context):
    msg = '''Usage of /view command

Just enter the command to view all Todos
'''
    context.bot.send_message(chat_id = update.effective_chat.id, text = msg)
viewHelp_handler = CommandHandler('view_help',view_help)
dispatcher.add_handler(viewHelp_handler)


#view all the todos 
def viewTask(update,context):
    user = update.message.chat.first_name
    if user not in tasks.keys() or len(tasks[user]) == 0:
        msg = "Your Todo List is empty. Add todos to the list using /add command to view."
        context.bot.send_message(chat_id = update.effective_chat.id,text = msg)
    else:
        view = 'The Todos in the list: '
        view += '\n\n'
        
        for t in tasks[user]:
            view += t
            view += '\n'
            print(view)
        context.bot.send_message(chat_id = update.effective_chat.id,text = view)
view_handler = CommandHandler('view',viewTask)
dispatcher.add_handler(view_handler)


#done_help command
def done_help(update,context):
    msg = '''Usage of /done command

Enter a Todo that you want mark it as complete.

Example:
/done Eat some bread
'''
    context.bot.send_message(chat_id = update.effective_chat.id, text = msg)
doneHelp_handler = CommandHandler('done_help',done_help)
dispatcher.add_handler(doneHelp_handler)

    
completed = {}
#mark todos as completed
def doneTodos(update,context):
    user = update.message.chat.first_name
    msg = ''
    d = ' '.join(str(a) for a in context.args).upper()
    if user in tasks.keys() and d in tasks[user]:
            if user in completed.keys():
                completed[user].append(d)
            else:
                l = []
                l.append(d)
                completed[user] = l
            i = tasks[user].index(d)
            del tasks[user][i]
            msg = "The Todo "+d+" is marked as complete and removed from the Todo List, If you want to view the completed Todos List use the command /completed."
    else:
        msg = "No such Todo"
    context.bot.send_message(chat_id = update.effective_chat.id,text = msg)
done_handler = CommandHandler('done',doneTodos)
dispatcher.add_handler(done_handler)


#delete_help command
def delete_help(update,context):
    msg = '''Usage of /delete command

Enter the Todo you want to delete from the list.

Example:
/delete Eat some bread
'''
    context.bot.send_message(chat_id = update.effective_chat.id, text = msg)
deleteHelp_handler = CommandHandler('delete_help',delete_help)
dispatcher.add_handler(deleteHelp_handler)


#delete Todos
def deleteTodos(update,context):
    user = update.message.chat.first_name
    msg = ''
    d = ' '.join(str(a) for a in context.args).upper()
    if user in tasks.keys() and d in tasks[user]:
            i = tasks[user].index(d)
            del tasks[user][i]
            msg = "The Todo " + d + " is removed from the list, If you want to view the updated Todo List use the command /view."
    else:
        msg = "No such Todo"
    context.bot.send_message(chat_id = update.effective_chat.id,text = msg)
delete_handler = CommandHandler('delete',deleteTodos)
dispatcher.add_handler(delete_handler)


#complete_help command
def complete_help(update,context):
    msg = '''Usage of /completed command

Just enter the command to view all the completed Todos
'''
    context.bot.send_message(chat_id = update.effective_chat.id, text = msg)
completeHelp_handler = CommandHandler('complete_help',complete_help)
dispatcher.add_handler(completeHelp_handler)


#view completed Todos
def completedTodos(update,context):
    user = update.message.chat.first_name
    if user not in completed.keys() or len(completed[user]) == 0:
        msg = "Your Completed Todo List is empty. You can add your Todos to Completed Todos by marking them as done using /done command."
        context.bot.send_message(chat_id = update.effective_chat.id,text = msg)
    else:
        view = 'Completed Todos: '
        view += '\n\n'
        
        for t in completed[user]:
            view += t
            view += '\n'
            print(view)
        context.bot.send_message(chat_id = update.effective_chat.id,text = view)
viewDone_handler = CommandHandler('completed',completedTodos)
dispatcher.add_handler(viewDone_handler)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)
    
updater.start_webhook(listen = "0.0.0.0",port = int(PORT),url_path = TOKEN,clean=True)
updater.bot.setWebhook('https://young-refuge-36136.herokuapp.com/' + TOKEN)
