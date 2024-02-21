from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_callback_query(filters.regex('^seller_menu$'))
async def seller_menu_callback(client, callback):
    user = (client.database.get_user(callback.from_user.id))
    if user is not None:
        if user.is_seller:
            await callback.answer()
            await callback.edit_message_text(
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
            await client.send_message(
                callback.from_user.id,
                client.plate('not_seller_error'),
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        client.plate('become_a_seller'),
                        url='https://eyas12ez.wixsite.com/my-site-2'
                    )
                ]])
            )
    else:
        await client.send_message(
            callback.from_user.id,
            client.plate('user_not_valid')
        )
