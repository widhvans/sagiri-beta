from telegram import Update, InputMediaPhoto
from telegram.ext import Application, CommandHandler, ContextTypes
from pymongo import MongoClient
from config import MONGO_URI
import logging

logger = logging.getLogger(__name__)

client = MongoClient(MONGO_URI)
db = client.get_database("mychannelbot")

async def set_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    args = context.args
    if not args:
        await update.message.reply_text("Please provide a new title: /settitle newtitle")
        return
    new_title = " ".join(args)
    try:
        await context.bot.set_chat_title(chat.id, new_title)
        await update.message.reply_text(f"Channel title set to: {new_title}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    args = context.args
    if not args:
        await update.message.reply_text("Please provide a user ID or username: /kick id|username")
        return
    user_id = args[0]
    try:
        await context.bot.ban_chat_member(chat.id, user_id)
        await context.bot.unban_chat_member(chat.id, user_id)
        await update.message.reply_text(f"User {user_id} kicked from the channel.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    args = context.args
    if not args:
        await update.message.reply_text("Please provide a user ID or username: /unban id|username")
        return
    user_id = args[0]
    try:
        await context.bot.unban_chat_member(chat.id, user_id)
        await update.message.reply_text(f"User {user_id} unbanned from the channel.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def set_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    args = context.args
    if not args:
        await update.message.reply_text("Please provide a description: /setdes description")
        return
    description = " ".join(args)
    try:
        await context.bot.set_chat_description(chat.id, description)
        await update.message.reply_text("Channel description updated.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def promote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    args = context.args
    if not args:
        await update.message.reply_text("Please provide a user ID or username: /promote id|username")
        return
    user_id = args[0]
    try:
        await context.bot.promote_chat_member(
            chat.id, user_id,
            can_change_info=True, can_delete_messages=True, can_invite_users=True,
            can_pin_messages=True, can_promote_members=True
        )
        await update.message.reply_text(f"User {user_id} promoted in the channel.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def demote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    args = context.args
    if not args:
        await update.message.reply_text("Please provide a user ID or username: /demote id|username")
        return
    user_id = args[0]
    try:
        await context.bot.promote_chat_member(
            chat.id, user_id,
            can_change_info=False, can_delete_messages=False, can_invite_users=False,
            can_pin_messages=False, can_promote_members=False
        )
        await update.message.reply_text(f"User {user_id} demoted in the channel.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def admins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    try:
        admins = await context.bot.get_chat_administrators(chat.id)
        admin_list = "\n".join([f"@{admin.user.username or admin.user.full_name} (ID: {admin.user.id})" for admin in admins])
        await update.message.reply_text(f"Admins:\n{admin_list}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def delete_pic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    try:
        await context.bot.set_chat_photo(chat.id, None)
        await update.message.reply_text("Channel profile picture removed.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def set_pic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        await update.message.reply_text("Please reply to a photo to set as channel picture.")
        return
    photo = update.message.reply_to_message.photo[-1]
    try:
        photo_file = await photo.get_file()
        await context.bot.set_chat_photo(chat.id, photo_file)
        await update.message.reply_text("Channel profile picture updated.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    args = context.args
    if not args:
        await update.message.reply_text("Please provide a user ID or username: /ban id|username [time]")
        return
    user_id = args[0]
    ban_time = args[1] if len(args) > 1 else None
    try:
        await context.bot.ban_chat_member(chat.id, user_id, until_date=ban_time)
        await update.message.reply_text(f"User {user_id} banned from the channel.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def setup_admins_handlers(application: Application):
    application.add_handler(CommandHandler("settitle", set_title))
    application.add_handler(CommandHandler("kick", kick))
    application.add_handler(CommandHandler("unban", unban))
    application.add_handler(CommandHandler("setdes", set_description))
    application.add_handler(CommandHandler("promote", promote))
    application.add_handler(CommandHandler("demote", demote))
    application.add_handler(CommandHandler("admins", admins))
    application.add_handler(CommandHandler("delpic", delete_pic))
    application.add_handler(CommandHandler("setpic", set_pic))
    application.add_handler(CommandHandler("ban", ban))
