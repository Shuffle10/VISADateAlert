from datetime import date, datetime

from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
    PeerChannel
)

import winsound

# get api credentials from https://my.telegram.org/
api_id = 123456
api_hash = 'xyz'
# this can be a random string
session_name = 'session'  


# your credentials
phone = 'your phone'
username = 'your name'
duration = 15000
freq = 500

#months to get alert 
conditions = ['AUGUST', 'MAY', 'JUNE', 'JULY', 'AUG', 'JUL']

client = TelegramClient(username, api_id, api_hash)

async def main(phone):
    await client.start()
    print("Client Created")
    if await client.is_user_authorized() == False:
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))

    me = await client.get_me()


    # telegram channel link
    entity = ''  
    


    my_channel = await client.get_entity(entity)
    offset_id = 0
    limit = 100

    @client.on(events.NewMessage(chats=my_channel))
    async def my_event_handler(event):
        print(event.raw_text)
        for month in conditions:
            if(month in (event.raw_text).upper()):
                print('Date Alert!!!!')
                winsound.Beep(freq, duration) 
        

    while True:
        history = await client(GetHistoryRequest(
            peer=my_channel,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
        if not history.messages:
            break
        messages = history.messages
        

with client:
    client.loop.run_until_complete(main(phone))
    