from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_callback_query(filters.regex(r'modify_product (name|cost) (\S+)'))
async def show_product(client, callback):
    user = (client.database.get_user(callback.from_user.id))

    if user:
        if user.is_seller:
            modifying_type = callback.matches[0].group(1)
            product_id = callback.matches[0].group(2)
            product = (client.database.get_product_by_id(product_id))

            if product is not None:
                if product.seller_id == callback.from_user.id:
                    await callback.answer()
                    client.database.set_user_status(
                        callback.from_user.id,
                        f'modify_product {modifying_type} {product_id}'
                    )
                    await callback.edit_message_text(
                        client.plate(
                            'ready_to_modify',
                            type=modifying_type
                        ),
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton(
                                client.plate('back'),
                                callback_data='modify_product_menu {}'
                                .format(product_id)
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
