from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging

logger = logging.getLogger(__name__)

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Pong! I'm alive!")

async def markdown_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
｢ Help for Formatting Module 」⚊❯❯

Markdown is a powerful formatting tool supported by Telegram.

× _italic_: Produces italic text.
× **bold**: Produces bold text.
× `code`: Produces monospaced text.
× ~strike~: Produces strikethrough text.
× --underline--: Produces underlined text.
× ||spoiler||: Produces spoiler text.
× [hyperlink](someurl): Creates a hyperlink.
× [My Button](buttonurl://example.com): Creates a button.
"""
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    ids = f"Chat ID: {chat.id}\nUser ID: {user.id}"
    if update.message.reply_to_message:
        ids += f"\nReplied User ID: {update.message.reply_to_message.from_user.id}"
    await update.message.reply_text(ids)

def setup_misc_handlers(application: Application):
    application.add_handler(CommandHandler("ping", ping))
    application.add_handler(CommandHandler("markdownhelp", markdown_help))
    application.add_handler(CommandHandler("id", get_id))
