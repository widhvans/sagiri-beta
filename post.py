from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from pymongo import MongoClient
from config import MONGO_URI
import logging

logger = logging.getLogger(__name__)

client = MongoClient(MONGO_URI)
db = client.get_database("mychannelbot")

async def post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    args = context.args
    text = " ".join(args)
    if update.message.reply_to_message:
        await context.bot.copy_message(
            chat_id=chat.id,
            from_chat_id=chat.id,
            message_id=update.message.reply_to_message.message_id,
            caption=text,
            parse_mode="Markdown"
        )
    else:
        await context.bot.send_message(chat_id=chat.id, text=text, parse_mode="Markdown")
    await update.message.reply_text("Message posted.")

async def edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    args = context.args
    if not args and not update.message.reply_to_message:
        await update.message.reply_text("Please provide a message ID or reply to a message: /edit message_id text")
        return
    message_id = args[0] if args else update.message.reply_to_message.message_id
    text = " ".join(args[1:]) if len(args) > 1 else " ".join(context.args)
    try:
        await context.bot.edit_message_text(
            chat_id=chat.id,
            message_id=message_id,
            text=text,
            parse_mode="Markdown"
        )
        await update.message.reply_text("Message edited.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    args = context.args
    if not args:
        await update.message.reply_text("Usage: /schedule interval times delete_last_message text/off/noformat")
        return
    interval = args[0]
    # Simplified scheduling (actual implementation requires job queue)
    db.channels.update_one({"chat_id": chat.id}, {"$set": {"schedule": {"interval": interval, "text": " ".join(args[3:])}}}, upsert=True)
    await update.message.reply_text(f"Scheduled message with interval: {interval}")

def setup_post_handlers(application: Application):
    application.add_handler(CommandHandler("post", post))
    application.add_handler(CommandHandler("edit", edit))
    application.add_handler(CommandHandler("schedule", schedule))
