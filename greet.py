from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from pymongo import MongoClient
from config import MONGO_URI
import logging

logger = logging.getLogger(__name__)

client = MongoClient(MONGO_URI)
db = client.get_database()

async def greet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    args = context.args
    mode = args[0].lower() if args else "status"
    if mode not in ["on", "off", "status"]:
        await update.message.reply_text("Invalid mode. Use: on, off")
        return
    if mode == "status":
        status = db.channels.find_one({"chat_id": chat.id}) or {"greet": False}
        await update.message.reply_text(f"Greet is: {'on' if status['greet'] else 'off'}")
        return
    db.channels.update_one({"chat_id": chat.id}, {"$set": {"greet": mode == "on"}}, upsert=True)
    await update.message.reply_text(f"Greet set to: {mode}")

async def clean_greet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    args = context.args
    mode = args[0].lower() if args else "status"
    if mode not in ["on", "off", "status"]:
        await update.message.reply_text("Invalid mode. Use: on, off")
        return
    if mode == "status":
        status = db.channels.find_one({"chat_id": chat.id}) or {"clean_greet": False}
        await update.message.reply_text(f"Clean greet is: {'on' if status['clean_greet'] else 'off'}")
        return
    db.channels.update_one({"chat_id": chat.id}, {"$set": {"clean_greet": mode == "on"}}, upsert=True)
    await update.message.reply_text(f"Clean greet set to: {mode}")

async def join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    args = context.args
    mode = args[0].lower() if args else "status"
    if mode not in ["on", "off", "decline", "status"]:
        await update.message.reply_text("Invalid mode. Use: on, off, decline")
        return
    if mode == "status":
        status = db.channels.find_one({"chat_id": chat.id}) or {"join_request": "off"}
        await update.message.reply_text(f"Join request is: {status['join_request']}")
        return
    db.channels.update_one({"chat_id": chat.id}, {"$set": {"join_request": mode}}, upsert=True)
    await update.message.reply_text(f"Join request set to: {mode}")

def setup_greet_handlers(application: Application):
    application.add_handler(CommandHandler("greet", greet))
    application.add_handler(CommandHandler("cleangreet", clean_greet))
    application.add_handler(CommandHandler("joinrequest", join_request))
