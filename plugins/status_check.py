import random
import shutil
from locale import currency
import pandas as pd
import re

from PIL import Image
from pyrogram.client import Client
from pyrogram import filters
from functools import partial
import logging
from typing import Union
import httpx
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import PeerIdInvalid
from imgurpython import ImgurClient
import openpyxl
from openpyxl import load_workbook
from openpyxl_image_loader import SheetImageLoader
import requests
import os

import get_pics_paths


@Client.on_message(group=-1)
async def status_check(client, message):
    user = client.database.get_user(message.from_user.id)
    if user is not None:
        def validate_product(
                name: str = None,
                cost: Union[int, float] = None,
                currency: str = None
        ) -> tuple:
            is_name_valid = False
            is_cost_valid = False

            if name:
                if (len(name) < 16) & (len(name) >= 1):
                    is_name_valid = True

            if cost:
                if (999 > cost) & (cost > 1):
                    is_cost_valid = True

            return {
                'valid': is_name_valid and is_cost_valid,
                'name': is_name_valid,
                'cost': is_cost_valid
            }

        def _parse_cost(cost: str):
            return float(
                re.match(
                    r'(\d{1,3}[,\\.]?(\d{1,2})?)',
                    cost
                )[0].replace(',', '.')
            )

        search = partial(re.search, string=user.status)
        if search('^add_by_excel$'):
            print('got_here')
            imgur_client = ImgurClient(
                client.config['imgur']['client_id'],
                client.config['imgur']['client_secret']
            )
            if message.document:
                # Check if the document is an Excel file
                if message.document.mime_type == "application/vnd.openxmlformats-" \
                                                 "officedocument.spreadsheetml.sheet":
                    # Download the Excel file
                    print('found excel')
                    file_id = message.document.file_id
                    bot_token = client.config['pyrogram']['bot_token']
                    r = ''
                    try:
                        async with httpx.AsyncClient() as http_client:
                            r = await http_client.get(
                                f'https://api.telegram.org/bot{bot_token}/getFile',
                                params={'file_id': message.document.file_id}
                            )
                            print(r.json())
                    except Exception as e:
                        print(f"Error downloading the file: {e}")
                        return
                    print('file downloaded')

                    file_path = '{}/file/bot{}/{}'.format(
                        'https://api.telegram.org',
                        bot_token,
                        r.json()['result']['file_path']
                    )
                    channels_data = str(message.document.file_name)
                    channels_data = channels_data.replace(".xlsx", "")
                    print(f"reading excel at {file_path}, this may take some time..")
                    try:
                        df = pd.read_excel(file_path)
                    except Exception as e:
                        print(f"Error reading Excel file: {e}")
                        return
                    print("excel reading  complete")

                    print("inserting products to database")
                    # Iterate over rows
                    flag = True
                    client_id = client.config['imgur']['client_id']
                    response = requests.get(file_path)
                    response.raise_for_status()
                    with open(r.json()['result']['file_path'], 'wb') as file:
                        file.write(response.content)
                    pxl_doc = openpyxl.load_workbook(r.json()['result']['file_path'])
                    print('file opened')
                    ws = pxl_doc.worksheets[0]
                    with_pics = False
                    if ws._images:
                        with_pics = True
                    added = 0

                    # calling the image_loader
                    image_loader = SheetImageLoader(ws)
                    print('got to loop')
                    flag2 = False
                    for index, row in df.iterrows():
                        name = row['name']
                        name = name.replace("\n", "-")
                        print(name)
                        cost = row['cost']
                        print(cost)
                        product_description = row['description']
                        print(index)
                        if with_pics:
                            img = image_loader.get(f'D{index + 2}')
                            img.save('documents/img.jpg')
                        else:
                            if not flag2:
                                collection_dir = "C:/Users/Eyas1/PycharmProjects/YupooScraper/" + row["photo"].replace("\\", "/")
                                collection_dir = collection_dir.split("/")[:-1].join("/")
                                flag2 = True
                            img = Image.open("C:/Users/Eyas1/PycharmProjects/YupooScraper/" + row["photo"])
                            img.save('documents/img.jpg')
                        hidden_link = row['hidden_link']
                        product_code = row['product_code']
                        collection_code = row['collection_code']
                        sizes = row['sizes']
                        collection = client.database.get_collection(collection_code)
                        if not collection:
                            client.database.insert_collection(collection_code, channels_data, message.from_user.id)
                        # try:
                        #  img_data_bytes=int(img_data).to_bytes(4, byteorder='big')
                        # img_data_bytes64 = base64.b64encode(img_data_bytes).decode('utf-8')
                        # img_binary = base64.b64decode(img_bytes)
                        # except Exception as e:
                        # print(f"Error decoding image data: {e}")
                        # continue
                        response = imgur_client.upload_from_path('documents/img.jpg')
                        link = response['link']
                        os.remove('documents/img.jpg')
                        validation = validate_product(name, cost)
                        if validation['valid']:
                            random_product_id = client.database.add_product(
                                name,
                                cost,
                                product_description,
                                link,
                                message.from_user.id,
                                hidden_link,
                                product_code,
                                collection_code,
                                sizes
                            )
                        if random_product_id:
                            added += 1
                            print(f'product {name} added')
                            client.database.insert_product_to_collection(collection_code, random_product_id)
                        else:
                            flag = False

                    more_pics = get_pics_paths.find_pictures_without_prefixes(collection_dir)
                    random.shuffle(more_pics)
                    for i, pic_path in enumerate(more_pics):
                        if i > 10:
                            break
                        img = Image.open(pic_path)
                        img.save("documents/img.jpg")
                        response = imgur_client.upload_from_path('documents/img.jpg')
                        pic_link = response['link']
                        os.remove('documents/img.jpg')
                        client.database.add_picture_to_collection(pic_link)
                    if flag:
                        client.database.set_user_status(
                            message.from_user.id,
                            'start'
                        )
                        os.remove(r.json()['result']['file_path'])
                        shutil.rmtree(collection_dir)
                        if added > 0:
                            await message.reply(client.plate(
                                'products_added_successfully', num=added
                            ))

                    else:
                        await message.reply(client.plate(
                            'product_not_added'
                        ))

        search = partial(re.search, string=user.status)
        if search('^add_product$'):
            if message.photo:
                imgur_client = ImgurClient(
                    client.config['imgur']['client_id'],
                    client.config['imgur']['client_secret']
                )

                try:
                    p = message.caption.split('\n')
                    product_name = p[0]
                    product_cost = _parse_cost(p[1])
                    product_description = p[2]
                    if len(p) > 3:
                        hidden_link = p[3]
                        product_code = p[4]
                    else:
                        hidden_link = ''
                        product_code = ''
                    bot_token = client.config['pyrogram']['bot_token']

                    async with httpx.AsyncClient() as http_client:
                        r = await http_client.get(
                            f'https://api.telegram.org/bot{bot_token}/getFile',
                            params={'file_id': message.photo.file_id}
                        )

                        img = imgur_client.upload_from_url(
                            '{}/file/bot{}/{}'.format(
                                'https://api.telegram.org',
                                bot_token,
                                r.json()['result']['file_path']
                            )
                        )

                except Exception:
                    await message.reply(client.plate('product_not_added'))

                else:
                    validation = validate_product(product_name, product_cost)
                    if validation['valid']:
                        random_product_id = client.database.add_product(
                            product_name,
                            product_cost,
                            product_description,
                            img['link'],
                            message.from_user.id,
                            hidden_link,
                            product_code
                        )

                        if random_product_id:
                            client.database.set_user_status(
                                message.from_user.id,
                                'start'
                            )

                            await message.reply(
                                client.plate('product_added'),
                                reply_markup=InlineKeyboardMarkup([[
                                    InlineKeyboardButton(
                                        client.plate('ask_channel_share'),
                                        callback_data='channel_product_share '
                                                      + random_product_id
                                    )
                                ],
                                    [InlineKeyboardButton(
                                        client.plate('add_another_product'),
                                        callback_data='add_product'
                                    )], [InlineKeyboardButton(
                                        client.plate('back'),
                                        callback_data=f'show_products'
                                    )]])
                            )

                        else:
                            await message.reply(client.plate(
                                'product_not_added'
                            ))


                    else:
                        if not validation['name']:
                            msg = 'product_name_too_long'
                        elif not validation['cost']:
                            msg = 'product_cost_out_of_range'
                        else:
                            msg = None

                        if msg:
                            await message.reply(client.plate(msg))
            else:
                await message.reply(client.plate('photo_required'))

        if x := search(r'modify_product (name|cost) (\S+)'):
            modify_type = x.group(1)
            product_id = x.group(2)
            name = None
            cost = None

            if modify_type == 'name':
                name = True
            elif modify_type == 'cost':
                try:
                    cost = _parse_cost(message.text)
                except Exception:
                    pass

            if name:
                v = validate_product(name=message.text)
            elif cost:
                v = validate_product(cost=cost)
            else:
                v = None

            if v:
                if v['valid']:
                    if modify_type == 'name':
                        client.database.set_product_name(
                            product_id, message.text
                        )
                    elif modify_type == 'cost':
                        client.database.set_product_cost(
                            product_id, cost
                        )

                    client.database.set_user_status(
                        message.from_user.id,
                        'start'
                    )
                    await message.reply(client.plate('product_modified'))
                else:
                    await message.reply(client.plate(
                        'product_not_modified',
                        type=modify_type
                    ))
            else:
                await message.reply(client.plate(
                    'product_not_modified',
                    type=modify_type
                ))

        if x := search(r'create_custom_offer 0 (\S+)'):
            product_id = x.group(1)
            product = client.database.get_product_by_id(product_id)

            if product is not None:
                if product.seller_id == message.from_user.id:
                    try:
                        user = await client.get_users(
                            int(
                                message.text
                            ) if message.text.isdigit() else message.text
                        )
                    except PeerIdInvalid:
                        await message.reply(client.plate(
                            'user_not_registered'
                        ))
                    else:
                        user_db = client.database.get_user(user.id)
                        if user_db is not None:
                            client.database.set_user_status(
                                message.from_user.id,
                                f'create_custom_offer 1 {product_id} {user.id}'
                            )

                            await message.reply(client.plate(
                                'get_username_success'
                            ))
                        else:
                            await message.reply(client.plate(
                                'user_not_registered'
                            ))
                else:
                    await message.reply(client.plate('product_not_owned'))
            else:
                await message.reply(client.plate('product_not_valid'))

        if x := search(r'create_custom_offer 1 (\S+) (\d+)'):
            product_id = x.group(1)
            buyer_id = x.group(2)
            product = client.database.get_product_by_id(product_id)

            if product is not None:
                if product.seller_id == message.from_user.id:
                    random_offer_id = client.database.insert_offer(
                        product_id,
                        message.from_user.id,
                        buyer_id,
                        _parse_cost(message.text)
                    )

                    if random_offer_id:
                        try:
                            seller = await client.get_users(
                                message.from_user.id
                            )
                            buyer = await client.get_users(buyer_id)

                            await client.send_message(
                                buyer_id,
                                client.plate(
                                    'offer_received',
                                    seller=seller.first_name,
                                    product=product.name
                                ),
                                reply_markup=InlineKeyboardMarkup([[
                                    InlineKeyboardButton(
                                        client.plate('use_offer'),
                                        url='t.me/{}?start=use_offer_{}'
                                            .format(
                                            client.config['bot']['username'],
                                            random_offer_id
                                        )
                                    )
                                ]])
                            )
                        except PeerIdInvalid:
                            await message.reply(client.plate(
                                'offer_not_received_because_bot_blocked'
                            ))
                        except Exception as e:
                            await message.reply(client.plate(
                                'offer_not_received_general'
                            ))
                            logging.error(e, exc_info=True)
                        else:
                            client.database.set_user_status(
                                message.from_user.id,
                                'start'
                            )

                            await message.reply(client.plate(
                                'offer_created_success',
                                name=buyer.first_name
                            ))
                    else:
                        await message.reply(client.plate(
                            'offer_created_error'
                        ))
                else:
                    await message.reply(client.plate('product_not_owned'))
            else:
                await message.reply(client.plate('product_not_valid'))
