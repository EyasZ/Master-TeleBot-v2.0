from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_callback_query(filters.regex(r'delete_product_from_cart (\S+)'))
async def delete_product(client, callback):
    product = (client.database.get_product_by_id(callback.matches[0].group(1)))
    cart = (client.database.get_user_cart(callback.from_user.id))

   
    if product is not None:
            await callback.answer()
            current_products_data = cart.products
            ids_array=[]
            ids_array = current_products_data.split(',')
            current_products_data = ''
            flag= True
            is_removed=False
            for i in range(len(ids_array)):
                ids_array[i] = ids_array[i].replace('p ','')
             
            ids_array.remove(str(product.id))
            client.database.empty_cart(callback.from_user.id)  
            for id in ids_array:
                flag = flag & client.database.add_product_to_cart(callback.from_user.id, id)
             
            if flag:
                msg = 'product_deleted'
            else:
                msg = 'product_not_deleted'

            await callback.edit_message_text(
                client.plate(msg),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(
                        client.plate('back'),
                        callback_data='show_cart'
                    )]
                ])
            )
    else:
            await client.send_message(
                callback.from_user.id,
                client.plate('product_not_valid')
            )
    
