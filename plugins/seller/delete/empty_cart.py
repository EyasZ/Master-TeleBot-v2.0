from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_callback_query(filters.regex(r'empty_cart'))
async def empty_cart(client, callback):
   
   if client.database.empty_cart(callback.from_user.id):
     await callback.edit_message_text(
                client.plate('cart_emptied'),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(
                        client.plate('back'),
                        callback_data='show_cart'
                    )]
                ])
            )

   else:
     await callback.edit_message_text(client.plate('empty_cart_error'),
                                 reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(
                        client.plate('back'),
                        callback_data='show_cart'
                    )]
                ]))
    