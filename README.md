# Eyezmiedia Bot
Un bot su commissione da parte di Eyezmiedia, per la vendita di prodotti online.

## Configurazione
La configurazione è semplice.
Tutte le variabili (Api ID, Bot Token, etc...) sono contenute all'interno del file `config.ini`, che dev'essere riempito con i mancanti dati che si possono ottenere da Telegram.

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

Inoltre va creata la cartella `sessions`, dove Pyrogram scriverà la sessione, appunto, per il bot.

Tutto il bot è stato testato con Python 3.8 64-bit. Una versione più obsoleta non è compatibile in quanto è usato il [warlus operator](https://docs.python.org/3/whatsnew/3.8.html) in alcune parti del codice. Il codice può comunque essere reso per python 3.6 senza troppi problemi, ma questa pratica è ovviamente sconsigliata.

Tutti i pacchetti da installare sono nel file `requirements.txt`. Basta fare `pip install -r requirements.txt` per installare tutti i pacchetti alla versione corretta.

## Database
Per il database è stato utilizzato SQLite, un database leggero, facilmente integrabile e molto portabile. SQLite è perfetto per database di piccola grandezza come questo.
Il nome del file predefinito è `database.db`.

L'immagine riporta la struttura del database

![](https://i.imgur.com/131n7Pi.png)

##### Tabella users
- *id* e *name* -> Corrispettivo nel database di Telegram
- *is_seller* -> Se è un seller
- *channel_id* -> ID del canale del seller
- *status* -> Stato dell'utente in un momento specifico

##### Tabella products
- *id* -> Tag univoco alfanumerico di 8 cifre
- *name* -> Nome del prodotto
- *cost* -> Costo del prodotto
- *description* -> Descrizione del prodotto
- *photo_id* -> ID corrispettivo nel database di Telegram
- *photo_link* -> Link imgur dell'immagine
- *seller_id* -> ID dell'utente venditore

##### Tabella offers
- *id* -> Tag univoco alfanumerico di 8 cifre
- *product_id* -> ID del prodotto
- *seller_id* -> ID dell'utente venditore
- *buyer_id* -> ID dell'utente compratore
- *cost* -> Prezzo in offerya
- *valid* -> Se è valida

##### Tabella transactions
- *id* -> Tag univoco alfanumerico di 8 cifre
- *product_id* -> ID del prodotto
- *seller_id* -> ID dell'utente venditore
- *buyer_id* -> ID dell'utente compratore
- *cost* -> Soldi spesi
- *is_offer* -> Se ha pagato con una offerta
- *date* -> Data nel formato UNIX di quando è stato fatto l'acquisto
- *address* -> Indirizzo per la spedizione

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