import psycopg2
from psycopg2 import sql
from psycopg2.extras import DictCursor
import copy
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )


def create_database(db_name, conn_params):
    """Create a new PostgreSQL database if it does not exist."""
    try:
        conn = psycopg2.connect(**conn_params)
        conn.autocommit = True  # Enable autocommit - required to create a DB.
        with conn.cursor() as cur:
            cur.execute(
                sql.SQL("SELECT 1 FROM pg_database WHERE datname = {}").format(sql.Literal(db_name))
            )

            if not cur.fetchone():
                cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
                logging.info(f"Databse '{db_name}' was created successfully.")
            else:
                logging.info(f"Database '{db_name}' already exists.")
    except psycopg2.Error as err:
        logging.error(f"Error creating database: {err}")
    finally:
        if conn:
            conn.close()


def create_tables(conn_params):
    """Create the 'clients' and 'phones' tables if they do not exist."""
    try:
        with psycopg2.connect(**conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS clients (
                            id SERIAL PRIMARY KEY,
                            first_name VARCHAR(100) NOT NULL,
                            last_name VARCHAR(100) NOT NULL,
                            email VARCHAR(100) UNIQUE NOT NULL
                    );
                """)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS phones (
                            id SERIAL PRIMARY KEY,
                            client_id INT REFERENCES clients(id) ON DELETE CASCADE,
                            phone_number VARCHAR(20) NOT NULL
                    );
                """)
                conn.commit()
                logging.info("Tables 'clients' and 'phones' were created successfully")
    except psycopg2.Error as err:
        logging.error(f"Error creating tables: {err}")


def create_clients_db(db_name="clients_db", conn_params=None):
    """Main function to create a database and necessary tables."""
    if conn_params is None:
        logging.error("Connection parameters not specified. Database not created.")
        return

    # Create database if not exists.
    create_database(db_name, conn_params)

    # Create tables in the new database.
    conn_params_newdb = copy.deepcopy(conn_params)
    conn_params_newdb["database"] = db_name
    create_tables(conn_params_newdb)


if __name__ == "__main__":
    conn_params = {
        "database": "postgres",
        "user": "postgres",
        "password": "123",
        "host": "localhost",
        "port": 5432
    }

    create_clients_db(db_name="clients_db", conn_params=conn_params)
