from telegram.ext import CallbackContext
from common.lastb_entry import LastbEntry
from common import config

app_config = config.get_config()


def login_attempts_checker(context: CallbackContext) -> None:
    if app_config.GLOBAL_STORED_ENTRY.is_empty():
        app_config.GLOBAL_STORED_ENTRY = LastbEntry.get_last_btmp_entry()
        return False

    tmp_entry = LastbEntry.get_last_btmp_entry()
    if not app_config.GLOBAL_STORED_ENTRY.is_equal(tmp_entry):
        if context:
            job = context.job
            context.bot.send_message(job.context, text='#alarm %s %s' % (tmp_entry.username, tmp_entry.host))
            app_config.GLOBAL_STORED_ENTRY = tmp_entry
        return False
    return True


def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True
