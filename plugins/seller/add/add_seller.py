from pyrogram import Client, filters
from pyrogram.errors import PeerIdInvalid
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(filters.command('add_seller'))
async def add_admin(client, message):
    if int(client.config['bot']['admin_id']) != message.from_user.id:
        return

    try:
        user = await client.get_users(
            int(
                message.command[1]
            ) if message.command[1].isdigit() else message.command[1]
        )
    except PeerIdInvalid:
        await message.reply(client.plate('user_not_registered'))
    else:
        db_user = client.database.get_user(user.id)

        if db_user.is_seller == 1:
            await message.reply(client.plate('user_already_seller'))
        else:
            if client.database.set_user_is_seller(user.id, 1):
                await message.reply(client.plate(
                    'user_became_seller',
                    name=user.first_name
                ))
                await client.send_message(chat_id=user.id, 
                                text=client.plate('choose_currency'),
                                reply_markup=InlineKeyboardMarkup([[
                                    InlineKeyboardButton(
                                        client.plate('bank_note_EUR'),
                                        callback_data='set_currency '+'EUR'
                                    ),
                                       InlineKeyboardButton(
                                        client.plate('bank_note_USD'),
                                        callback_data='set_currency '
                                        + 'USD'
                                    ),
                                       InlineKeyboardButton(
                                        client.plate('bank_note_GBP'),
                                        callback_data='set_currency '
                                        + 'GBP'
                                    )
                                ]])
                            )
