import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN
from admins import setup_admins_handlers
from antiforward import setup_antiforward_handlers
from autocaption import setup_autocaption_handlers
from autoforward import setup_autoforward_handlers
from cleaner import setup_cleaner_handlers
from connection import setup_connection_handlers
from formatting import setup_formatting_handlers
from greet import setup_greet_handlers
from locks import setup_locks_handlers
from misc import setup_misc_handlers
from network import setup_network_handlers
from pins import setup_pins_handlers
from post import setup_post_handlers
from purge import setup_purge_handlers
from replace import setup_replace_handlers
from broadcast import setup_broadcast_handlers
from stats import setup_stats_handlers

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Help", callback_data="help")],
        [InlineKeyboardButton("About", callback_data="about")],
        [InlineKeyboardButton("Support Chat", url="https://t.me/MySupportChat")],
        [InlineKeyboardButton("Add me to a Channel", url=f"https://t.me/MyChannelBot?startchannel")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to MyChannelBot! Choose an option:", reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "help":
        keyboard = [
            [InlineKeyboardButton("Admins", callback_data="help_admins"), InlineKeyboardButton("AntiForward", callback_data="help_antiforward")],
            [InlineKeyboardButton("AutoCaption", callback_data="help_autocaption"), InlineKeyboardButton("AutoForward", callback_data="help_autoforward")],
            [InlineKeyboardButton("Cleaner", callback_data="help_cleaner"), InlineKeyboardButton("Connection", callback_data="help_connection")],
            [InlineKeyboardButton("Formatting", callback_data="help_formatting"), InlineKeyboardButton("Greet", callback_data="help_greet")],
            [InlineKeyboardButton("Locks", callback_data="help_locks"), InlineKeyboardButton("Misc", callback_data="help_misc")],
            [InlineKeyboardButton("Network", callback_data="help_network"), InlineKeyboardButton("Pins", callback_data="help_pins")],
            [InlineKeyboardButton("Post", callback_data="help_post"), InlineKeyboardButton("Purge", callback_data="help_purge")],
            [InlineKeyboardButton("Replace", callback_data="help_replace"), InlineKeyboardButton("Back", callback_data="start")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Select a module to view help:", reply_markup=reply_markup)
    elif query.data == "about":
        about_text = """
｢ About 」⚊❯❯

MyChannelBot is a highly capable bot designed to help you manage your channels with ease, offering a range of additional features that you won't find in other channel bots.

Version: 1.0.0
Developer: @MyBotDeveloper
Support: @MySupportChat
Updates: @MyUpdatesChannel
Server: Hosted by @MyServerProvider. Powered by @MyHostingService
📝 Language & 🧰 Framework: Python - python-telegram-bot!
💾 Database: MongoDB

Highly inspired by the best and most popular channel bots out there.
Online since 01/05/2025!

Privacy Policy:
> If you use MyChannelBot for any purpose, you agree to the terms and conditions written on /privacy which is subject to change any time at any moment!
> MyChannelBot is highly customized for @MyUpdatesChannel!

Made with Love in Python by @MyBotDeveloper.
"""
        await query.message.reply_text(about_text, parse_mode="Markdown")
    elif query.data == "start":
        await start(update, context)
    elif query.data.startswith("help_"):
        module = query.data.replace("help_", "")
        help_texts = {
            "admins": "｢ Help for Admins Module 」⚊❯❯\nLazy to do other stuffs of channel management?\nHere's a module to get rid off it!\n\n" + 
                      "× /settitle newtitle: Set channel title.\n" +
                      "× /kick id|username: Kick an user from the channel.\n" +
                      "× /unban id|username: Unban an user in the channel.\n" +
                      "× /setdes description: Sets new channel description.\n" +
                      "× /promote id|username: Promote an user in the channel.\n" +
                      "× /demote id|username: Demotes an admin in the channel.\n" +
                      "× /admins: Shows the cached admins list in the channel.\n" +
                      "× /delpic: To remove channel's profile picture.\n" +
                      "× /setpic: As a reply to photo to set channel's profile picture.\n" +
                      "× /ban id|username x(m/h/d/w): Bans a user from the channel.",
            "antiforward": "｢ Help for Antiforward Module 」⚊❯❯\n" + 
                           "× /antiforward mode/off: Toggles action on forwarded posts.\n" +
                           "Modes: del|on, repost, recaption\n" +
                           "× /noantiforward off: Shows or toggles no-antiforward.\n" +
                           "× /addnoantiforward | /rmnoantiforward word: Sets | Removes no-antiforward data.",
            "autocaption": "｢ Help for Autocaption Module 」⚊❯❯\n" + 
                           "× /setgap x: Set x lines of gaps.\n" +
                           "× /inlinetag mode/off: Toggles action on inline posts.\n" +
                           "× /setsticker: Set sticker for posts.\n" +
                           "× /disablepreview on/off: Toggles web preview.\n" +
                           "× /setheader format/off: Sets header on posts.",
            "autoforward": "｢ Help for Autoforward Module 」⚊❯❯\n" + 
                           "× /autoforward off/chat_id: Stop or start auto forwarding.\n" +
                           "× /forwarddel on/off: Delete original post after forwarding.\n" +
                           "× /forwardtag on/off: Keep forwarded tag.",
            "cleaner": "｢ Help for Cleaner Module 」⚊❯❯\n" + 
                       "× /cleanservice on/off: Clean service messages automatically.",
            "connection": "｢ Help for Connection Module 」⚊❯❯\n" + 
                          "× /resetall: Resets all data (Owner).\n" +
                          "× /rmchannel chat_id: Removes channel from database.\n" +
                          "× /connection: Shows current connected channel.",
            "formatting": "｢ Help for Formatting Module 」⚊❯❯\n" + 
                          "× _italic_: Produces italic text.\n" +
                          "× **bold**: Produces bold text.\n" +
                          "× [My Button](buttonurl://example.com): Creates a button.",
            "greet": "｢ Help for Greet Module 」⚊❯❯\n" + 
                     "× /greet on/off: Toggles greet on member count.\n" +
                     "× /cleangreet on/off: Toggles greet sticker cleaning.\n" +
                     "× /joinrequest on/off/decline: Manages join requests.",
            "locks": "｢ Help for Locks Module 」⚊❯❯\n" + 
                     "× /blacklist off: Shows or toggles blacklist.\n" +
                     "× /addbl word: Sets blacklist words.\n" +
                     "× /rmbl word: Removes blacklist words.",
            "misc": "｢ Help for Misc Module 」⚊❯❯\n" + 
                    "× /ping: Pings the bot.\n" +
                    "× /markdownhelp: Sends markdown help.\n" +
                    "× /id: Gets message IDs.",
            "network": "｢ Help for Network Module 」⚊❯❯\n" + 
                       "× /nchannels: Shows all network channels.\n" +
                       "× /nkick id|username: Kick user from channels.\n" +
                       "× /nbroadcast: Sends a message to network.",
            "pins": "｢ Help for Pins Module 」⚊❯❯\n" + 
                    "× /pinned: Shows current pinned message.\n" +
                    "× /unpin: Unpins the current message.\n" +
                    "× /autopin: Sets auto pin status.",
            "post": "｢ Help for Post Module 」⚊❯❯\n" + 
                    "× /post: Post a custom message.\n" +
                    "× /edit message_id: Edits a post.\n" +
                    "× /schedule interval: Schedules a message.",
            "purge": "｢ Help for Purge Module 」⚊❯❯\n" + 
                     "× /purge: Deletes messages up to replied message.\n" +
                     "× /purge X: Deletes X messages after replied message.",
            "replace": "｢ Help for Replace Module 」⚊❯❯\n" + 
                       "× /replace off: Toggles replacing words.\n" +
                       "× /addreplace word::new-word: Sets replacing words."
        }
        await query.message.reply_text(help_texts.get(module, "Help not available for this module."), parse_mode="Markdown")
        
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))

    # Setup handlers for each module
    setup_admins_handlers(application)
    setup_antiforward_handlers(application)
    setup_autocaption_handlers(application)
    setup_autoforward_handlers(application)
    setup_cleaner_handlers(application)
    setup_connection_handlers(application)
    setup_formatting_handlers(application)
    setup_greet_handlers(application)
    setup_locks_handlers(application)
    setup_misc_handlers(application)
    setup_network_handlers(application)
    setup_pins_handlers(application)
    setup_post_handlers(application)
    setup_purge_handlers(application)
    setup_replace_handlers(application)
    setup_broadcast_handlers(application)
    setup_stats_handlers(application)

    application.run_polling()

if __name__ == "__main__":
    main()
