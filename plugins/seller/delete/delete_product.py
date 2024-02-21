from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_callback_query(filters.regex(r'delete_product (\S+)'))
async def delete_product(client, callback):
    product = (client.database.get_product_by_id(callback.matches[0].group(1)))

    if product is not None:
        if product.seller_id == callback.from_user.id:
            await callback.answer()

            if client.database.delete_product(product.id):
                msg = 'product_deleted'
            else:
                msg = 'product_not_deleted'

            await callback.edit_message_text(
                client.plate(msg),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(
                        client.plate('back'),
                        callback_data='show_products'
                    )]
                ])
            )
        else:
            await client.send_message(
                callback.from_user.id,
                client.plate('product_not_owned')
            )
    else:
        await client.send_message(
            callback.from_user.id,
            client.plate('product_not_valid')
        )
