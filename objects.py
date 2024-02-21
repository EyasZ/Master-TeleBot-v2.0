from typing import Union


class User:
    def __init__(self, user: tuple):
        if user:
            self.id = user[0]
            self.name = user[1]
            self.is_seller = user[2]
            self.channel_id = user[3]
            self.currency = user[4]
            self.status = user[5]
            self.balance = user[6]
        else:
            return None

    def classFactory(self: tuple):
        if self:
            return User(self)
        else:
            return None


class Product:
    def __init__(self, product: tuple):
        if product:
            self.id = product[0]
            self.name = product[1]
            self.cost = product[2]
            self.description = product[3]
            self.photo_link = product[4]
            self.seller_id = product[5]
            self.hidden_link = product[6]
            self.product_code = product[7]
            self.collection_code = product[12]
            self.sizes = product[13]
        else:
            self = None

    def classFactory(self: tuple):
        if self:
            return Product(self)
        else:
            return None


class Offer:
    def __init__(self, offer: tuple):
        if offer:
            self.id = offer[0]
            self.product_id = offer[1]
            self.seller_id = offer[2]
            self.buyer_id = offer[3]
            self.cost = offer[4]
            self.valid = offer[5]
        else:
            self = None

    def classFactory(self: tuple):
        if self:
            return Offer(self)
        else:
            return None


class Transaction:
    def __init__(self, transaction: tuple):
        if transaction:
            self.id = transaction[0]
            self.products_ids = transaction[1]
            self.seller_id = transaction[2]
            self.buyer_id = transaction[3]
            self.cost = transaction[4]
            self.is_offer = transaction[5]
            self.date = transaction[6]
            self.address = transaction[7]
        else:
            self = None

    def classFactory(self: tuple):
        if self:
            return Transaction(self)
        else:
            return None


class Users_cart:
    def __init__(self, cart: tuple):
        if cart:
            self.id = cart[0]
            self.products = cart[1]
            self.count = cart[2]
        else:
            self = None

    def classFactory(self: tuple):
        if self:
            return Users_cart(self)
        else:
            return None


class Collection:
    def __init__(self, collection: tuple):
        if collection:
            self.id = collection[0]
            self.products = collection[1]
            self.count = collection[2]
            self.channels_data = collection[8]
            self.more_pics = []
            for link in collection[9].split("\n"):
                self.more_pics.append(link)

        else:
            self = None

    def classFactory(self: tuple):
        if self:
            return Collection(self)
        else:
            return None
