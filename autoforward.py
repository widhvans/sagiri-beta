from telegram import Update
from telegram.ext import Application, CommandHandler, Context28ContextTypes
from pymongo import MongoClient
from config import MONGO_URI
import logging

logger = logging.getLogger(__name__)

client = MongoClient(MONGO_URI)
db = client.get_database("mychannelbot")

async def autoforward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    args = context.args
    if not args:
        await update.message.reply_text("Usage: /autoforward off/chat_id")
        return
    target = args[0]
    db.channels.update_one({"chat_id": chat.id}, {"$set": {"autoforward_target": target}}, upsert=True)
    await update.message.reply_text(f"Auto-forward set to: {target}")

async def forward_del(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    args = context.args
    mode = args[0].lower() if args else "off"
    if mode not in ["on", "off"]:
        await update.message.reply_text("Invalid mode. Use: on, off")
        return
    db.channels.update_one({"chat_id": chat.id}, {"$set": {"forward_delete": mode == "on"}}, upsert=True)
    await update.message.reply_text(f"Forward delete set to: {mode}")

async def forward_tag(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    args = context.args
    mode = args[0].lower() if args else "off"
    if mode not in ["on", "off"]:
        await update.message.reply_text("Invalid mode. Use: on, off")
        return
    db.channels.update_one({"chat_id": chat.id}, {"$set": {"forward_tag": mode == "on"}}, upsert=True)
    await update.message.reply_text(f"Forward tag set to: {mode}")

def setup_autoforward_handlers(application: Application):
    application.add_handler(CommandHandler("autoforward", autoforward))
    application.add_handler(CommandHandler("forwarddel", forward_del))
    application.add_handler(CommandHandler("forwardtag", forward_tag))
