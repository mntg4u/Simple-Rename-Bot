from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import ADMIN

# Constants for frequently used text and buttons
SOURCE_CODE_URL = "https://github.com/MrMKN/Simple-Rename-Bot"
HOW_TO_DEPLOY_URL = "https://youtu.be/oc847WvOUaI"
BOT_UPDATES_URL = "https://t.me/mkn_bots_updates"
DEVELOPER_URL = "https://github.com/MrMKN"
MASTER_1_URL = "https://t.me/Mo_Tech_YT"
MASTER_2_URL = "https://t.me/venombotupdates"

# Start Command Handler
@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(bot, msg):
    """Handles the /start command."""
    txt = (
        "This is a personal-use bot 🙏. Want your own bot? 👇 Click the source code to deploy."
    )
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🤖 SOURCE CODE", url=SOURCE_CODE_URL)],
        [InlineKeyboardButton("🖥️ How To Deploy", url=HOW_TO_DEPLOY_URL)]
    ])
    
    # If user is not ADMIN, show the deployment information
    if msg.from_user.id != ADMIN:
        return await msg.reply_text(text=txt, reply_markup=buttons, disable_web_page_preview=True)
    
    # If user is ADMIN, proceed to show bot details
    await show_start_info(bot, msg, cb=False)


# Callback Query: Start
@Client.on_callback_query(filters.regex("start"))
async def show_start_info(bot, msg, cb=True):
    """Displays the start message with bot details."""
    txt = (
        f"Hi {msg.from_user.mention}, I am a simple rename bot for personal use.\n"
        f"This bot is developed by <b><a href={DEVELOPER_URL}>MrMKN</a></b>."
    )
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🤖 Bot Updates", url=BOT_UPDATES_URL)],
        [
            InlineKeyboardButton("ℹ️ Help", callback_data="help"),
            InlineKeyboardButton("📡 About", callback_data="about")
        ]
    ])
    
    if cb:
        await msg.message.edit(text=txt, reply_markup=buttons, disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML)
    else:
        await msg.reply_text(text=txt, reply_markup=buttons, disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML)


# Callback Query: Help
@Client.on_callback_query(filters.regex("help"))
async def show_help(bot, msg):
    """Displays help information."""
    txt = (
        "To use this bot:\n"
        "- Send a file and reply with `/rename <new name>` to rename it.\n"
        "- Send a photo to set a custom thumbnail.\n"
        "- Use /view to see your current thumbnail.\n"
        "- Use /del to delete your thumbnail."
    )
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🚫 Close", callback_data="del"),
            InlineKeyboardButton("⬅️ Back", callback_data="start")
        ]
    ])
    await msg.message.edit(text=txt, reply_markup=buttons, disable_web_page_preview=True)


# Callback Query: About
@Client.on_callback_query(filters.regex("about"))
async def show_about(bot, msg):
    """Displays information about the bot."""
    me = await bot.get_me()
    txt = (
        f"<b>Bot Name:</b> {me.mention}\n"
        f"<b>Developer:</b> <a href={DEVELOPER_URL}>MrMKN</a>\n"
        f"<b>Bot Updates:</b> <a href={BOT_UPDATES_URL}>Mᴋɴ Bᴏᴛᴢ™</a>\n"
        f"<b>Masters:</b> <a href={MASTER_1_URL}>MoTech</a>, <a href={MASTER_2_URL}>MhdRzn</a>\n"
        f"<b>Source Code:</b> <a href={SOURCE_CODE_URL}>Click Here</a>"
    )
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🚫 Close", callback_data="del"),
            InlineKeyboardButton("⬅️ Back", callback_data="start")
        ]
    ])
    await msg.message.edit(text=txt, reply_markup=buttons, disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML)


# Callback Query: Close
@Client.on_callback_query(filters.regex("del"))
async def close_message(bot, msg):
    """Closes the message."""
    try:
        await msg.message.delete()
    except Exception as e:
        print(f"Failed to delete message: {e}")
