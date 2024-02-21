from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


@Client.on_inline_query(filters.regex(r'share_product (\S+)'))
async def inline_product_share(client, inline_query):
    product = client.database.get_product_by_id(
        inline_query.matches[0].group(1)
    )

    if product is not None:
        seller = await client.get_users(product.seller_id)

        await inline_query.answer(
            results=[InlineQueryResultArticle(
                title=product.name,
                description='{}€'.format(product.cost),
                input_message_content=InputTextMessageContent(
                    str(client.plate(
                        'product_info',
                        photo_link=product.photo_link,
                        name=product.name,
                        description=product.description,
                        cost=product.cost
                    ))
                    + '\n\n' + str(client.plate(
                        'no_username_found'
                    ) if not seller.username else '')
                ),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(
                            '🗣 Speak to him',
                            url=f't.me/{seller.username}'
                        )] if seller.username else [],
                        [InlineKeyboardButton(
                            '💰 Buy',
                            url='https://t.me/{}?start=buy_{}'.format(
                                client.config['bot']['username'],
                                product.id
                            )
                        )],
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
            )],
            cache_time=1
        )
    else:
        await inline_query.answer(
            results=[
                InlineQueryResultArticle(
                    title=client.plate('no_product_found'),
                    input_message_content=InputTextMessageContent(
                        client.plate('no_product_found_description')
                    )
                )
            ],
            cache_time=1
        )
