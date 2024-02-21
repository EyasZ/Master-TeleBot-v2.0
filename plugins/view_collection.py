import re
from os import name
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


'''@Client.on_callback_query()
async def print_callback_data(client, callback_query):
    # Print the callback data
    print(f"Received callback data: {callback_query.data}")

    # It's good practice to answer the callback query
    # This stops the loading spinner on the button
    await callback_query.answer()'''


@Client.on_callback_query(filters.regex(r'^(next|prev)_(\S+)_(\S+)_(\S+)$'))
async def handle_buttons(client, callback_query):
    action, product_id, current_index_str, collection_len_str = callback_query.data.split("_")
    current_index, collection_len = int(current_index_str), int(collection_len_str)

    # Retrieve the collection from the database
    product = client.database.get_product_by_id(product_id)
    collection = client.database.get_products_by_collection_code(product.collection_code)

    # Update the current index based on the action
    if action == "next":
        current_index = (current_index + 1) % collection_len
    elif action == "prev":
        current_index = (current_index - 1) % collection_len

    # Get the seller information
    seller = await client.get_users(collection[current_index].seller_id)

    # Prepare the message text with product information
    product_info_text = client.plate(
        'product_info',
        photo_link=collection[current_index].photo_link,
        name=collection[current_index].name,
        description=collection[current_index].description,
        cost=collection[current_index].cost
    )

    # Check for the seller's username
    seller_info_text = "" if seller.username else str(client.plate('no_username_found'))

    # Edit the message with the new product information and updated buttons
    await callback_query.message.edit_text(
        f"{product_info_text}\n",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Previous",
                                     callback_data=f"prev_{collection[0].id}_{current_index}_{len(collection)}"),
                InlineKeyboardButton(
                    "View more pictures",
                    callback_data=f'view_pics_{collection[current_index].collection.code}'
                ),
                InlineKeyboardButton("Next", callback_data=f"next_{collection[0].id}_{current_index}_{len(collection)}")
            ],
            [InlineKeyboardButton(
                    "Add model to cart 🛒",
                    callback_data=f'add2cart_cb_{collection[current_index].id}'
                )]
        ])
    )

    # Optionally, you can answer the callback query to stop the loading spinner on the button
    await callback_query.answer()


@Client.on_callback_query(filters.regex(r'^view_pics_(\S+)$') | filters.regex(r'^(prev_|next_)$'))
async def view_more_pics(client, callback_query):
    collection_code = callback_query.data.split("_")[-1]
    collection = client.database.get_collection(collection_code)
    products = client.database.get_products_by_collection_code(collection_code)
    product_info_text = client.plate(
        'view_pics_text',
        photo_link=collection.more_pics[0]
    )
    await callback_query.message.edit_text(
        f"{product_info_text}\n",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Previous",
                                     callback_data=f"prevP_{collection[0].id}_0_{len(collection)}"),
                InlineKeyboardButton(
                    "Choose a model",
                    callback_data=f"next_{products[0].id}_0_{len(products)}"
                ),
                InlineKeyboardButton("Next", callback_data=f"nextP_{products[0].id}_0_{len(products)}")
            ]
        ])
    )
    await callback_query.answer()


@Client.on_callback_query(filters.regex(r'^(nextP|prevP)_(\S+)_(\S+)_(\S+)$'))
async def handle_pv_buttons(client, callback_query):
    action, product_id, current_index_str, collection_pics_len_str = callback_query.data.split("_")
    current_index, collection_pics_len = int(current_index_str), int(collection_pics_len_str)
    product = client.database.get_product_by_id(product_id)
    collection = client.database.get_collection(product.collection_code)

    # Update the current index based on the action
    if action == "nextP":
        current_index = (current_index + 1) % collection_pics_len
    elif action == "preP":
        current_index = (current_index - 1) % collection_pics_len

    # Prepare the message text with product information
    product_info_text = client.plate(
        'view_pics_text',
        photo_link=collection.more_pics[current_index]
    )

    # Edit the message with the new product information and updated buttons
    await callback_query.message.edit_text(
        f"{product_info_text}\n",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Previous",
                                     callback_data=f"prevP_{product.id}_{current_index}_{len(collection.more_pics)}"),
                InlineKeyboardButton(
                    "Choose a model",
                    callback_data=f"next_{product.id}_0_{collection.count}"
                ),
                InlineKeyboardButton("Next", callback_data=f"nextP_{product.id}_{current_index}_{len(collection.more_pics)}")
            ]
        ])
    )

    # Optionally, you can answer the callback query to stop the loading spinner on the button
    await callback_query.answer()


async def view_collection(client, message, collection_code):
    collection = client.database.get_products_by_collection_code(collection_code)
    current_index = 0
    seller = await client.get_users(collection[current_index].seller_id)
    try:
        await client.send_message(
            message.from_user.id,
            str(client.plate(
                'product_info',
                photo_link=collection[current_index].photo_link,
                name=collection[current_index].name,
                description=collection[current_index].description,
                cost=collection[current_index].cost
            )) + '\n\n' + (str(client.plate('no_username_found')) if not seller.username else ''),
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("Previous",
                                         callback_data=f"prev_{collection[0].id}_{current_index}_{len(collection)}"),
                    InlineKeyboardButton(
                        'Add to cart 🛒',
                        callback_data=f'add2cart_cb_{collection[current_index].id}'
                    ),
                    InlineKeyboardButton("Next",
                                         callback_data=f"next_{collection[0].id}_{current_index}_{len(collection)}")
                ]
            ])
        )

    except Exception as e:
        await message.reply(
            f"<b>Something went wrong</b>")
