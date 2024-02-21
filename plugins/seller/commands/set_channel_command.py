from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import ChannelPrivate


@Client.on_message(filters.command('set_channel'))
async def set_channel_command(client, message):
    user = (client.database.get_user(message.from_user.id))
    if user is not None:
        if user.is_seller:
            if message.reply_to_message:
                try:
                    bot_member = await client.get_chat_member(
                        message.reply_to_message.forward_from_chat.id,
                        'me'
                    )
                except ChannelPrivate:
                    await message.reply(client.plate('channel_invalid'))
                else:
                        if client.database.set_user_channel_id(
                            message.from_user.id,
                            message.reply_to_message.forward_from_chat.id
                        ):
                            reply_message = message.reply_to_message
                            await message.reply(client.plate(
                                'set_channel_success',
                                title=reply_message.forward_from_chat.title
                            ))
                        else:
                            await message.reply(
                                client.plate('set_channel_error')
                            )
                    
            else:
                await message.reply(client.plate('no_channel_on_reply'))
        else:
            await message.reply(
                client.plate('not_seller_error'),
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        client.plate('become_a_seller'),
                        url='https://eyas12ez.wixsite.com/my-site-2'
                    )
                ]])
            )
    else:
        await message.reply(client.plate('user_not_valid'))
