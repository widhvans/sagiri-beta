from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from pymongo import MongoClient
from config import MONGO_URI
import logging

logger = logging.getLogger(__name__)

client = MongoClient(MONGO_URI)
db = client.get_database()

async def pinned(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    channel = db.channels.find_one({"chat_id": chat.id})
    pinned_id = channel.get("pinned_message_id") if channel else None
    if pinned_id:
        await update.message.reply_text(f"Pinned message ID: {pinned_id}")
    else:
        await update.message.reply_text("No pinned message found.")

async def unpin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    try:
        await context.bot.unpin_chat_message(chat.id)
        db.channels.update_one({"chat_id": chat.id}, {"$unset": {"pinned_message_id": ""}})
        await update.message.reply_text("Pinned message unpinned.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def autopin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    args = context.args
    mode = args[0].lower() if args else "status"
    if mode not in ["on", "off", "status"]:
        await update.message.reply_text("Invalid mode. Use: on, off")
        return
    if mode == "status":
        status = db.channels.find_one({"chat_id": chat.id}) or {"autopin": False}
        await update.message.reply_text(f"Autopin is: {'on' if status['autopin'] else 'off'}")
        return
    db.channels.update_one({"chat_id": chat.id}, {"$set": {"autopin": mode == "on"}}, upsert=True)
    await update.message.reply_text(f"Autopin set to: {mode}")

def setup_pins_handlers(application: Application):
    application.add_handler(CommandHandler("pinned", pinned))
    application.add_handler(CommandHandler("unpin", unpin))
    application.add_handler(CommandHandler("autopin", autopin))
