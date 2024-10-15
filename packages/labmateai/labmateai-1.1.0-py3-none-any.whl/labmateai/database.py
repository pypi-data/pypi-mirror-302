# database.py

import os
import logging
import psycopg2
from psycopg2 import sql, pool
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Database connection parameters
DB_CONFIG = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

# Initialize the connection pool
connection_pool = pool.SimpleConnectionPool(
    1, 20,  # min and max number of connections
    dbname=DB_CONFIG['dbname'],
    user=DB_CONFIG['user'],
    password=DB_CONFIG['password'],
    host=DB_CONFIG['host'],
    port=DB_CONFIG['port'],
    sslmode='require'
)


def get_db_connection():
    """
    Gets a connection from the connection pool.

    Returns:
        psycopg2.extensions.connection: A database connection.

    Raises:
        psycopg2.Error: If an error occurs while getting a connection.
    """

    try:
        conn = connection_pool.getconn()
        if conn:
            logging.debug("Acquired connection from pool.")
            return conn
    except psycopg2.Error as e:
        logging.error("Error getting connection from pool: %s", e)
        raise e


def release_db_connection(conn):
    """
    Releases a connection back to the pool.

    Args:
        conn (psycopg2.extensions.connection): The connection to release.
    """

    try:
        connection_pool.putconn(conn)
        logging.debug("Released connection back to pool.")
    except psycopg2.Error as e:
        logging.error("Error releasing connection to pool: %s", e)
        raise e


def get_engine(db_config):
    """
    Creates a SQLAlchemy engine using the provided database configuration.

    Args:
        db_config (dict): Database configuration parameters.

    Returns:
        Engine: A SQLAlchemy Engine instance.
    """
    try:
        database_url = f"postgresql://{db_config['user']}:{db_config['password']}@" \
                       f"{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
        engine = create_engine(database_url)
        return engine
    except Exception as e:
        logging.error("Failed to create database engine: %s", e)
        raise e
