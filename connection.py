from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from pymongo import MongoClient
from config import MONGO_URI
import logging

logger = logging.getLogger(__name__)

client = MongoClient(MONGO_URI)
db = client.get_database("mychannelbot")

async def reset_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    if not db.channels.find_one({"chat_id": chat.id, "owner_id": user.id}):
        await update.message.reply_text("Only the channel owner can reset data.")
        return
    db.channels.delete_one({"chat_id": chat.id})
    await update.message.reply_text("All channel data reset.")

async def remove_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    args = context.args
    if not args:
        await update.message.reply_text("Please provide a chat ID: /rmchannel chat_id")
        return
    chat_id = args[0]
    if not db.channels.find_one({"chat_id": chat_id, "adder_id": update.effective_user.id}):
        await update.message.reply_text("You can only remove channels you added.")
        return
    db.channels.delete_one({"chat_id": chat_id})
    await update.message.reply_text(f"Channel {chat_id} removed from database.")

async def connection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    channel = db.channels.find_one({"chat_id": chat.id})
    if not channel:
        await update.message.reply_text("No connected channel found.")
        return
    await update.message.reply_text(f"Connected channel: {channel['chat_id']}")

def setup_connection_handlers(application: Application):
    application.add_handler(CommandHandler("resetall", reset_all))
    application.add_handler(CommandHandler("rmchannel", remove_channel))
    application.add_handler(CommandHandler("connection", connection))
