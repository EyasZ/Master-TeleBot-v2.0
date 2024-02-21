from pyrogram.client import Client
from pyrogram import filters


@Client.on_message(filters.command('help')) # type: ignore
async def help_command(client, message):
    msg = client.plate('user_commands')
    if message.from_user.id == int(client.config['bot']['admin_id']):
        msg = msg + '\n\n' + client.plate('admin_commands')

    await message.reply(msg)
