from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_callback_query(filters.regex(r'delete_product_from_cart_ask (\S+)'))
async def delete_product(client, callback):
    product = (client.database.get_product_by_id(callback.matches[0].group(1)))

    if product is not None:
        if product is not None:
            product_id = product.id

            await callback.answer()
            await callback.edit_message_text(
                client.plate('ask_delete_confirmation'),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(
                        client.plate('confirm_product_delete'),
                        callback_data=f'delete_product_from_cart {product_id}'
                    )],
                    [InlineKeyboardButton(
                        client.plate('back'),
                        callback_data=f'show_cart'
                    )]
                ])
            )
        else:
            await client.send_message(
                callback.from_user.id,
                client.plate('product_not_valid')
            )
    else:
        await client.send_message(
            callback.from_user.id,
            client.plate('product_not_valid')
        )
