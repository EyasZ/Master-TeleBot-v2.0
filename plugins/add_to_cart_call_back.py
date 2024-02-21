from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_callback_query(filters.regex(r'^add2cart_cb_(\S+)$'))
async def start_add_to_cart(client, callback):
    product_id = callback.data.split("_")[-1]
    product = client.database.get_product_by_id(product_id)
    cart = client.database.get_user_cart(callback.from_user.id)
    productsData = cart.products
    productsIds = productsData.split(',')
    last_added = client.database.get_product_by_id(productsIds[len(productsIds) - 1].replace('p ', ''))
    if last_added:
        if last_added.seller_id != product.seller_id:
            await client.send_message(
                callback.from_user.id,
                client.plate('different_seller_error', product_name=product.name),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(
                        client.plate('show_cart'),
                        callback_data='show_cart'
                    )]
                ])
            )
            return

    if product is not None:
        user_id = callback.from_user.id
        # user_cart = client.database.get_user_cart(user_id)

        # Add the product to the user's shopping cart
        if client.database.add_product_to_cart(user_id, product_id):
            await callback.message.edit_text(
                client.plate('add_product_to_cart_success', product_name=product.name),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(
                        client.plate('show_cart'),
                        callback_data='show_cart'
                    )]
                ])
            )
    else:
        await client.send_message(callback.from_user.id, client.plate('add_product_to_cart_error'), alert=True)
    await callback.answer()
