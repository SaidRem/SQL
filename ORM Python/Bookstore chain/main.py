import os
import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from models import create_tables, Publisher, Shop, Book, Stock, Sale


load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DSN = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = sqlalchemy.create_engine(DSN)
create_tables(engine)


def populate_tables(session):
    with open('fixtures/tests_data.json', 'r') as fd:
        data = json.load(fd)

    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()


def get_sales_by_publisher(session, publisher_input):
    try:
        publisher_id = int(publisher_input)
        query_filter = Publisher.id == publisher_id
    except ValueError:
        query_filter = Publisher.name == publisher_input

    query = (
        session.query(Book.title, Shop.name, Sale.price, Sale.date_sale)
        .join(Stock, Stock.id_book == Book.id)
        .join(Sale, Sale.id_stock == Stock.id)
        .join(Shop, Stock.id_shop == Shop.id)
        .join(Publisher, Book.id_publisher == Publisher.id)
        .filter(query_filter)
        .order_by(Sale.date_sale.desc())
    )

    results = query.all()

    if not results:
        print("No sales found for the given publisher.")
        return None

    title_width = max(len(row[0]) for row in results)
    shop_width = max(len(row[1]) for row in results)

    for title, shop, price, date in results:
        print(f"{title.ljust(title_width)} | {shop.ljust(shop_width)} | {price:6.2f} | {date.strftime('%d-%m-%Y')}")


if __name__ == "__main__":
    Session = sessionmaker(bind=engine)

    with Session() as session:
        populate_tables(session)

    publisher_input = input("Enter publisher name or ID: ")

    with Session() as session:
        get_sales_by_publisher(session, publisher_input)
