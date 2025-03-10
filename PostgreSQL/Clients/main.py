import psycopg2
from psycopg2 import sql
from psycopg2.extras import DictCursor
import copy
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s"
                    )


def create_database(dbname, conn_params):
    """Create a new PostgreSQL database if it does not exist."""
    try:
        conn = psycopg2.connect(**conn_params)
        conn.autocommit = True  # Enable autocommit - required to create a DB.
        with conn.cursor() as cur:
            cur.execute(
                sql.SQL("SELECT 1 FROM pg_database WHERE datname = {}").format(sql.Literal(dbname))
            )

            if not cur.fetchone():
                cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))
                logging.info(f"Databse '{dbname}' was created successfully.")
            else:
                logging.info(f"Database '{dbname}' already exists.")
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


def create_clients_db(dbname="clients_db", conn_params=None):
    """Main function to create a database and necessary tables."""
    if conn_params is None:
        logging.error("Connection parameters not specified. Database not created.")
        return

    # Create database if not exists.
    create_database(dbname, conn_params)

    # Create tables in the new database.
    conn_params_newdb = copy.deepcopy(conn_params)
    conn_params_newdb["dbname"] = dbname
    create_tables(conn_params_newdb)


class PostgreSQLDatabase:
    def __init__(self, dbname, user, password, host='localhost', port=5432):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None

    def __del__(self):
        if self.connection:
            self.connection.close()
            logging.info(f"Closed connection to the database '{self.dbname}'")

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
        except psycopg2.Error as err:
            logging.error(f"Database connection error: {err}")

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def _execute_query(self, query, params=None):
        if self.connection is None:
            self.connect()
        try:
            with self.connection.cursor() as cur:
                cur.execute(query, params or ())
                self.connection.commit()
        except psycopg2.Error as err:
            self.connection.rollback()
            logging.error(f"Error executing query: {err}")

    def _fetch_all(self, query, params=None):
        if self.connection is None:
            self.connect()
        try:
            with self.connection.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(query, params or ())
                return cur.fetchall()
        except psycopg2.Error as err:
            self.connection.rollback()
            logging.error(f"Error executing query: {err}")
            return None

    def _fetch_one(self, query, params=None):
        if self.connection is None:
            self.connect()
        try:
            with self.connection.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(query, params or ())
                return cur.fetchone()
        except psycopg2.Error as err:
            self.connection.rollback()
            logging.error(f"Error executing query: {err}")
            return None

    def add_client(self, first_name, last_name, email):
        query = sql.SQL("""
            INSERT INTO clients (first_name, last_name, email)
            VALUES (%s, %s, %s);
        """)
        self._execute_query(query, (first_name, last_name, email))

    def add_phone(self, client_id, phone):
        query = sql.SQL("""
            INSERT INTO phones (client_id, phone_number)
            VALUES (%s, %s);
        """)
        self._execute_query(query, (client_id, phone))

    def update_client(self, client_id, first_name=None, last_name=None, email=None):
        updates = []
        params = []

        if first_name:
            updates.append("first_name = %s")
            params.append(first_name)
        if last_name:
            updates.append("last_name = %s")
            params.append(last_name)
        if email:
            updates.append("email = %s")
            params.append(email)

        if updates:
            query = sql.SQL("UPDATE clients SET {} WHERE id = %s").format(
                sql.SQL(", ").join(map(sql.SQL, updates)))
            params.append(client_id)
            self._execute_query(query, params)

    def delete_phone(self, client_id, phone):
        query = sql.SQL("""
            DELETE FROM phones WHERE client_id = %s AND phone_number = %s;
            """)
        self._execute_query(query, (client_id, phone))

    def delete_client(self, client_id):
        query = sql.SQL("""
            DELETE FROM clients WHERE id = %s
        """)
        self._execute_query(query, (client_id,))

    def find_client(self, first_name=None, last_name=None, email=None, phone_number=None):
        query = sql.SQL("""
            SELECT c.first_name, c.last_name, c.email, p.phone_number
            FROM clients c
            LEFT JOIN phones p ON c.id = p.client_id
            WHERE 1=1
        """)

        conditions = []
        params = []

        if first_name:
            conditions.append(sql.SQL("c.first_name = %s"))
            params.append(first_name)
        if last_name:
            conditions.append(sql.SQL("c.last_name = %s"))
            params.append(last_name)
        if email:
            conditions.append(sql.SQL("c.email = %s"))
            params.append(email)
        if phone_number:
            conditions.append(sql.SQL("p.phone_number = %s"))
            params.append(phone_number)

        if conditions:
            query = query + sql.SQL(" AND ") + sql.SQL(" AND ").join(conditions)

        result = self._fetch_all(query, params)
        return result


if __name__ == "__main__":
    conn_params = {
        "dbname": "postgres",
        "user": "postgres",
        "password": "123",
        "host": "localhost",
        "port": 5432
    }

    create_clients_db(dbname="clients_db", conn_params=conn_params)

    conn_params_newdb = copy.deepcopy(conn_params)
    conn_params_newdb["dbname"] = "clients_db"
    db = PostgreSQLDatabase(**conn_params_newdb)
    db.connect()

    db.add_client("John", "Doe", "john@mail.com")
    db.add_client("Adam", "Smit", "adam_smit@mail.com")
    db.add_client("Jane", "Doe", "jane_doe@mail.com")

    db.add_phone(1, '89171235678')
    db.add_phone(1, '89171235679')

    result = db.find_client()

    for client in result:
        print(f"name: {client[0]} | surname: {client[1]} | email: {client[2]} | tel: {client[3]}")

    result = db.find_client(last_name="Smit")
    for client in result:
        print(f"name: {client[0]} | surname: {client[1]} | email: {client[2]} | tel: {client[3]}")

    db.delete_phone(1, '89171235678')
    db.delete_client(3)

    db.update_client(5, email="john.doe@mail.com")
