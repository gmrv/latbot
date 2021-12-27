import logging
from common import config
from common.utils import set_app_root_path
from handlers import commands, buttons
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, Filters, MessageHandler
from common.jobs import remove_job_if_exists, login_attempts_checker

app_config = config.get_config()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, app_config.TRACE_LEVEL, logging.INFO)
)
logger = logging.getLogger(__name__)


def main() -> None:
    updater = Updater(app_config.TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("ping", commands.ping))
    dispatcher.add_handler(CommandHandler("do", commands.do))
    dispatcher.add_handler(CommandHandler("scripts", commands.scripts))
    dispatcher.add_handler(CommandHandler("commands", commands.commands))
    dispatcher.add_handler(CallbackQueryHandler(buttons.button_handler))

    # on non command i.e message
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, commands.non_command))

    due = app_config.JOB_INTERVAL
    remove_job_if_exists("CHECK-LASTB", updater)
    updater.job_queue.run_repeating(login_attempts_checker, due, context=app_config.MASTER_CHAT_ID, name="CHECK-LASTB")

    set_app_root_path()
    logger.info("Latbot started")
    updater.bot.send_message(app_config.MASTER_CHAT_ID, text='Latbot online...')
    updater.bot.send_message(app_config.MASTER_CHAT_ID, text=f'Bot root catalog: {app_config.APP_ABSOLUTE_PATH}')
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
