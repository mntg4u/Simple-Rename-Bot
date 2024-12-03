import time, os, asyncio
from pyrogram import Client, filters, enums
from config import DOWNLOAD_LOCATION, CAPTION, ADMIN, TARGET_CHANNEL
from main.utils import progress_message, humanbytes
from collections import deque

# Queue to hold incoming messages
processing_queue = deque()
processing = False  # Flag to indicate if processing is ongoing

# Automatically handle media messages in a specific channel
@Client.on_message(filters.channel & filters.chat("<your_channel_id>") & (filters.document | filters.video | filters.audio))
async def queue_media(bot, msg):
    # Add the message to the queue
    processing_queue.append(msg)
    await msg.reply_text("Your file has been added to the queue. Please wait...")

    # Start processing if not already running
    global processing
    if not processing:
        processing = True
        await process_queue(bot)

# Function to process the queue
async def process_queue(bot):
    while processing_queue:
        # Get the next message in the queue
        msg = processing_queue.popleft()

        media = msg.document or msg.audio or msg.video
        if not media:
            continue  # Skip if there's no media

        # Check file size (Telegram provides file size in bytes)
        if media.file_size > 2 * 1024 * 1024 * 1024:  # 2GB in bytes
            await msg.reply_text(f"Skipping {media.file_name} because it exceeds the 2GB limit.")
            continue

        original_name = media.file_name  # File name remains unchanged
        sts = await msg.reply_text(f"Processing {original_name}...")

        try:
            # Download the thumbnail or use a default
            dir = os.listdir(DOWNLOAD_LOCATION)
            if len(dir) == 0:
                file_thumb = await bot.download_media(media.thumbs[0].file_id) if media.thumbs else None
                og_thumbnail = file_thumb if file_thumb else "path/to/default/thumbnail.jpg"
            else:
                try:
                    og_thumbnail = f"{DOWNLOAD_LOCATION}/thumbnail.jpg"
                except Exception as e:
                    print(e)
                    og_thumbnail = "path/to/default/thumbnail.jpg"

            # Send the document with updated thumbnail
            await sts.edit(f"Uploading {original_name}...")
            c_time = time.time()
            await bot.send_document(
                TARGET_CHANNEL,
                document=media.file_id,  # Use the original file
                thumb=og_thumbnail,
                caption=CAPTION.format(file_name=original_name, file_size=humanbytes(media.file_size)) if CAPTION else f"{original_name}\n\n💽 size : {humanbytes(media.file_size)}",
                progress=progress_message,
                progress_args=("Upload Started...", sts, c_time)
            )

            # Clean up the downloaded thumbnail if it exists
            try:
                if file_thumb:
                    os.remove(file_thumb)
            except:
                pass

        except Exception as e:
            await sts.edit(f"Error: {e}")
            continue

        await sts.delete()

    global processing
    processing = False  # Mark processing as done

