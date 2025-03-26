import datetime, random, click, requests
from mongoengine import fields
from mongoengine import connect, Document, EmbeddedDocument, EmbeddedDocumentField, EmbeddedDocumentListField

def get_coin_price(coin_id:str, currency:str):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(coin_id)}&vs_currencies={currency}"
    data = requests.get(url).json()
    coin_prices = dict([(coin_id, data[coin_id][currency]) for coin_id in data])
    return coin_prices

def _seed_data():
    data = [
        ("Bulls", "Coins to buy", "USD", [("bitcoin", "Bitcoin is number one"),("ethereum", "ethereum is number 2")]),
        ("Bears", "Coins to sell", "USD", [("solan", "Mee..."),])]

    for row in data:
        Watchlist(
            name = row[0],
            metadata = WatchlistMetadata(description=row[1], currency=row[2]),
            coins = [WatchlistCoin(coin=coin[0], note=coin[1]) for coin in row[3]]
        ).save()

def _select_watchlist():
    watchlist_coins = Watchlist.objects.all().fields(coins=1)
    for index, coin in enumerate(watchlist_coins):
        print(f"{index+1}: {coin}")
    selected_watchlist_index = int(input("Select a watchlist: ")) - 1
    selected_watchlist_oid = watchlist_coins[selected_watchlist_index].id
    return Watchlist.objects(id=selected_watchlist_oid).first()


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
    metadata = fields.EmbeddedDocumentField(WatchListMetadata)
    coins = fields.EmbeddedDocumentListField(WatchlistCoin)

    def __str__(self):
        return f"<Watchlist name ={self.name}, currency ={self.metadata.currency} with {len(self.coins)} coins>"

@click.command(help="Clear the database")
def clear_data():
    Watchlist.drop_collection()
    print("Cleared data!")

@click.command(help="Seed the database with sample data, use the --force flag to ignore existing data")
@click.option("--force", is_flag=True, default=False)
def seed_data(force):
    if force:
        _seed_data()
    elif Watchlist.objects.count() > 0:
        print("Data not empty! Use --force flag to seed database")

@click.command(help="Add a new watchlist to the portfolia")
@click.option("--name", prompt=True)
@click.option("--description", prompt=True)
@click.option("--currency", prompt=True)
def add_watchlist(name,description, currency):
    metadata = WatchListMetadata(currency = currency, description = description)
    watchlist = Watchlist(name=name, metadata=metadata, coins = [])
    watchlist.save()

    print(f"Added watchlist {name}")

@click.command(help="Veiw the coins in watchlist")
def view_watchlist():
    selected_watchlist = _select_watchlist()
    coins = [coin.coin for coin in selected_watchlist.coins]
    coin_prices = get_coin_price(coins, selected_watchlist.metadata.currency.lower())

    print(f"Watchlist: {selected_watchlist.name} in {selected_watchlist.metadata.currency}")
    print(f"{selected_watchlist.metadata.description}")

    for index, coin in enumerate(selected_watchlist):
        print(f"{index + 1}: {coin} | {coin_prices[coin]}")
    print("Prices by CoinGecko")


@click.command("Add coin to watchlist")
@click.option("--coin", prompt=True)
@click.option("--note", prompt=True)
def add_coin(coin, note):
    selected_watchlist = _select_watchlist()
    selected_watchlist.coins.append(WatchlistCoin(coin=coin, note= note))
    selected_watchlist.save()
    print(f"Added {coin} to {selected_watchlist.name}")


@click.group()
def cli():
    pass

cli.add_command(clear_data)
cli.add_command(seed_data)
cli.add_command(view_watchlist)
cli.add_command(add_watchlist)
cli.add_command(add_coin)

if __name__ == "__main__":
    connect("portfolio_me")
    cli()