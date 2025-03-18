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
    

engine = create_engine("sqlite:///demo_r.db")
Base.metadata.create_all(engine)


bitcoin = Investment(coin="bitcoin", currency='usd', amount = 1.0)
ethereum = Investment(coin="ethereum", currency='gpb', amount = 10.0)
dogecoin = Investment(coin="solana", currency='usd', amount = 100.0)
bitcoin_2 = Investment(coin="bitcoin", currency='usd', amount = 10.0)

portfolio_1 = Portfolio(name="Portfolio 1", description="Description 1")
portfolio_2 = Portfolio(name="Portfolio 2", description="Description 2")
portfolio_3 = Portfolio(name="Portfolio 3", description="Description 3")

# Associate bitcoin with portfolio_1
# bitcoin.portfolio = portfolio_1
bitcoin_2.portfolio = portfolio_3

# Add the other investemts to portfolio_2
portfolio_2.investments.extend([ethereum, dogecoin])
with Session(engine) as session:
    ## Adding to db
    # #session.add(bitcoin) # NB: Adding bitcoin will add all table (portfolio) it has relation ship in db
    # session.add(bitcoin_2)
    # # session.add(portfolio_2) # Similarly , add portfolio adds it related table(investemt)
    # session.commit()

    ## Selecting from DB

    # Selection portfolio with id
    portfolio = session.get(Portfolio, 2)
    for investment in portfolio.investments:
        print(investment)

    print(portfolio)

    # Select investemtn with id
    investment = session.get(Investment, 1)
    print(investment.portfolio)

    # stmt = select(Investment).join(Portfolio)
    # print(stmt)

    # Select related objectjs
    subq = select(Investment).where(Investment.coin =="bitcoin").subquery()
    stmt = select(Portfolio).join(subq, Portfolio.id == subq.c.portfolio_id)
    portfolios = session.execute(stmt).scalars().all()
    print(portfolios)






