from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from pymongo import MongoClient
from config import MONGO_URI
import logging

logger = logging.getLogger(__name__)

client = MongoClient(MONGO_URI)
db = client.get_database("mychannelbot")

async def set_gap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    args = context.args
    if not args or not args[0].isdigit() or int(args[0]) not in [1, 2, 3]:
        await update.message.reply_text("Please provide a valid gap (1, 2, or 3): /setgap x")
        return
    gap = int(args[0])
    db.channels.update_one({"chat_id": chat.id}, {"$set": {"caption_gap": gap}}, upsert=True)
    await update.message.reply_text(f"Caption gap set to {gap} line(s).")

async def inline_tag(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    args = context.args
    if not args:
        await update.message.reply_text("Usage: /inlinetag mode/off\nModes: del|on, repost, recaption")
        return
    mode = args[0].lower()
    if mode not in ["del", "on", "repost", "recaption", "off"]:
        await update.message.reply_text("Invalid mode. Use: del|on, repost, recaption, off")
        return
    db.channels.update_one({"chat_id": chat.id}, {"$set": {"inline_tag_mode": mode}}, upsert=True)
    await update.message.reply_text(f"Inline tag mode set to: {mode}")

async def set_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if not update.message.reply_to_message or not update.message.reply_to_message.sticker:
        await update.message.reply_text("Please reply to a sticker to set.")
        return
    sticker = update.message.reply_to_message.sticker.file_id
    db.channels.update_one({"chat_id": chat.id}, {"$set": {"sticker": sticker}}, upsert=True)
    await update.message.reply_text("Sticker set for posts.")

async def disable_preview(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    args = context.args
    mode = args[0].lower() if args else "default"
    if mode not in ["on", "off", "default", "0"]:
        await update.message.reply_text("Invalid mode. Use: on, off, default, 0")
        return
    db.channels.update_one({"chat_id": chat.id}, {"$set": {"disable_preview": mode}}, upsert=True)
    await update.message.reply_text(f"Disable preview set to: {mode}")

async def set_header(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    args = context.args
    if not args:
        await update.message.reply_text("Usage: /setheader format/off/noformat")
        return
    header = " ".join(args)
    db.channels.update_one({"chat_id": chat.id}, {"$set": {"header": header}}, upsert=True)
    await update.message.reply_text(f"Header set to: {header}")

def setup_autocaption_handlers(application: Application):
    application.add_handler(CommandHandler("setgap", set_gap))
    application.add_handler(CommandHandler("inlinetag", inline_tag))
    application.add_handler(CommandHandler("setsticker", set_sticker))
    application.add_handler(CommandHandler("disablepreview", disable_preview))
    application.add_handler(CommandHandler("setheader", set_header))
