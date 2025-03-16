import psycopg2, click
import psycopg2.extras

CREATE_INVESTMENTS_TABLE = """
CREATE TABLE IF NOT EXISTS investments (
    id serial primary key,
    coin varchar(32),
    currency varchar(3),
    amount real);
"""

add_bitcoin = """
INSERT INTO investments
(
    coin, currency, amount
) values (
    'bitcoin', 'usd', 1.0
);
"""

# parameterize sql
add_invstment_template = """
INSERT INTO investments
(
    coin, currency, amount
) values %s;
"""

data = [
    ('ethereum','GBP', 10.0),
    ('dogecoin','EUR', 100.0)
]


select_sql ="""
SELECT * FROM investments where coin =%s
"""
def get_connection():
    connection = psycopg2.connect(
        host = "localhost",
        database ="postgres",
        user = "postgres",
        password = "pgpassword"
    )

    return connection
@click.command()
@click.option("--sql", default=CREATE_INVESTMENTS_TABLE)
def create_table(sql):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()


    
@click.command()
@click.option("--sql", default=add_bitcoin)
def add_bitcoin_investments(sql):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()

@click.command()
@click.option("--sql_template", default=add_invstment_template)
@click.option('--data', multiple=True,default=data)
def add_bitcoin_investments_parameterized(sql_template, data):
    connection = get_connection()
    cursor = connection.cursor()
    psycopg2.extras.execute_values(cursor, sql_template, data)
    connection.commit()
    cursor.close()
    connection.close()

@click.command()
@click.option("--sql", default=select_sql)
@click.option('--parameter', default='bitcoin')
def get_investments(sql, parameter):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql, (parameter,))
    data = cursor.fetchall()
    print(data)
    cursor.close()
    connection.close()

@click.group()
def cli():
    pass

cli.add_command(create_table)
cli.add_command(add_bitcoin_investments)
cli.add_command(add_bitcoin_investments_parameterized)
cli.add_command(get_investments)

if __name__ =='__main__':
    cli()