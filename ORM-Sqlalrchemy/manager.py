import psycopg2, click, csv, requests
import psycopg2.extras
from dataclasses import dataclass
from sqlalchemy import String, Numeric, create_engine, select, Text, ForeignKey
from typing import List
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship

class Base(DeclarativeBase):
    pass

class Investment(Base):
    __tablename__= "investment"
    id:Mapped[int] = mapped_column(primary_key=True)
    coin: Mapped[str] = mapped_column(String(32))
    currency: Mapped[str] = mapped_column(String(3))
    amount: Mapped[float] = mapped_column(Numeric(5,2))

    portfolio_id : Mapped[int] = mapped_column(ForeignKey("portfolio.id"))
    portfolio: Mapped["Portfolio"] = relationship(back_populates="investments")

    def __str__(self):
        return f"<Investment coin: :{self.coin}, currency: {self.currency}, amount: {self.amount}>"
    
class Portfolio(Base):
    __tablename__ = "portfolio"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(256))
    description: Mapped[str] = mapped_column(Text())

    investments: Mapped[List["Investment"]] = relationship(back_populates="portfolio")


    def __repr__(self) -> str:
        return f"<Portfolia name: {self.name} with {len(self.investments)} investments>"

def get_coin_price(coins, currencies):
    coin_csv = ",".join(coins)
    currency_csv = ",".join(currencies)

    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_csv}&vs_currencies={currency_csv}"
    data = requests.get(url).json()
    return data


@click.command()
@click.option("--filename")
def import_investments(filename):
    pass


@click.command()
@click.option("--currency")
def view_investments(currency):
    pass

@click.command(help="View the investments in a portfolio")
def view_portfolio():
    with Session(engine) as session:
        stmt = select(Portfolio)
        all_portfolios = session.execute(stmt).scalars().all()
        for index, portfolio in enumerate(all_portfolios):
            print(f"{index+1}: {portfolio.name}")  

        portfolio_id = int(input("Select a portfolio: ")) -1
        portfolio = all_portfolios[portfolio_id]

        investments = portfolio.investments

        coins = {investment.coin for investment in investments}
        currencies = {investment.currency for investment in investments}

        coin_prices = get_coin_price(coins, currencies)

        print(f"Investments in {portfolio.name}")
        for ind, inv in enumerate(investments):
            coin_price = coin_prices[inv.coin][inv.currency.lower()]
            total_price = float(inv.amount) * coin_price
            print(f"{ind + 1}: {inv.coin} {total_price:.2f} {inv.currency}")

        print("Prices provided by CoinGecko")


@click.command(help="Create a new investment and it to a portfolio")
@click.option("--coin", prompt=True)
@click.option("--currency", prompt=True)
@click.option("--amount", prompt=True)
def add_investment(coin:str,currency:str, amount:float):
    with Session(engine) as session:
        stmt = select(Portfolio)
        all_portfolios = session.execute(stmt).scalars().all()

        for index, portfolio in enumerate(all_portfolios):
            print(f"{index + 1}: {portfolio}")

        portfolio_index = int(input("Select a portfolio: ")) - 1
        portfolio = all_portfolios[portfolio_index]

        investment = Investment(coin=coin, currency = currency, amount = amount)
        portfolio.investments.append(investment)

        session.add(portfolio)
        session.commit()

        print(f"Added new {coin} investment to {portfolio.name}")


@click.command(help="Create a new portfolio")
@click.option("--name", prompt=True)
@click.option ("--description", prompt=True)
def add_portfolio(name, description):
    porfolio = Portfolio(name=name, description = description)
    with Session(engine) as session:
        session.add(porfolio)
        session.commit()
    print(f"Added portfolio {name}")

@click.command(help="Drop all tables in the database")
def clear_database():
    Base.metadata.drop_all(engine)
    print("Database cleared!")
        
@click.group()
def cli():
    pass

cli.add_command(add_portfolio)
cli.add_command(clear_database)
cli.add_command(add_investment)
cli.add_command(view_portfolio)

if __name__=='__main__':
    #engine = create_engine("sqlite:///demo_new.db")
    engine = create_engine("postgresql://postgres:pgpassword@localhost/postgres")
    Base.metadata.create_all(engine)
    cli()