from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_callback_query(filters.regex(r'show_product_in_cart (\S+)'))
async def show_product(client, callback):
    product = client.database.get_product_by_id(callback.matches[0].group(1))

    if product is not None:
        if product is not None:
            product_id = product.id

            await callback.answer()
            await callback.edit_message_text(
                client.plate(
                    'product_info',
                    photo_link=product.photo_link,
                    name=product.name,
                    description=product.description,
                    cost=product.cost
                ),
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton(
                            client.plate('remove_from_cart'),
                            callback_data=f'delete_product_from_cart_ask {product_id}'
                        ),
                         InlineKeyboardButton(
                            client.plate('back'),
                            callback_data=f'show_cart'
                        )
                    ]
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
