import logging
from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_callback_query(filters.regex(r'channel_product_share (\S+)'))
async def channel_product_share(client, callback):
    product = client.database.get_product_by_id(callback.matches[0].group(1))

    if product is not None:
        if product.seller_id == callback.from_user.id:
            user = client.database.get_user(callback.from_user.id)
            seller = await client.get_users(product.seller_id)

            if user.channel_id != 0:
                try:
                    await client.send_message(
                        user.channel_id,
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
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [InlineKeyboardButton(
                                    'Add to cart 🛒',
                                    url='https://t.me/{}?start=add2cart_{}'
                                    .format(
                                        client.config['bot']['username'],
                                        product.id
                                    )
                                )]
                            ]
                        )
                    )
                except Exception as e:
                    await callback.answer(
                        client.plate('channel_share_error'),
                        show_alert=True
                    )
                    logging.error(e, exc_info=True)
                else:
                    await callback.answer(
                        client.plate('channel_share_success'),
                        show_alert=True
                    )
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
