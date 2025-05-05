from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging

logger = logging.getLogger(__name__)

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
× [button 1](buttonurl://example.com:same): Places buttons on the same row.

Fillings:
× {id}: Channel ID.
× {title}: Channel title.
× {username}: Channel username.
× {date}: Current date.
× {time}: Current time.
"""
    await update.message.reply_text(help_text, parse_mode="Markdown")

def setup_formatting_handlers(application: Application):
    application.add_handler(CommandHandler("markdownhelp", markdown_help))
