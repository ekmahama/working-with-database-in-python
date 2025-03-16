import requests, click, sqlite3, csv
from datetime import datetime

CREATE_INVESTMENTS_SQL = """
CREATE TABLE IF NOT EXISTS investments (
    coin_id TEXT,
    currency TEXT,
    amount REAL,
    sell INT,
    date TIMESTAMP
);
"""
     
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
    sql = "INSERT INTO investments VALUES(?,?,?,?,?);"
    values = (coin_id, currency, amount, sell, datetime.now())
    cur.execute(sql, values)
    database.commit()

    if sell:
        print(f"Added sell of {amount} {coin_id}")
    else:
        print(f"Added buy of {amount} {coin_id}")

@click.command()
@click.option("--coin_id")
@click.option("--currency")
def get_investment_value(coin_id: str, currency:str):
     coin_price = get_coin_price(coin_id, currency)
     sql = """
        SELECT amount FROM investments
        WHERE coin_id =?
        AND currency=?
        AND sell=?;
     """
     buy_result = cur.execute(sql, (coin_id, currency, False)).fetchall()
     sell_result = cur.execute(sql, (coin_id, currency, True)).fetchall()

     buy_amount = sum([row[0] for row in buy_result])
     sell_amount = sum([row[0] for row in sell_result])
     total = buy_amount + sell_amount
     print(f"You won a total of {total} {coin_id} worth of {total * coin_price} {currency.upper()}")

@click.command()
@click.option("--csv_file")
def import_investments(csv_file):
    with open(csv_file) as f:
        rdr = csv.reader(f, delimiter=",")
        rows = list(rdr)
        sql = "INSERT INTO investments VALUES(?,?,?,?,?);"
        cur.executemany(sql, rows)
        database.commit()

        print(f"Imported {len(rows)} investments from {csv_file}")

@click.command()
@click.option('--file_name')
def export_investments(file_name):
    with open(file_name, '+a') as f:
        writer = csv.writer(f, delimiter=",")
        sql = "SELECT * FROM investments"
        rows = cur.execute(sql).fetchall()
        writer.writerows(rows)

        print(f'Exported {len(rows)} investments to {file_name}')

cli.add_command(show_coin_price)
cli.add_command(add_investment)
cli.add_command(get_investment_value) 
cli.add_command(import_investments)
cli.add_command(export_investments)

if __name__=="__main__":
    database = sqlite3.connect("portfolio.db")
    cur = database.cursor()
    cur.execute(CREATE_INVESTMENTS_SQL)
    cli()