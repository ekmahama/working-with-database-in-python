import datetime, click
from bson import ObjectId
from pymongo import MongoClient
from utils import get_coin_price, util_seed_data

client = MongoClient()

portfolio = client.portfolio

watchlists = portfolio.watchlists


def _get_all_watchlist_name():
    return list(watchlists.find({}, {"name": 1}))

def _select_watchlist(watchlist_names):
    for index, watchlist in enumerate(watchlist_names):
        print(f"{index + 1}: {watchlist['name']}")

    selected_watchlist_index = int(input("Select a watchlist: ")) - 1
    selected_watchlist_id = watchlist_names[selected_watchlist_index]["_id"]
    return watchlists.find_one({"_id": ObjectId(selected_watchlist_id)})


def _add_coin_to_watchlist(watchlist_oid, coin):
    filter = {"_id": ObjectId(watchlist_oid)}
    update = {"$push": {"coins": coin}}
    watchlists.update_one(filter, update)


def _remove_coin_from_watchlist(watchlist_oid, selected_coin):
    filter = {"_id": ObjectId(watchlist_oid)}
    update = {"$pull": {"coins": selected_coin}}
    watchlists.update_one(filter, update)

def _select_coin_from_watchlist(watchlist):
    for index, coin in enumerate(watchlist["coins"]):
        print(f"{index + 1}: {coin['coin']}")
    selected_coin_index = int(input("Select a coin: ")) - 1
    return watchlist["coins"][selected_coin_index]


@click.command(help="Clear the database")
def clear_data():
    portfolio.drop_collection("watchlists")

    print("Add data cleared")

@click.command(help="See the database")
@click.option("--force", is_flag=True, help="See even if the database is not empty")
def seed_data(force):
    if force:
        util_seed_data(watchlists)
    elif watchlists.count_documents({}) > 0:
        print("The database is empty, use the --force option or the clear-data cpmmand")
    else:
        util_seed_data(watchlists)

@click.command(help="View the coins and the current prices of a watchlist")
def view_watchlists():
    selected_watchlist = _select_watchlist(_get_all_watchlist_name())

    print(f"Watchlist: {selected_watchlist['name']} in {selected_watchlist['metadata']['currency']}")
    print(f"{selected_watchlist['metadata']['description']}")
    print(f"{'-' * 25}")
    print("coins:")

    coin_prices = get_coin_price([coin["coin"] for coin in selected_watchlist["coins"]], selected_watchlist['metadata']['currency'])

    for index, coin in enumerate(selected_watchlist['coins']):
        print(f"{str(index + 1).rjust(3, " ")}: {coin['coin']} - {coin['note']}")
        print(f"    Current price: {coin_prices[coin['coin']]}")

    print("Prices provided by CoinGecko")

@click.command(help="Add a new watchlist to the portfolio")
@click.option("--name", prompt=True, help="Naem of the watchlist")
@click.option("--description", prompt=True, help="Description of the watchlist")
@click.option("--currency", prompt=True, help="Currency to display prices")
def add_watchlist(name, description, currency):
    metadata = {
        "description": description,
        "currency": currency,
        "date_added": datetime.datetime.now()
    }

    watchlist = {
        "name": name,
        "metadata": metadata,
        "coins": []
    }

    watchlists.insert_one(watchlist)

    print(f"Added new {name} watchlist")

@click.command(help="Add a new coin to a watchlist")
@click.option("--coin", prompt=True,help="The coin to add")
@click.option("--note", prompt=True, help="A note")
def add_coin(coin, note):
    selected_watchlist = _select_watchlist(_get_all_watchlist_name())
    _add_coin_to_watchlist(selected_watchlist["_id"], {"coin": coin, "note": note, "date_added": datetime.datetime.now()})

    print(f"Added {coin} to {selected_watchlist['name']}")

@click.command(help="Remove a coin from a watchlist")
def remove_coin():
    selected_watchlist = _select_watchlist(_get_all_watchlist_name())
    selected_coin = _select_coin_from_watchlist(selected_watchlist)

    _remove_coin_from_watchlist(selected_watchlist['_id'], selected_coin['coin'])
    print(f"Removed {selected_coin} from {selected_watchlist['name']}")
    

@click.group()
def cli():
    pass


cli.add_command(clear_data)
cli.add_command(seed_data)
cli.add_command(view_watchlists)
cli.add_command(add_watchlist)
cli.add_command(add_coin)
cli.add_command(remove_coin)

if __name__== "__main__":
    cli()