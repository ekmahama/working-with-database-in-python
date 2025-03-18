import psycopg2, click, csv, requests
import psycopg2.extras
from dataclasses import dataclass

@dataclass
class Investment:
    id: int
    coin: str
    currency: str
    amount : float

def get_connection():
    connection = psycopg2.connect(
        host = "localhost",
        database ="postgres",
        user = "postgres",
        password = "pgpassword"
    )
    return connection

@click.command()
@click.option("--coin", prompt=True)
@click.option("--currency", prompt=True)
@click.option("--amount", prompt=True)
def new_investment(coin:str,currency:str, amount:float):
    sql = f"""
    INSERT INTO investments (
        coin, currency, amount
    ) VALUES (
        '{coin.lower()}', '{currency.lower()}', '{amount}'
    )
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()

    cursor.close()
    connection.close()

    print(f"Added investment for {amount} {coin} in {currency}")

@click.command()
@click.option("--filename")
def import_investments(filename):
    sql = """
    INSERT INTO investments (coin, currency, amount) VALUES %s;
    """
    connection = get_connection()
    cursor = connection.cursor()

    with open(filename, 'r') as f:
        rdr = csv.reader(f, delimiter=",")
        rows = [[x.lower() for x in row[1:]] for row in rdr]

    psycopg2.extras.execute_values(cursor, sql, rows)
    connection.commit()

    cursor.close()
    connection.close()

    print(f"Added {len(rows)} Investments")

@click.command()
@click.option("--currency")
def view_investments(currency):
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sql = """SELECT * from investments"""

    if currency is not None:
        sql += f" WHERE currency = %s;"
        cursor.execute(sql, (currency,))
    else:
        cursor.execute(sql)

    data = [Investment(**dict(row)) for row in cursor.fetchall()]

    cursor.close()
    connection.close()

    coins = set([row.coin for row in data])
    currencies = set([row.currency for row in data])

    url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(coins)}&vs_currencies={','.join(currencies)}"
    coin_data = requests.get(url).json()

    for investment in data:
        coin_price = coin_data[investment.coin][investment.currency.lower()]
        coin_total = investment.amount * coin_price
        print(f"{investment.amount} {investment.coin} in {investment.currency} is worth {coin_total}")

        


@click.group()
def cli():
    pass

cli.add_command(new_investment)
cli.add_command(import_investments)
cli.add_command(view_investments)

if __name__=='__main__':
    cli()