import sqlite3
from datetime import datetime


def execute_query(connection, query, params=None):
    try:
        cursor = connection.cursor()
        if params:
            cursor.executemany(query, params)
        else:
            cursor.execute(query)
        connection.commit()
    except sqlite3.Error as e:
        print(f"Error: {e}")


def create_tables(connection):
    queries = [
        """
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            order_date DATE NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
        """
    ]
    for query in queries:
        execute_query(connection, query)


def add_products(connection):
    products = [
        ("iPhone 14", "смартфони", 999.99),
        ("MacBook Pro 16", "ноутбуки", 2499.99),
        ("iPad Pro", "планшети", 799.99),
        ("Samsung Galaxy S23", "смартфони", 899.99),
        ("Dell XPS 15", "ноутбуки", 1999.99)
    ]
    for product in products:
        try:
            query = "INSERT INTO products (name, category, price) VALUES (?, ?, ?)"
            execute_query(connection, query, [product])
        except sqlite3.IntegrityError:
            print(f"Продукт {product[0]} уже существует в базе данных.")


def add_customers(connection):
    customers = [
        ("Іван", "Іванов", "ivan.ivanov@example.com"),
        ("Анна", "Петрівна", "anna.petrova@example.com"),
        ("Сергій", "Кузнецов", "sergey.k@example.com")
    ]
    for customer in customers:
        try:
            query = "INSERT INTO customers (first_name, last_name, email) VALUES (?, ?, ?)"
            execute_query(connection, query, [customer])
        except sqlite3.IntegrityError:
            print(f"Клиент с email {customer[2]} уже существует в базе данных.")


def add_orders(connection):
    orders = [
        (1, 1, 1, 2, datetime.now().strftime("%Y-%m-%d")),
        (2, 2, 3, 1, datetime.now().strftime("%Y-%m-%d")),
        (3, 1, 2, 1, datetime.now().strftime("%Y-%m-%d")),
        (4, 3, 5, 1, datetime.now().strftime("%Y-%m-%d"))
    ]
    for order in orders:
        query = "INSERT INTO orders (order_id, customer_id, product_id, quantity, order_date) VALUES (?, ?, ?, ?, ?)"
        execute_query(connection, query, [order])


def get_total_sales(connection):
    query = """
    SELECT SUM(p.price * o.quantity) AS total_sales
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
    """
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    print(f"Сумарний обсяг продаж: {result[0]:.2f}")


def get_orders_per_customer(connection):
    query = """
    SELECT c.first_name || ' ' || c.last_name AS customer_name, COUNT(o.order_id) AS order_count
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id
    """
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
        print(f"Клієнт: {row[0]}, Кількість замовлень: {row[1]}")


def get_average_order_value(connection):
    query = """
    SELECT AVG(p.price * o.quantity) AS average_order_value
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
    """
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    print(f"Середня сумма замовлення: {result[0]:.2f}")


def get_most_popular_category(connection):
    query = """
    SELECT p.category, COUNT(o.order_id) AS order_count
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
    GROUP BY p.category
    ORDER BY order_count DESC
    LIMIT 1
    """
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    print(f"Наиболее популярная категория товаров: {result[0]} (Заказов: {result[1]})")


def update_smartphone_prices(connection):
    query = "UPDATE products SET price = price * 1.10 WHERE category = 'смартфони'"
    execute_query(connection, query)
    print("Цены на смартфоны увеличены на 10%")


def interactive_menu(connection):
    while True:
        print("\nВыберите действие:")
        print("1. Добавить товары")
        print("2. Добавить клиентов")
        print("3. Добавить заказы")
        print("4. Показать общий объем продаж")
        print("5. Показать количество заказов на каждого клиента")
        print("6. Показать средний чек заказа")
        print("7. Показать наиболее популярную категорию товаров")
        print("8. Обновить цены на смартфоны (+10%)")
        print("9. Выйти")

        choice = input("Введите номер действия: ")
        if choice == "1":
            add_products(connection)
        elif choice == "2":
            add_customers(connection)
        elif choice == "3":
            add_orders(connection)
        elif choice == "4":
            get_total_sales(connection)
        elif choice == "5":
            get_orders_per_customer(connection)
        elif choice == "6":
            get_average_order_value(connection)
        elif choice == "7":
            get_most_popular_category(connection)
        elif choice == "8":
            update_smartphone_prices(connection)
        elif choice == "9":
            print("Выход...")
            break
        else:
            print("Неверный выбор, попробуйте снова.")


def main():
    connection = sqlite3.connect("online_shop.db")
    create_tables(connection)
    interactive_menu(connection)
    connection.close()


if __name__ == "__main__":
    main()
