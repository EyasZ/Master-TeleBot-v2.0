from http import client
import logging
import mysql.connector
import random
import string
from typing import Union
import time
import sqlcon
import objects
import datetime


class Database:
    def __init__(self):
        self.conn = sqlcon.connect_with_connector()
        self.c = self.conn.cursor()

    def execute(self, query: str, data: tuple = ()) -> bool:
        try:
            self.c.execute(query, data)
            self.conn.commit()
        except mysql.connector.Error as e:
            logging.error(e, exc_info=True)
            return False
        else:
            return True

    def select(self, query: str, data: tuple = ()) -> mysql.connector.cursor.MySQLCursor:
        self.c.execute(query, data)
        return self.c

    # User queries

    def add_user(self, user_id: int, user_name: str):
        a = self.execute(
            'INSERT INTO users VALUES (%s, %s, 0, 0,\'\' ,\'start\', 0,%s,%s,%s,\'Eyez\')',
            (user_id, user_name, str(user_id), str(datetime.date.today()), str(datetime.date.today()),))
        b = self.execute(
            'INSERT INTO users_carts VALUES (%s, \'\',0,%s,%s,%s,\'Eyez\')',
            (user_id, user_id, str(datetime.date.today()), str(datetime.date.today()),)
        )
        return a and b

    def update_balance(self, user_id: int, amount: float):
        user = objects.User.classFactory(self.select(
            'SELECT * FROM users WHERE id = %s',
            (user_id,)
        ).fetchone())
        sum = user.balance + amount

        return self.execute(
            'UPDATE users SET balance = %s WHERE id = %s',
            (sum, user_id,)
        )

    def get_user_cart(self, user_id: int):
        return objects.Users_cart.classFactory(self.select(
            'SELECT * FROM users_carts WHERE id = %s',
            (user_id,)
        ).fetchone())

    def empty_cart(self, user_id: int):
        return self.execute(
            'UPDATE users_carts SET products = %s WHERE id = %s',
            ('', user_id)
        )

    def set_products_in_cart(self, updated_products: str, user_id: int):
        return self.execute(
            'UPDATE users_carts SET products = %s WHERE id = %s',
            (updated_products, user_id)
        )

    def add_product_to_cart(self, user_id: int, product_id: int):
        cart = objects.Users_cart.classFactory(self.select('SELECT * FROM users_carts WHERE id = %s',
                                                           (user_id,)).fetchone())
        count = cart.count + 1
        if count == 11:
            return False
        self.set_cart_count(user_id, count)

        current_products = cart.products
        if current_products != '':
            current_products = current_products + ',p ' + str(product_id)
        else:
            current_products = 'p ' + str(product_id)

        a = self.execute(
            'UPDATE users_carts SET products = %s WHERE id = %s',
            (current_products, user_id)
        )
        b = self.execute(
            'UPDATE users_carts SET count = %s WHERE id = %s',
            (count, user_id)
        )
        return a and b

    def get_user(self, user_id: int):
        return objects.User.classFactory(self.select(
            'SELECT * FROM users WHERE id = %s',
            (user_id,)
        ).fetchone())

    def set_user_is_seller(self, user_id: int, is_seller: int):
        return self.execute(
            'UPDATE users SET is_seller = %s WHERE id = %s',
            (is_seller, user_id)
        )

    def set_user_channel_id(self, user_id: int, channel_id: int):
        return self.execute(
            'UPDATE users SET channel_id = %s WHERE id = %s',
            (channel_id, user_id)
        )

    def set_user_status(self, user_id: int, status: str):
        return self.execute(
            'UPDATE users SET status = %s WHERE id = %s',
            (status, user_id)
        )

    # Product queries
    def get_collection_pics(self, collection_id):
        return self.select(
            'SELECT more_pics FROM collections WHERE collection_id = %s',
            (collection_id,)
        ).fetone()

    def add_picture_to_collection(self, link, collection_id):
        collection_pics = self.get_collection_pics(collection_id)
        collection_pics = collection_pics + f"{link}\n"
        return self.execute(
            'UPDATE collections SET more_pics = %s WHERE id = %s',
            (collection_pics, collection_id))

    def get_products_by_collection_code(self, collection_code):
        prods = self.select(
            'SELECT * FROM products WHERE collection_code = %s',
            (collection_code,)
        ).fetchall()
        collection = []
        for prod in prods:
            collection.append(objects.Product.classFactory(prod))
        return collection

    def update_collection_channel_data(self, collection_id, data):
        collection = self.get_collection(collection_id)
        current_data = collection.channels_data
        current_data = current_data.split(": ")[0] + f": {data}"
        return self.execute(
            'UPDATE collections SET channels = %s WHERE id = %s',
            (current_data, collection_id))

    def insert_product_to_collection(self, collection_id, prod_id):
        products = self.get_products_by_collection_code(prod_id)
        collection = self.get_collection(collection_id)
        products.append(prod_id)
        a = self.execute(
            'UPDATE collections SET products = %s WHERE id = %s',
            (str(products), collection_id)
        )
        b = self.execute(
            'UPDATE collections SET count = %s WHERE id = %s',
            (collection.count + 1, collection_id)
        )
        return a and b

    def insert_collection(self, collection_id, channels_data, seller_id):
        products = ""
        return self.execute(
            'INSERT INTO collections VALUES (%s, %s,%s,0,%s,%s,%s,\'Eyez\',%s)',
            (collection_id, products, str(seller_id), collection_id, str(datetime.date.today())
             , str(datetime.date.today()), channels_data,))

    def get_collection(self, collection_id):
        return objects.Collection.classFactory(self.select(
            'SELECT * FROM collections WHERE id = %s',
            (collection_id,)
        ).fetchone())

    def add_product(
            self,
            product_name: str,
            product_cost: Union[int, float],
            product_description: str,
            product_photo_url: str,
            product_seller_id: int,
            hidden_link: str,
            product_code: str,
            collection_code: str,
            sizes: str
    ):
        while True:
            random_product_id = ''.join(random.choices(
                string.ascii_lowercase + string.digits,
                k=8
            ))
            prod = self.get_product_by_id(random_product_id)

            if prod is None:
                break
        date = str(datetime.date.today())

        x = self.execute(
            'INSERT INTO products VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\'Eyez\',%s,%s)',
            (
                random_product_id,
                product_name,
                product_cost,
                product_description,
                product_photo_url,
                product_seller_id,
                hidden_link,
                product_code,
                random_product_id,
                date,
                date,
                collection_code,
                sizes
            )
        )

        if x:
            return random_product_id
        else:
            return False

    def get_product_by_id(self, product_id: str):
        return objects.Product.classFactory(self.select(
            'SELECT * FROM products WHERE id = %s',
            (product_id,)
        ).fetchone())

    def get_products_by_user_id(self, user_id: int):
        prods = self.select(
            'SELECT * FROM products WHERE seller_id = %s',
            (user_id,)
        ).fetchall()
        products = []
        for product in prods:
            products.append(objects.Product.classFactory(product))
        return products

    def set_product_name(self, product_id: str, product_name: str):
        return self.execute(
            'UPDATE products SET name = %s WHERE id = %s',
            (product_name, product_id)
        )

    def set_product_cost(
            self,
            product_id: str,
            product_cost: Union[int, float]
    ):
        return (self.execute(
            'UPDATE products SET cost = %s WHERE id = %s',
            (product_cost, product_id)
        ))

    def set_currency(self, currency_updated: str, user_id: str):
        return self.execute('UPDATE users SET currency = %s WHERE id = %s', (currency_updated, user_id,))

    def delete_product(self, product_id: str):
        return self.execute(
            'DELETE FROM products WHERE id = %s',
            (product_id,)
        )

    # Offer queries

    def insert_offer(
            self,
            product_id: int,
            seller_id: int,
            buyer_id: int,
            cost: Union[int, float]
    ):
        while True:
            random_offer_id = ''.join(random.choices(
                string.ascii_lowercase + string.digits,
                k=8
            ))

            if self.get_offer_by_id(random_offer_id) is None:
                break
        date = str(datetime.date.today())

        x = self.execute(
            'INSERT INTO offers VALUES (%s, %s, %s, %s, %s, 1,%s,%s,%s,\'Eyez\')',
            (random_offer_id, product_id, seller_id, buyer_id, cost, random_offer_id, date, date,)
        )

        if x:
            return random_offer_id
        else:
            return False

    def get_offer_by_id(self, offer_id: str):
        return objects.Offer.classFactory(self.select(
            'SELECT * FROM offers WHERE id = %s',
            (offer_id,)
        ).fetchone())

    def set_offer_valid(self, offer_id: str, valid: int):
        return self.execute(
            'UPDATE offers SET valid = %s WHERE id = %s',
            (valid, offer_id)
        )

    def delete_offer(self, offer_id: str):
        return self.execute(
            'DELETE FROM offers WHERE id = %s',
            (offer_id,)
        )

    # Transaction queries

    def insert_transaction(
            self,
            products_ids: str,
            seller_id: int,
            buyer_id: int,
            cost: Union[int, float],
            is_offer: int,
            shipping_address: str
    ):
        while True:
            random_transaction_id = ''.join(random.choices(
                string.ascii_lowercase + string.digits,
                k=8
            ))

            if self.get_transaction_by_id(random_transaction_id) is None:
                break
        date = str(datetime.date.today())

        x = self.execute(
            'INSERT INTO transactions VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,\'Eyez\')',
            (
                random_transaction_id,
                products_ids,
                seller_id,
                buyer_id,
                cost,
                is_offer,
                int(time.time()),
                shipping_address,
                random_transaction_id,
                date,
                date,

            )
        )

        if x:
            return random_transaction_id
        else:
            return False

    def get_transaction_by_id(self, transaction_id: int):
        return objects.Transaction.classFactory(self.select(
            'SELECT * FROM transactions WHERE id = %s',
            (transaction_id,)
        ).fetchone())

    def get_transactions(self):
        transes = self.select('SELECT * FROM transactions').fetchall()
        transactions = []
        for transaction in transes:
            transactions.append(objects.Transaction.classFactory(transaction))
        return transactions

    def get_transactions_by_user_id(self, user_id: int):
        transes = self.select(
            'SELECT * FROM transactions WHERE buyer_id = %s',
            (user_id,)
        ).fetchall()
        transactions = []
        for transaction in transes:
            transactions.append(objects.Transaction.classFactory(transaction))
        return transactions

    def set_cart_count(self, cart_id, count):
        return self.execute(
            'UPDATE users_carts SET count = %s WHERE id = %s', (cart_id, count,)
        )
