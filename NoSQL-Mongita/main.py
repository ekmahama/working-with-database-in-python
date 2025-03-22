import requests, click,csv
from datetime import datetime
from mongita import MongitaClientDisk
 
def get_coin_price(coin_id:str, currency:str):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={currency}"
    data = requests.get(url).json()
    coin_price = data[coin_id][currency]
    return coin_price


@click.group()
def cli():
    pass

@click.command()
@click.option("--coin_id", default="bitcoin")
@click.option("--currency", default = "usd")
def show_coin_price(coin_id:str, currency:str):
    coin_price = get_coin_price(coin_id, currency)
    print(f"The price of {coin_id} is {coin_price:.2f} {currency.upper()}")

@click.command()
@click.option("--coin_id")
@click.option("--currency")
@click.option("--amount", type=float)
@click.option("--sell", is_flag=True)
def add_investment(coin_id, currency, amount, sell):
    investment_document = {
        "coin_id": coin_id,
        "currency": currency,
        "amount": amount,
        "sell": sell,
        "timestamp": datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    }

    investments.insert_one(investment_document)

    if sell:
        print(f"Added sell of {amount} {coin_id}")
    else:
        print(f"Added buy of {amount} {coin_id}")

@click.command()
@click.option("--coin_id")
@click.option("--currency")
def get_investment_value(coin_id: str, currency:str):
     coin_price = get_coin_price(coin_id, currency)

     buy_result = investments.find({"coin_id": coin_id, "currency": currency, "sell": False})
     sell_result = investments.find({"coin_id": coin_id, "currency": currency, "sell": True})

     buy_amount = sum([doc["amount"] for doc in buy_result])
     sell_amount = sum([doc["amount"] for doc in sell_result])
     total = buy_amount + sell_amount
     print(f"You won a total of {total} {coin_id} worth of {total * coin_price} {currency.upper()}")

@click.command()
@click.option("--csv_file")
def import_investments(csv_file):
    fieldnames = ["coin_id", "currency", "amount", "sell", "timestamp"]
    with open(csv_file, "r") as file:
        reader = csv.DictReader(file, fieldnames=fieldnames)
        docs = list(reader)
        investments.insert_many(docs)

        print(f"Imported {len(docs)} investments from {csv_file}")

@click.command()
@click.option('--file_name')
def export_investments(file_name):
    with open(file_name, '+a') as f:
        writer = csv.writer(f)
        # sql = "SELECT * FROM investments"
        # rows = cur.execute(sql).fetchall()
        docs = investments.find({})
        writer.writerow(["crypto","currency", "amount", "timestamp"])
        for doc in docs:
            writer.writerow([doc['coin_id'], doc['currency'], doc['amount'], doc['timestamp']])

        print(f'Exported {len(list(docs))} investments to {file_name}')

cli.add_command(show_coin_price)
cli.add_command(add_investment)
cli.add_command(get_investment_value) 
cli.add_command(import_investments)
cli.add_command(export_investments)

if __name__=="__main__":
    client = MongitaClientDisk()
    db = client.portfolio
    investments = db.investments
    cli()