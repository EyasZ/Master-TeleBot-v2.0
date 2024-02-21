from os import name
from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_callback_query(filters.regex('^show_cart$'))
async def show_cart(client, callback):
    user = client.database.get_user(callback.from_user.id)
    cart = client.database.get_user_cart(callback.from_user.id)
    products = []

    if user is not None and cart is not None:
        
        if cart.products != '':
            await callback.answer()
            products_data = cart.products
            products_id_array = products_data.split(',')
            for i in range(len(products_id_array)):
                products_id_array[i]=products_id_array[i].replace('p ','')
                products.append(client.database.get_product_by_id(products_id_array[i]))

            keyboard_menu = []
        # back to cart button needs to be added
            if len(products) > 0:
                seller = client.database.get_user(products[0].seller_id)
                sum = 0
                for product in products:
                    sum += int(product.cost)
                    keyboard_menu.append([InlineKeyboardButton(
                        client.plate('cart_product_info',name=product.name, cost=product.cost,currency=client.plate(seller.currency)),
                        callback_data='show_product_in_cart {}'.format(product.id)
                    )])
                keyboard_menu.append([InlineKeyboardButton(
                     client.plate('pay_total', currency=client.plate(seller.currency), total = sum),
                        
                        callback_data='buy_cart'
                    )])
                keyboard_menu.append([InlineKeyboardButton(
                        client.plate('empty_cart_now'),
                        callback_data='empty_cart'
                    )])
          
            

            await callback.edit_message_text(
                client.plate('your_cart'),
                reply_markup=InlineKeyboardMarkup(keyboard_menu)
            )

        else:
            await callback.edit_message_text(
                client.plate('choose_store'),
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        client.plate('go_shopping'),
                        url='t.me/TeleShopsBot/Testoapp'
                    )
                ]])
            )
    else:
        await client.send_message(
            callback.from_user.id,
            client.plate('user_not_valid')
        )
