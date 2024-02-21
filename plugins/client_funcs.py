import os.path
import asyncio
import random

from telethon import TelegramClient, types, errors
from telethon.errors import UsernameNotOccupiedError
from telethon.tl.functions.channels import UpdateUsernameRequest
from telethon.tl.functions.channels import CreateChannelRequest, EditAdminRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import ChatAdminRights, InputPeerEmpty, Channel
from telethon import utils
from configparser import ConfigParser
from plate import Plate
import database as db


# configparser = ConfigParser()
# configparser.read('config.ini')
# api_id = configparser['pyrogram']['api_id']
# api_hash = configparser['pyrogram']['api_hash']
# plate = Plate(
# root=configparser['plate']['root'],
# fallback=configparser['plate']['fallback']
# )

async def ensure_channel_exists_and_set_admin(channel_name, collection_id):
    configparser = ConfigParser()
    configparser.read('config.ini')
    api_id = configparser['pyrogram']['api_id']
    api_hash = configparser['pyrogram']['api_hash']
    plate = Plate(
        root=configparser['plate']['root'],
        fallback=configparser['plate']['fallback']
    )
    async with TelegramClient('my_session', api_id, api_hash) as client:
        channel_id = ""
        database = db.Database()
        collection = database.get_collection(collection_id)
        data_array = collection.channels_data.split(": ")
        if len(data_array) > 1:
            channel_id = int(data_array[-1])
            channel = await client.get_entity(channel_id)
        if channel_id == "":
            try:
                result = await client.get_dialogs()
                channels = [dialog.entity for dialog in result if isinstance(dialog.entity, Channel)]
                # Filter out channels where you are the creator or have admin rights
                owned_channels = [channel for channel in channels if channel.creator or channel.admin_rights]

                exists = False
                for channel in owned_channels:
                    if channel_name == channel.title:
                        exists = True
                        channel_id = channel.id
                if channel_id != "":
                    print(f"Channel '{channel_name}' already exists with ID: {channel_id}")
                channel = await client.get_entity(channel_id)
            except ValueError:
                # If the channel does not exist, create it
                print(f"Channel '{channel_name}' not found. Creating it...")
                created_channel = await client(CreateChannelRequest(
                    title=channel_name.replace("@", ""),
                    about=plate("About_Channel"),
                    megagroup=False  # Set True if you want to create a supergroup instead
                ))
                channel = created_channel.chats[0]
                channel_id = channel.id
                flag = False
                i = 0
                rand = f"{random.randint(0, 9999999)}"
                while not flag:
                    try:
                        user_name = channel_name
                        user_name = "TeleBazar_" + channel_name
                        if await client(UpdateUsernameRequest(channel.id, user_name + f"{rand}")):
                            flag = True
                        else:
                            i += 1
                            rand = f"{random.randint(0, 9999999)}"
                            channel_name = channel + rand
                            if i > 3:
                                print(i)
                                return
                    except (errors.rpcerrorlist.UsernameInvalidError, errors.rpcerrorlist.UsernameOccupiedError) as e:
                        print(f"username {user_name + rand} unavailable trying again...\n")
                        if i > 5:
                            break

                print(f"New channel created with ID: {channel.id}")

                # Prepare admin rights
                admin_rights = ChatAdminRights(
                    change_info=True,
                    post_messages=True,
                    edit_messages=True,
                    delete_messages=True,
                    ban_users=True,
                    invite_users=True,
                    pin_messages=True,
                    add_admins=False,  # Assuming you do not want the bot to add other admins
                )

                # Add @TeleShopsBot as an admin
                try:
                    await client(EditAdminRequest(
                        channel=channel_id,
                        user_id='@TeleShopsBot',
                        admin_rights=admin_rights,
                        rank='bot'
                    ))
                    print("@TeleShopsBot has been made an admin in the channel.")
                    database.update_collection_channel_data(collection_id, channel.id)
                    return "@" + channel.username
                except Exception as e:
                    print(f"Failed to add @TeleShopsBot as admin. Error: {e}")
        database.update_collection_channel_data(collection_id, channel.id)
        return "@" + channel.username
