from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from pymongo import MongoClient
from config import MONGO_URI
import logging

logger = logging.getLogger(__name__)

client = MongoClient(MONGO_URI)
db = client.get_database("mychannelbot")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    # Check if user is admin
    admins = db.admins.find_one({"chat_id": chat.id}) or {"admins": []}
    if user.id not in admins["admins"]:
        await update.message.reply_text("This command is for admins only.")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("Please reply to a message to broadcast.")
        return

    message = update.message.reply_to_message
    channels = db.channels.find()

    for channel in channels:
        try:
            await context.bot.forward_message(
                chat_id=channel["chat_id"],
                from_chat_id=chat.id,
                message_id=message.message_id
            )
        except Exception as e:
            logger.error(f"Failed to broadcast to {channel['chat_id']}: {e}")

    await update.message.reply_text("Broadcast sent to all connected channels.")

def setup_broadcast_handlers(application: Application):
    application.add_handler(CommandHandler("broadcast", broadcast))
