import os
import logging
from utils.lastb_entry import LastbEntry
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from utils.utils import run_command, get_commands_list, get_last_btmp_entry, remove_job_if_exists

TOKEN = os.getenv("APP_TOKEN")
MASTER_CHAT_ID = os.getenv("APP_MASTER_CHAT_ID")
JOB_INTERVAL = int(os.getenv("APP_JOB_INTERVAL", "30"))
OUTPUT_DELAY = int(os.getenv("APP_OUTPUT_DELAY", "5"))
global_stored_entry = LastbEntry(None, None, None)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def ping(update: Update, context: CallbackContext) -> None:
    """Sends explanation on how to use the bot."""
    update.message.reply_text('pong', parse_mode=ParseMode.HTML)


def do(update: Update, context: CallbackContext) -> None:
    """Sends explanation on how to use the bot."""
    if not update.message.chat_id == int(MASTER_CHAT_ID):
        update.message.reply_text("Access denied")
        return
    command = update.message.text[4:]
    output = run_command(command, OUTPUT_DELAY)
    update.message.reply_text("<pre>%s</pre>" % output, parse_mode=ParseMode.HTML)


def scripts(update: Update, context: CallbackContext) -> None:
    if not update.message.chat_id == int(MASTER_CHAT_ID):
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
    if not update.message.chat_id == int(MASTER_CHAT_ID):
        update.message.reply_text("Access denied")
        return
    commands = get_commands_list()
    keyboard = []
    for command in commands:
        keyboard.append([InlineKeyboardButton(text=command, callback_data=command)])
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Commands:", reply_markup=reply_markup)


def button_handler(update: Update, context: CallbackContext) -> None:
    if not update.callback_query.message.chat_id == int(MASTER_CHAT_ID):
        update.message.reply_text("Access denied")
        return
    query = update.callback_query
    query.answer()
    command = query.data
    output = run_command(command, OUTPUT_DELAY)
    query.edit_message_text("<pre>%s</pre>" % output, parse_mode=ParseMode.HTML)


def login_attempts_checker(context: CallbackContext) -> None:
    global global_stored_entry
    if global_stored_entry.is_empty():
        global_stored_entry = get_last_btmp_entry()
        return False

    tmp_entry = get_last_btmp_entry()
    if not global_stored_entry.is_equal(tmp_entry):
        if context:
            job = context.job
            context.bot.send_message(job.context, text='#alarm %s %s' % (tmp_entry.username, tmp_entry.host))
            global_stored_entry = tmp_entry
        return False
    return True


def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("ping", ping))
    dispatcher.add_handler(CommandHandler("do", do))
    dispatcher.add_handler(CommandHandler("scripts", scripts))
    dispatcher.add_handler(CommandHandler("commands", commands))
    dispatcher.add_handler(CallbackQueryHandler(button_handler))

    due = JOB_INTERVAL
    remove_job_if_exists("CHECK-LASTB", updater)
    updater.job_queue.run_repeating(login_attempts_checker, due, context=MASTER_CHAT_ID, name="CHECK-LASTB")

    logger.info("Latbot started")
    updater.bot.send_message(MASTER_CHAT_ID, text='Latbot online...')
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
