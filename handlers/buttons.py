from common import config
from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from common.utils import run_command


def button_handler(update: Update, context: CallbackContext) -> None:
    if not update.callback_query.message.chat_id == int(config.MASTER_CHAT_ID):
        update.message.reply_text("Access denied")
        return
    query = update.callback_query
    query.answer()
    command = query.data
    output = run_command(command, config.OUTPUT_DELAY)
    query.edit_message_text("<pre>%s</pre>" % output, parse_mode=ParseMode.HTML)
