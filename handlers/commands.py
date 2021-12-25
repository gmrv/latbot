from common import config
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import CallbackContext
from common.utils import run_command, get_commands_list

app_config = config.get_config()

def ping(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('pong', parse_mode=ParseMode.HTML)


def do(update: Update, context: CallbackContext) -> None:
    if not update.message.chat_id == int(app_config.MASTER_CHAT_ID):
        update.message.reply_text("Access denied")
        return
    command = update.message.text[4:]
    output = run_command(command, app_config.OUTPUT_DELAY)
    update.message.reply_text("<pre>%s</pre>" % output, parse_mode=ParseMode.HTML)


def scripts(update: Update, context: CallbackContext) -> None:
    if not update.message.chat_id == int(app_config.MASTER_CHAT_ID):
        update.message.reply_text("Access denied")
        return
    output = run_command("ls ./scripts/*.sh", 1)
    filenames = output.splitlines()
    keyboard = []
    for f in filenames:
        if len(f) > 4:
            filename = f.split("/")[2]
            keyboard.append([InlineKeyboardButton(filename, callback_data=f)])
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Scripts:", reply_markup=reply_markup)


def commands(update: Update, context: CallbackContext) -> None:
    if not update.message.chat_id == int(app_config.MASTER_CHAT_ID):
        update.message.reply_text("Access denied")
        return
    commands = get_commands_list()
    keyboard = []
    for command in commands:
        keyboard.append([InlineKeyboardButton(text=command, callback_data=command)])
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Commands:", reply_markup=reply_markup)
