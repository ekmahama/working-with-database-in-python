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

@click.group()
def cli():
    pass

cli.add_command(new_investment)

if __name__=='__main__':
    cli()