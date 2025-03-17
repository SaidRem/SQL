import os
import tkinter as tk
from tkinter import filedialog, scrolledtext
import threading
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from models import create_tables, Publisher, Shop, Book, Stock, Sale


def load_env(directory):
    """Load environment variables from the selected directory"""
    env_path = os.path.join(directory, ".env")
    if os.path.exists(env_path):
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, ".env file found")
        load_dotenv(env_path)
    else:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "No .env file found in the selected directory.\n")


def select_directory():
    """Open dialog to select directory containing .env file"""
    directory = filedialog.askdirectory()
    env_directory_var.set(directory)
    load_env(directory)


def query_database(search_id, search_text):
    """Query PostgreSQL database"""
    try:
        DB_USER = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        DB_HOST = os.getenv("DB_HOST")
        DB_PORT = os.getenv("DB_PORT")
        DB_NAME = os.getenv("DB_NAME")

        DSN = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

        engine = sqlalchemy.create_engine(DSN)

        if search_id:
            query_filter = Publisher.id == search_id
        else:
            query_filter = Publisher.name == search_text

        Session = sessionmaker(bind=engine)
        with Session() as session:
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

        result_text.delete("1.0", tk.END)
        if not results:
            result_text.insert("1.0", "No sales found for the given publisher")
            return None

        title_width = max(len(row[0]) for row in results)
        shop_width = max(len(row[1]) for row in results)

        for i, (title, shop, price, date) in enumerate(results):
            result_text.insert(f"{i+1}.0", f"{title.ljust(title_width)} | {shop.ljust(shop_width)} | {price:6.2f} | {date.strftime('%d-%m-%Y')}\n")
    except Exception as err:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, f"Error: {err}")


def start_search():
    """Start database query"""
    search_entry = id_entry.get()

    result_text.delete("1.0", tk.END)

    if search_entry.isdigit():
        search_id = int(search_entry)
        search_text = None
    else:
        search_id = None
        search_text = search_entry.strip()

    thread = threading.Thread(target=query_database, args=(search_id, search_text))
    thread.start()


root = tk.Tk()
root.title("Sales by publisher")
root.geometry("800x400")

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Env Directory:").grid(row=0, column=0, sticky="w")
env_directory_var = tk.StringVar()
tk.Button(frame, text="Select Env Directory", command=select_directory).grid(row=0, column=2, padx=5)
tk.Entry(frame, textvariable=env_directory_var, width=50).grid(row=0, column=1)

tk.Label(frame, text="Search ID/name:").grid(row=1, column=0, sticky="w")
id_entry = tk.Entry(frame)
id_entry.grid(row=1, column=1, sticky="w")

tk.Button(frame, text="Search in DB", command=start_search, width=15).grid(row=1, column=2, padx=5)

result_text = scrolledtext.ScrolledText(root, width=90, height=15)
result_text.pack()

root.mainloop()
