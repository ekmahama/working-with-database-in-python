import psycopg2, click, csv
import psycopg2.extras
from dataclasses import dataclass

@dataclass
class Investments:
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


@click.group()
def cli():
    pass

cli.add_command(new_investment)
cli.add_command(import_investments)

if __name__=='__main__':
    cli()