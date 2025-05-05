from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from pymongo import MongoClient
from config import MONGO_URI
import logging

logger = logging.getLogger(__name__)

client = MongoClient(MONGO_URI)
db = client.get_database("mychannelbot")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    # Check if user is admin
    admins = db.admins.find_one({"chat_id": chat.id}) or {"admins": []}
    if user.id not in admins["admins"]:
        await update.message.reply_text("This command is for admins only.")
        return

    total_users = db.users.count_documents({})
    total_channels = db.channels.count_documents({})

    stats_text = f"📊 Bot Statistics:\n\nTotal Users: {total_users}\nTotal Channels: {total_channels}"
    await update.message.reply_text(stats_text)

def setup_stats_handlers(application: Application):
    application.add_handler(CommandHandler("stats", stats))
