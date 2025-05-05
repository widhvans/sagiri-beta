from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from pymongo import MongoClient
from config import MONGO_URI
import logging

logger = logging.getLogger(__name__)

client = MongoClient(MONGO_URI)
db = client.get_database()

async def nchannels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    channels = db.channels.find()
    channel_list = "\n".join([f"{channel['chat_id']}" for channel in channels])
    await update.message.reply_text(f"Network channels:\n{channel_list or 'None'}")

async def nkick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("Please provide a user ID or username: /nkick id|username")
        return
    user_id = args[0]
    channels = db.channels.find()
    for channel in channels:
        try:
            await context.bot.ban_chat_member(channel["chat_id"], user_id)
            await context.bot.unban_chat_member(channel["chat_id"], user_id)
        except Exception as e:
            logger.error(f"Failed to kick {user_id} from {channel['chat_id']}: {e}")
    await update.message.reply_text(f"User {user_id} kicked from network channels.")

async def nbroadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("Please reply to a message to broadcast.")
        return
    message = update.message.reply_to_message
    channels = db.channels.find()
    for channel in channels:
        try:
            await context.bot.forward_message(
                chat_id=channel["chat_id"],
                from_chat_id=update.effective_chat.id,
                message_id=message.message_id
            )
        except Exception as e:
            logger.error(f"Failed to broadcast to {channel['chat_id']}: {e}")
    await update.message.reply_text("Broadcast sent to network channels.")

def setup_network_handlers(application: Application):
    application.add_handler(CommandHandler("nchannels", nchannels))
    application.add_handler(CommandHandler("nkick", nkick))
    application.add_handler(CommandHandler("nbroadcast", nbroadcast))
