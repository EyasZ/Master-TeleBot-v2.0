# Eyezmiedia Bot
A commissioned bot by Eyezmiedia for selling products online.

## Configuration
The configuration is simple. All variables (Api ID, Bot Token, etc...) are contained within the config.ini file, which must be filled in with the missing data obtainable from Telegram.

```ini
[pyrogram]
api_id =
api_hash =
bot_token =

[bot]
stripe =
username =
admin_id =

[imgur]
client_id = 
client_secret = 

[plugins]
root = plugins

[database]
path = database.db

[plate]
root = translations
fallback = en_US
```

Additionally, the sessions folder must be created, where Pyrogram will write the session for the bot.

The entire bot has been tested with Python 3.8 64-bit. An older version is not compatible as the walrus operator is used in some parts of the code. The code can still be made compatible with Python 3.6 without too many issues, but this practice is obviously not recommended.

All packages to be installed are in the requirements.txt file. Simply run pip install -r requirements.txt to install all packages at the correct version.

## Database
SQLite has been used for the database, a lightweight, easily integrable, and very portable database. SQLite is perfect for small-sized databases like this one. The default file name is database.db.

The image shows the structure of the database.

![](https://i.imgur.com/131n7Pi.png)

####Users Table
id and name -> Corresponding to the database of Telegram
is_seller -> Whether the user is a seller
channel_id -> ID of the seller's channel
status -> User's status at a specific moment

####Products Table
id -> Unique alphanumeric 8-digit tag
name -> Product name
cost -> Product cost
description -> Product description
photo_id -> Corresponding ID in Telegram's database
photo_link -> Imgur link of the image
seller_id -> ID of the seller user

####Offers Table
id -> Unique alphanumeric 8-digit tag
product_id -> Product ID
seller_id -> Seller user ID
buyer_id -> Buyer user ID
cost -> Price in offer
valid -> Whether it is valid

####Transactions Table
id -> Unique alphanumeric 8-digit tag
product_id -> Product ID
seller_id -> Seller user ID
buyer_id -> Buyer user ID
cost -> Money spent
is_offer -> Whether it was paid with an offer
date -> Date in UNIX format when the purchase was made
address -> Shipping address

<br>

```sql
CREATE TABLE offers
(
id text not null,
product_id int not null,
seller_id int not null,
buyer_id int not null,
cost real not null,
valid int default 1 not null,
PRIMARY KEY (id),
FOREIGN KEY (product_id) REFERENCES products(id),
FOREIGN KEY (seller_id) REFERENCES users(id),
FOREIGN KEY (buyer_id) REFERENCES users(id)
);

CREATE TABLE products
(
id text not null,
name text not null,
cost real not null,
description text not null,
photo_id text not null,
photo_link text not null,
seller_id int not null,
PRIMARY KEY (id),
FOREIGN KEY (seller_id) REFERENCES users(id)
);


CREATE TABLE users
(
id int not null,
name text not null,
is_seller int default 0 not null,
channel_id int not null,
status text default '' not null,
PRIMARY KEY (id)
);

CREATE TABLE transactions
(
id text,
product_id int not null,
seller_id int not null,
buyer_id int not null,
cost real not null,
is_offer int not null,
date int not null,
address text not null,
PRIMARY KEY (id),
FOREIGN KEY (product_id) REFERENCES products(id),
FOREIGN KEY (seller_id) REFERENCES users(id),
FOREIGN KEY (buyer_id) REFERENCES users(id)
);
```
