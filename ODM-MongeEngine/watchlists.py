import datetime, random, click, requests
from mongoengine import fields
from mongoengine import connect, Document, EmbeddedDocument, EmbeddedDocumentField, EmbeddedDocumentListField

def get_coin_price(coin_id:str, currency:str):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(coin_id)}&vs_currencies={currency}"
    data = requests.get(url).json()
    coin_prices = dict([(coin_id, data[coin_id][currency]) for coin_id in data])
    return coin_prices


class WatchListMetadata(EmbeddedDocument):
    currency = fields.StringField(max_length=3)
    description = fields.StringField()
    date_created = fields.DateField(default=datetime.datetime.now().date)

class WatchlistCoin(EmbeddedDocument):
    coin = fields.StringField(max_length=32)
    note = fields.StringField()
    date_added = fields.DateField(default=datetime.datetime.now().date)

class Watchlist(Document):
    name = fields.StringField(max_length=256)
    metadata = fields.EmbeddedDocument(WatchListMetadata)
    coins = fields.EmbeddedDocumentListField(WatchlistCoin)

    def __str__(self):
        return f"<Watchlist name ={self.name}, currency ={self.metadata.currency} with {len(self.coins)} coins>"


@click.group()
def cli():
    pass

if __name__ == "__main__":
    cli()