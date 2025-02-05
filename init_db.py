import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class InitPostgreSQL:
    
    DB_NAME = "my_database"
    DB_USER = "postgres"
    DB_PASSWORD = "your_password"
    DB_HOST = "localhost"
    DB_PORT = "5432"

    TABLES = { 
        "users": """
                      CREATE TABLE IF NOT EXISTS users (
                      id SERIAL PRIMARY KEY,
                      name VARCHAR(255) NOT NULL,
                      email VARCHAR(255) UNIQUE NOT NULL
                      )
                    """,
        "products": """
                      CREATE TABLE IF NOT EXISTS products (
                      product_id SERIAL PRIMARY KEY,
                      title VARCHAR(255) NOT NULL,
                      price DECIMAL(10,2) NOT NULL
                      )
                    """
             }


    def __init__(self):
        pass
        create_database()
        create_tables()

    def _create_database():
        try:
            # Подключаемся к серверу PostgreSQL без конкретной базы
            conn = psycopg2.connect(
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT,
                dbname="postgres"
                )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()

            # Проверяем существование базы данных
            cursor.execute(
                sql.SQL("SELECT 1 FROM pg_database WHERE datname = {}").format(sql.Literal(DB_NAME))
                )
        
            if not cursor.fetchone():
                cursor.execute(
                    sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME))
                )
                print(f"База данных {DB_NAME} создана")
            else:
                print(f"База данных {DB_NAME} уже существует")

        except Exception as e:
            print(f"Ошибка при создании базы данных: {e}")
        finally:
            if conn:
                cursor.close()
                conn.close()

    def _create_tables():
        try:
            # Подключаемся к конкретной базе
            conn = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
                )
            cursor = conn.cursor()

            # Создаем таблицы
            for table_name, ddl in TABLES.items():
                cursor.execute(ddl)
                print(f"Таблица {table_name} создана или уже существует")
        
            conn.commit()

        except Exception as e:
            print(f"Ошибка при создании таблиц: {e}")
            conn.rollback()
        finally:
            if conn:
                cursor.close()
                conn.close()
   





