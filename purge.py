from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from pymongo import MongoClient
from config import MONGO_URI
import logging

logger = logging.getLogger(__name__)

client = MongoClient(MONGO_URI)
db = client.get_database("mychannelbot")

async def purge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if not update.message.reply_to_message:
        await update.message.reply_text("Please reply to a message to purge up to.")
        return
    start_message_id = update.message.reply_to_message.message_id
    end_message_id = update.message.message_id
    for msg_id in range(start_message_id, end_message_id + 1):
        try:
            await context.bot.delete_message(chat.id, msg_id)
        except Exception as e:
            logger.error(f"Failed to delete message {msg_id}: {e}")
    await update.message.reply_text("Messages purged.")

async def purge_x(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    args = context.args
    if not args or not args[0].isdigit():
        await update.message.reply_text("Please provide a number of messages to purge: /purge X")
        return
    count = int(args[0])
    if not update.message.reply_to_message:
        await update.message.reply_text("Please reply to a message to start purging from.")
        return
    start_message_id = update.message.reply_to_message.message_id
    for msg_id in range(start_message_id, start_message_id + count + 1):
        try:
            await context.bot.delete_message(chat.id, msg_id)
        except Exception as e:
            logger.error(f"Failed to delete message {msg_id}: {e}")
    await update.message.reply_text(f"Purged {count} messages.")

def setup_purge_handlers(application: Application):
    application.add_handler(CommandHandler("purge", purge))
    application.add_handler(CommandHandler("purge", purge_x))
