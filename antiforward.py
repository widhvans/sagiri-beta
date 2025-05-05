from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from pymongo import MongoClient
from config import MONGO_URI
import logging

logger = logging.getLogger(__name__)

client = MongoClient(MONGO_URI)
db = client.get_database("mychannelbot")

async def antiforward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    args = context.args
    if not args:
        await update.message.reply_text("Usage: /antiforward mode/off\nModes: del|on, repost, recaption")
        return
    mode = args[0].lower()
    if mode not in ["del", "on", "repost", "recaption", "off"]:
        await update.message.reply_text("Invalid mode. Use: del|on, repost, recaption, off")
        return
    db.channels.update_one({"chat_id": chat.id}, {"$set": {"antiforward_mode": mode}}, upsert=True)
    await update.message.reply_text(f"Anti-forward mode set to: {mode}")

async def no_antiforward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    args = context.args
    if not args or args[0].lower() == "off":
        no_antiforward = db.channels.find_one({"chat_id": chat.id}) or {"no_antiforward": []}
        await update.message.reply_text(f"No-anti-forward words: {', '.join(no_antiforward['no_antiforward'])}")
        return
    db.channels.update_one({"chat_id": chat.id}, {"$set": {"no_antiforward_enabled": args[0].lower() != "off"}}, upsert=True)
    await update.message.reply_text("No-anti-forward toggled.")

async def add_no_antiforward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    args = context.args
    if not args:
        await update.message.reply_text("Please provide words to add: /addnoantiforward word")
        return
    db.channels.update_one({"chat_id": chat.id}, {"$addToSet": {"no_antiforward": {"$each": args}}}, upsert=True)
    await update.message.reply_text("Words added to no-anti-forward list.")

async def remove_no_antiforward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    args = context.args
    if not args:
        await update.message.reply_text("Please provide words to remove: /rmnoantiforward word")
        return
    db.channels.update_one({"chat_id": chat.id}, {"$pullAll": {"no_antiforward": args}}, upsert=True)
    await update.message.reply_text("Words removed from no-anti-forward list.")

def setup_antiforward_handlers(application: Application):
    application.add_handler(CommandHandler("antiforward", antiforward))
    application.add_handler(CommandHandler("noantiforward", no_antiforward))
    application.add_handler(CommandHandler("addnoantiforward", add_no_antiforward))
    application.add_handler(CommandHandler("rmnoantiforward", remove_no_antiforward))
