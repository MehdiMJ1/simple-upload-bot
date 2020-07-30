from telethon import TelegramClient , events 
import asyncio 
import time 
from telethon import TelegramClient , events ,errors
from telethon import  Button 
from telethon.utils import get_input_location
import asyncio 
import time 
import math
import datetime
from telethon.tl.types import DocumentAttributeFilename
from telethon.tl.types import Document
from os.path import splitext 
from telethon.errors import UserNotParticipantError
from telethon import functions
import os
from config import BOTTOKEN, APIID, APIHASH, DOWNLOADPATH
from hfunc import progress , time_formatter , humanbytes



client = TelegramClient('Zipper Bot',api_id = APIID,api_hash = APIHASH).start(bot_token=BOTTOKEN)

startMsg = """Hello [{}](tg://user?id={})
Welcome to Renamer Bot , With That bot , You Can Rename Files ..

To Rename Any File, send it first , then reply to the message with ( /rename file_name ).. 
"""


@client.on(events.NewMessage)
async def handler(event):

    chat_id = event.chat_id     # work 
    user_id = event.sender_id   # work
    user = (await event.get_sender())
    first_name = user.first_name

    if event.text == '/start':
        await client.send_message(
            chat_id,
            message=startMsg.format(first_name,user_id),
            buttons=[
                [Button.url('My Channel','https://t.me/icode11')]
            ])
    if '/rename' in event.text and event.is_reply:
        try: 
            await client(functions.channels.GetParticipantRequest(channel='icode11',user_id=user_id))
            file = await event.get_reply_message()
            filePAth = os.path.join(DOWNLOADPATH,str(user_id))
            reply = await event.reply('`Processing Now ..`')
            s_time = time.time()
            command, filename = event.text.split(' ')
            try:
                downloaded_file_name = await client.download_media(
                    file,
                    file=filePAth,
                    progress_callback=lambda d, t: asyncio.get_event_loop().create_task(    # progress work !!
                            progress(d, t, reply, s_time, "Downloading Now ...")
                    ))
                ext = splitext(downloaded_file_name)[1]
                reply2 = await reply.edit('Downloaded Successfully ✅')
                s_time2 = time.time()
                upload_filename = await client.send_file(
                    user_id,
                    downloaded_file_name,
                    attributes=[
                        DocumentAttributeFilename(file_name=filename+ext)
                    ],
                    progress_callback=lambda d, t: asyncio.get_event_loop().create_task(    # progress work !!
                            progress(d, t, reply2, s_time2, "Uploading Now ...")
                    ))
                await reply2.edit('Uploaded Successfully ✅')
                await reply2.delete()
            except Exception as e:
                await event.reply(e)
        except UserNotParticipantError:
            await event.reply('Sorry, You Should Join The Channel To Use THe Bot .. ')

# with client:
#     client.run_until_disconnected()

def  main():
    if not os.path.isdir(DOWNLOADPATH):
        os.mkdir(DOWNLOADPATH)

    """Start the bot."""
    print("\nBot started..\n")
    client.run_until_disconnected()


if __name__ == '__main__':
    main()
