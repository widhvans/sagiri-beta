from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from pymongo import MongoClient
from config import MONGO_URI
import logging

logger = logging.getLogger(__name__)

client = MongoClient(MONGO_URI)
db = client.get_database("mychannelbot")

async def blacklist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    args = context.args
    if not args or args[0].lower() == "off":
        blacklist = db.channels.find_one({"chat_id": chat.id}) or {"blacklist": []}
        await update.message.reply_text(f"Blacklist: {', '.join(blacklist['blacklist'])}")
        return
    db.channels.update_one({"chat_id": chat.id}, {"$set": {"blacklist_enabled": args[0].lower() != "off"}}, upsert=True)
    await update.message.reply_text("Blacklist toggled.")

async def add_blacklist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    args = context.args
    if not args:
        await update.message.reply_text("Please provide words to add: /addbl word")
        return
    db.channels.update_one({"chat_id": chat.id}, {"$addToSet": {"blacklist": {"$each": args}}}, upsert=True)
    await update.message.reply_text("Words added to blacklist.")

async def remove_blacklist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    args = context.args
    if not args:
        await update.message.reply_text("Please provide words to remove: /rmbl word")
        return
    db.channels.update_one({"chat_id": chat.id}, {"$pullAll": {"blacklist": args}}, upsert=True)
    await update.message.reply_text("Words removed from blacklist.")

def setup_locks_handlers(application: Application):
    application.add_handler(CommandHandler("blacklist", blacklist))
    application.add_handler(CommandHandler("addbl", add_blacklist))
    application.add_handler(CommandHandler("rmbl", remove_blacklist))
