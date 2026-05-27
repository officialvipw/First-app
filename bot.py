import os
import re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# API Credentials (Ye sab Render ke Environment Variables me dalna hoga)
API_ID = int(os.environ.get("API_ID", "12345"))
API_HASH = os.environ.get("API_HASH", "your_api_hash_here")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token_here")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1001234567890")) # Aapke channel ki ID

bot = Client("AutoFilterBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        f"Hi **{message.from_user.mention}**!\n\n"
        "Main ek Auto Filter Bot hoon. Mujhe channel me maujood kisi bhi file ya photo ka naam bhejein, "
        "main dhoondh kar aapko direct link de dunga."
    )

@bot.on_message(filters.text & filters.private)
async def filter_search(client, message):
    query = message.text.strip().lower()
    sent_msg = await message.reply_text("🔍 **Channel me dhoondh raha hoon...**")
    
    found_files = []
    
    # Channel ke purane messages me keyword search karne ke liye loop
    async for msg in client.get_chat_history(CHANNEL_ID, limit=100):
        caption = ""
        if msg.caption:
            caption = msg.caption.lower()
        elif msg.text:
            caption = msg.text.lower()
            
        # Agar keyword match ho jata hai
        if query in caption or (msg.document and query in msg.document.file_name.lower()):
            # Direct post link generate karna
            link = f"https://t.me{str(CHANNEL_ID)[4:]}/{msg.id}"
            file_title = msg.document.file_name if msg.document else "Photo/Media File"
            found_files.append((file_title, link))
            
    if not found_files:
        await sent_msg.edit(f"❌ Maaf ji, **'{query}'** naam ki koi file channel me nahi mili.")
        return

    # User ko button format me results bhejna
    buttons = []
    for title, link in found_files[:5]: # Max 5 results dikhane ke liye
        buttons.append([InlineKeyboardButton(text=f"📂 {title[:25]}...", url=link)])
        
    await sent_msg.delete()
    await message.reply_text(
        text=f"✅ Mujhe **'{query}'** ke liye ye files mili hain:\nNiche diye link par click karke direct channel par jayein.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

print("Bot successfully started...")
bot.run()
