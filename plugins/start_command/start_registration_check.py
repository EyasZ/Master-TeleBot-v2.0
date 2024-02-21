from pyrogram.client import Client
from pyrogram import filters


@Client.on_message(filters.regex('^/start$'), group=-1)
async def on_start_user_registration_check(client, message):
    user = client.database.get_user(message.from_user.id)
    query = None

    if user is None:
       
        query = client.database.add_user(
            message.from_user.id,
            message.from_user.first_name
        )
        user = client.database.get_user(message.from_user.id)
       
        

    if user  is None and not query:
        await message.reply(client.plate('registration_fail'))
