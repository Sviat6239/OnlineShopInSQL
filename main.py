import sqlite3
from datetime import datetime


def execute_query(connection, query, params=None):
    cursor = connection.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    connection.commit()
    return cursor.fetchall()


def add_products(connection):
    products = [
        (1, 'iPhone 14', 'смартфони', 999.99),
        (2, 'Samsung Galaxy S22', 'смартфони', 849.99),
        (3, 'MacBook Pro', 'ноутбуки', 1999.99),
        (4, 'Dell XPS 13', 'ноутбуки', 1399.99),
        (5, 'iPad Pro', 'планшети', 799.99),
        (6, 'Samsung Galaxy Tab S8', 'планшети', 699.99)
    ]
    execute_query(connection, "INSERT INTO products VALUES (?, ?, ?, ?)", products)


def add_customers(connection):
    customers = [
        (1, 'Іван', 'Іваненко', 'ivan.ivanenko@example.com'),
        (2, 'Марія', 'Петренко', 'maria.petrenko@example.com'),
        (3, 'Олексій', 'Коваленко', 'olexiy.kovalenko@example.com')
    ]
    execute_query(connection, "INSERT INTO customers VALUES (?, ?, ?, ?)", customers)


def add_orders(connection):
    orders = [
        (1, 1, 1, 1, '2024-12-01'),
        (2, 2, 3, 1, '2024-12-02'),
        (3, 3, 5, 2, '2024-12-03'),
        (4, 1, 2, 1, '2024-12-04')
    ]
    execute_query(connection, "INSERT INTO orders VALUES (?, ?, ?, ?, ?)", orders)


def interactive_query_execution(connection):
    print("1. Сумарний обсяг продажів")
    print("2. Кількість замовлень на клієнта")
    print("3. Середній чек замовлення")
    print("4. Найпопулярніша категорія товарів")
    print("5. Кількість товарів у категорії")
    print("6. Оновлення цін")

    choice = input("Введіть номер запиту: ")
    if choice == "1":
        query = "SELECT SUM(p.price * o.quantity) AS total_sales FROM orders o INNER JOIN products p ON o.product_id = p.product_id;"
        result = execute_query(connection, query)
        print("Сумарний обсяг продажів:", result[0][0])
    elif choice == "2":
        query = "SELECT c.first_name, c.last_name, COUNT(o.order_id) AS order_count FROM customers c INNER JOIN orders o ON c.customer_id = o.customer_id GROUP BY c.customer_id;"
        result = execute_query(connection, query)
        for row in result:
            print(f"Клієнт: {row[0]} {row[1]}, Кількість замовлень: {row[2]}")
    elif choice == "3":
        query = "SELECT AVG(p.price * o.quantity) AS average_order_value FROM orders o INNER JOIN products p ON o.product_id = p.product_id;"
        result = execute_query(connection, query)
        print("Середній чек замовлення:", result[0][0])
    elif choice == "4":
        query = "SELECT p.category, COUNT(o.order_id) AS order_count FROM products p INNER JOIN orders o ON p.product_id = o.product_id GROUP BY p.category ORDER BY order_count DESC LIMIT 1;"
        result = execute_query(connection, query)
        print("Найпопулярніша категорія:", result[0][0])
    elif choice == "5":
        query = "SELECT category, COUNT(*) AS product_count FROM products GROUP BY category;"
        result = execute_query(connection, query)
        for row in result:
            print(f"Категорія: {row[0]}, Кількість товарів: {row[1]}")
    elif choice == "6":
        execute_query(connection, "UPDATE products SET price = price * 1.1 WHERE category = 'смартфони';")
        print("Ціни оновлено.")
    else:
        print("Невірний вибір.")


def main():
    connection = sqlite3.connect("electronics_store.db")
    with connection:
        add_products(connection)
        add_customers(connection)
        add_orders(connection)
        while True:
            interactive_query_execution(connection)
            save = input("Зберегти зміни в базі даних? (yes/no): ").lower()
            if save == 'no':
                connection.rollback()
            cont = input("Виконати ще один запит? (yes/no): ").lower()
            if cont == 'no':
                break


if __name__ == "__main__":
    main()
