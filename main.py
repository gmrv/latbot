import logging
from common import config
from handlers import commands, buttons
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, Filters, MessageHandler
from common.jobs import remove_job_if_exists, login_attempts_checker

config = config.get_config()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, config.TRACE_LEVEL, logging.INFO)
)
logger = logging.getLogger(__name__)


def main() -> None:
    updater = Updater(config.TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("ping", commands.ping))
    dispatcher.add_handler(CommandHandler("do", commands.do))
    dispatcher.add_handler(CommandHandler("scripts", commands.scripts))
    dispatcher.add_handler(CommandHandler("commands", commands.commands))
    dispatcher.add_handler(CallbackQueryHandler(buttons.button_handler))

    # on non command i.e message
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, commands.non_command))

    due = config.JOB_INTERVAL
    remove_job_if_exists("CHECK-LASTB", updater)
    updater.job_queue.run_repeating(login_attempts_checker, due, context=config.MASTER_CHAT_ID, name="CHECK-LASTB")

    logger.info("Latbot started")
    updater.bot.send_message(config.MASTER_CHAT_ID, text='Latbot online...')
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
