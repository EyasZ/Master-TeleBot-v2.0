from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_callback_query(filters.regex('^make_custom_offer'))
async def make_custom_offer(client, callback):
    user = (client.database.get_user(callback.from_user.id))

    if user is not None:
        if user.is_seller:
            await callback.answer()

            products = client.database.get_products_by_user_id(
                callback.from_user.id
            )

            keyboard_menu = []
            i = 0
            for product in products:
                i += 1
                keyboard_menu.append([InlineKeyboardButton(
                    product.name,
                    callback_data='ask_buyer_username {}'.format(product.id)
                )])

            keyboard_menu.append(
                [InlineKeyboardButton(
                    client.plate('back'),
                    callback_data='seller_menu'
                )]
            )

            await callback.edit_message_text(
                client.plate(
                    'your_products'
                ) if i > 0 else client.plate('no_product_owned'),
                reply_markup=InlineKeyboardMarkup(keyboard_menu)
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
