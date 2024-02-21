from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_callback_query(filters.regex(r'ask_buyer_username (\S+)'))
async def ask_buyer_username(client, callback):
    product = (client.database.get_product_by_id(callback.matches[0].group(1)))

    if product is not None:
        if product.seller_id == callback.from_user.id:
            await callback.answer()
            client.database.set_user_status(
                callback.from_user.id,
                'create_custom_offer 0 {}'.format(product.id)
            )
            await callback.edit_message_text(
                client.plate('ready_to_username'),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(
                        client.plate('back'),
                        callback_data='make_custom_offer'
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
