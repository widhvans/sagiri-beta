from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from pymongo import MongoClient
from config import MONGO_URI
import logging

logger = logging.getLogger(__name__)

client = MongoClient(MONGO_URI)
db = client.get_database()

async def replace(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    args = context.args
    if not args or args[0].lower() == "off":
        replacements = db.channels.find_one({"chat_id": chat.id}) or {"replacements": []}
        await update.message.reply_text(f"Replacements: {replacements['replacements']}")
        return
    db.channels.update_one({"chat_id": chat.id}, {"$set": {"replace_enabled": args[0].lower() != "off"}}, upsert=True)
    await update.message.reply_text("Replace toggled.")

async def add_replace(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    args = context.args
    if not args:
        await update.message.reply_text("Please provide words to replace: /addreplace old-word::new-word")
        return
    replacements = [arg.split("::") for arg in args]
    db.channels.update_one({"chat_id": chat.id}, {"$addToSet": {"replacements": {"$each": replacements}}}, upsert=True)
    await update.message.reply_text("Replacements added.")

async def remove_replace(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    args = context.args
    if not args:
        await update.message.reply_text("Please provide words to remove: /rmreplace word")
        return
    db.channels.update_one({"chat_id": chat.id}, {"$pullAll": {"replacements": args}}, upsert=True)
    await update.message.reply_text("Replacements removed.")

def setup_replace_handlers(application: Application):
    application.add_handler(CommandHandler("replace", replace))
    application.add_handler(CommandHandler("addreplace", add_replace))
    application.add_handler(CommandHandler("rmreplace", remove_replace))
