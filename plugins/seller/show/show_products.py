from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_callback_query(filters.regex('^show_products$'))
async def show_products(client, callback):
    user = client.database.get_user(callback.from_user.id)

    if user is not None:
        if user.is_seller:
            await callback.answer()

            products = client.database.get_products_by_user_id(
                callback.from_user.id
            )
            keyboard_menu = [[InlineKeyboardButton(
                client.plate('add_product'), callback_data='add_products_ask'
            )]]

            if len(products) > 0:
                for product in products:
                    keyboard_menu.append([InlineKeyboardButton(
                        product.name,
                        callback_data='show_product {}'.format(product.id)
                    )])
            else:
                keyboard_menu.append([InlineKeyboardButton(
                    client.plate('no_product_owned'),
                    callback_data='no_product_owned_explanation'
                )])

            keyboard_menu.append([InlineKeyboardButton(
                client.plate('back'), callback_data='seller_menu'
            )])
            keyboard_menu.append([InlineKeyboardButton(
                client.plate('share_all'), callback_data=f'channel_product_share_all {callback.from_user.id}'
            )])

            await callback.edit_message_text(
                client.plate('your_products'),
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
