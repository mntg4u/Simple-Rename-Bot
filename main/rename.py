import time
import os
from queue import Queue
from pyrogram import Client, filters, enums
from config import DOWNLOAD_LOCATION, CAPTION, ADMIN, SOURCE_CHANNEL, TARGET_CHANNEL
from main.utils import progress_message, humanbytes

# Queue for managing sequential uploads
file_queue = Queue()

@Client.on_message(filters.channel & filters.chat(SOURCE_CHANNEL))
async def process_message(bot, msg):
    media = msg.document or msg.audio or msg.video
    if not media:
        return

    # Skip files larger than 2GB
    if media.file_size > 2 * 1024 * 1024 * 1024:  # 2GB in bytes
        await bot.send_message(TARGET_CHANNEL, f"⚠️ File `{media.file_name}` is larger than 2GB and cannot be processed.")
        return

    # Add task to queue
    file_queue.put((msg, media))
    if file_queue.qsize() == 1:  # Start processing if no other tasks
        await process_queue(bot)


async def process_queue(bot):
    while not file_queue.empty():
        msg, media = file_queue.get()
        await handle_file(bot, msg, media)


async def handle_file(bot, msg, media):
    sts = await bot.send_message(TARGET_CHANNEL, f"📥 Downloading `{media.file_name}`...")

    # Download file
    c_time = time.time()
    downloaded = await msg.download(progress=progress_message, progress_args=("Downloading...", sts, c_time))
    filesize = humanbytes(media.file_size)

    # Prepare caption
    if CAPTION:
        try:
            cap = CAPTION.format(file_name=media.file_name, file_size=filesize)
        except Exception as e:
            await sts.edit(f"⚠️ Error in caption format: {e}")
            return
    else:
        cap = f"{media.file_name}\n\n💽 Size: {filesize}"

    # Handle thumbnail
    og_thumbnail = None
    if media.thumbs:
        try:
            og_thumbnail = await bot.download_media(media.thumbs[0].file_id)
        except Exception as e:
            print(f"Error downloading thumbnail: {e}")

    # Upload file
    await sts.edit("📤 Uploading...")
    c_time = time.time()
    try:
        await bot.send_document(
            TARGET_CHANNEL,
            document=downloaded,
            thumb=og_thumbnail,
            caption=cap,
            progress=progress_message,
            progress_args=("Uploading...", sts, c_time),
        )
    except Exception as e:
        await sts.edit(f"⚠️ Upload failed: {e}")
        return

    # Cleanup
    try:
        if og_thumbnail:
            os.remove(og_thumbnail)
        os.remove(downloaded)
    except Exception as e:
        print(f"Error during cleanup: {e}")

    await sts.delete()






