from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from pymongo import MongoClient
from config import MONGO_URI
import logging

logger = logging.getLogger(__name__)

client = MongoClient(MONGO_URI)
db = client.get_database()

async def clean_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    args = context.args
    mode = args[0].lower() if args else "status"
    if mode not in ["on", "off", "status"]:
        await update.message.reply_text("Invalid mode. Use: on, off")
        return
    if mode == "status":
        status = db.channels.find_one({"chat_id": chat.id}) or {"clean_service": False}
        await update.message.reply_text(f"Clean service is: {'on' if status['clean_service'] else 'off'}")
        return
    db.channels.update_one({"chat_id": chat.id}, {"$set": {"clean_service": mode == "on"}}, upsert=True)
    await update.message.reply_text(f"Clean service set to: {mode}")

def setup_cleaner_handlers(application: Application):
    application.add_handler(CommandHandler("cleanservice", clean_service))
