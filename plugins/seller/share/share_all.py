import logging
from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from plugins import client_funcs


@Client.on_callback_query(filters.regex(r'channel_product_share_all (\S+)'))
async def channel_product_share(client, callback):
    products = client.database.get_products_by_user_id(callback.matches[0].group(1))
    count = 0
    is_collection = False
    is_admin = False
    sent_collections = []
    for product in products:
        if product is not None:
            if product.seller_id == callback.from_user.id:
                collection = client.database.get_products_by_collection_code(product.collection_code)
                if len(collection) > 1:
                    is_collection = True
                    if collection[0].collection_code in sent_collections:
                        continue

                user = client.database.get_user(callback.from_user.id)
                seller = await client.get_users(product.seller_id)

                keyboard = [
                    [InlineKeyboardButton(
                        'Add to cart 🛒',
                        url='https://t.me/{}?start=add2cart_{}'
                            .format(
                             client.config['bot']['username'],
                             product.id)
                    )]
                ]

                if user.channel_id != 0:
                    channel_id = user.channel_id
                    if is_collection:
                        products = collection
                        collection = client.database.get_collection(product.collection_code)
                        channels_data = collection.channels_data
                        if channels_data != "":
                            # automate channel creation here
                            channel_id = await client_funcs.ensure_channel_exists_and_set_admin(channels_data,
                                                                                                collection.id)
                        product = products[int(len(products)/2)]
                        keyboard = [[InlineKeyboardButton(
                            'View collection',
                            url=f"https://t.me/{client.config['bot']['username']}?start=view_collection_{product.collection_code}"
                        )]]

                    try:
                        await client.send_message(
                            channel_id,
                            str(client.plate(
                                'product_info',
                                photo_link=product.photo_link,
                                name=product.name,
                                description=product.description,
                                cost=product.cost
                            ))
                            + '\n\n' + str(client.plate(
                                'no_username_found'
                            ) if not seller.username else ''),
                            reply_markup=InlineKeyboardMarkup(keyboard)
                        )
                        sent_collections.append(product.collection_code)
                        count += 1
                    except Exception as e:
                        await callback.answer(
                            client.plate('channel_share_error'),
                            show_alert=True
                        )
                        logging.error(e, exc_info=True)

                else:
                    await callback.answer(
                        client.plate('channel_not_set'),
                        show_alert=True
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

    if count == len(products) or is_collection:
        await callback.answer(
            client.plate('channel_share_all_success', shared=count, productsNum=len(products)),
            show_alert=True
        )
    else:
        await callback.answer(
            client.plate('channel_share_all_error', shared=count, productsNum=len(products)),
            show_alert=True
        )
