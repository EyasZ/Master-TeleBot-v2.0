from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(filters.command('seller'))
async def seller_menu_command(client, message):
    user = (client.database.get_user(message.from_user.id))
    if user is not None:
        if user.is_seller:
            await message.reply(
                client.plate('seller_menu'),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(
                        client.plate('show_products'),
                        callback_data='show_products'
                    )],
                    [InlineKeyboardButton(
                        client.plate('make_custom_offer'),
                        callback_data='make_custom_offer'
                    )]
                ])
            )

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
