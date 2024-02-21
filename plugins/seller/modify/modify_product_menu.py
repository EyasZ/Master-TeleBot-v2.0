from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_callback_query(filters.regex(r'modify_product_menu (\S+)'))
async def show_product(client, callback):
    product = (client.database.get_product_by_id(callback.matches[0].group(1)))

    if product is not None:
        if product.seller_id == callback.from_user.id:
            product_id = product.id

            await callback.answer()
            await callback.edit_message_text(
                client.plate('modify_product_menu'),
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton(
                            client.plate('name'),
                            callback_data=f'modify_product name {product_id}'
                        ),
                        InlineKeyboardButton(
                            client.plate('cost'),
                            callback_data=f'modify_product cost {product_id}'
                        )
                    ],
                    [InlineKeyboardButton(
                        client.plate('back'),
                        callback_data=f'show_product {product_id}'
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
