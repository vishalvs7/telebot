import configparser
import json
import asyncio
import pandas as pd

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.types import (
    PeerChannel
)

# Setting configuration values
api_id = 17335519
api_hash = 'e994fe35530b621f369df937d07d3b71'
api_hash = str(api_hash)
phone = '+917081134062'
username = "Lonewolfvs7"

# Create the client and connect
client = TelegramClient(username, api_id, api_hash)

async def main(phone):
    await client.start()
    print("Client Created")
    # Ensure you're authorized
    if await client.is_user_authorized() == False:
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))

    me = await client.get_me()

    user_input_channel = input("enter entity(telegram URL or entity id):")

    if user_input_channel.isdigit():
        entity = PeerChannel(int(user_input_channel))
    else:
        entity = user_input_channel

    my_channel = await client.get_entity(entity)

    offset = 0
    limit = 100
    all_participants = []

    while True:
        participants = await client(GetParticipantsRequest(
            my_channel, ChannelParticipantsSearch(''), offset, limit,
            hash=0
        ))
        if not participants.users:
            break
        all_participants.extend(participants.users)
        offset += len(participants.users)

    all_user_details = []
    for participant in all_participants:
        all_user_details.append(
            {"user.id": participant.id, 
            "first_name": participant.first_name, 
            "last_name": participant.last_name,
            "username": participant.username, 
            "phone": "a_"+str(participant.phone),
            "user.access_hash": participant.access_hash,
            "is_bot": participant.bot})

    #with open('user_data.json', 'w') as outfile:
    #    json.dump(all_user_details, outfile)

    filename = user_input_channel.replace("/","_").replace(":","")
    df = pd.DataFrame(all_user_details)
    df.to_csv('withphone_'+filename+'.csv', index = True) # column names ekler

with client:
    client.loop.run_until_complete(main(phone))