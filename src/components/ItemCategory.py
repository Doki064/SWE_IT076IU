import sqlite3


def insert(connection, category_id, category_name):
    """Add a new Category to the database.

    Args:
        connection (sqlite3.Connection)
        category_id (str)
        category_name (str)
    """

    if not category_id:
        raise TypeError("Argument 'category_id' is required!")
    if not category_name:
        raise TypeError("Argument 'category_name' is required!")

    cur = connection.cursor()
    cur.execute('''INSERT INTO ItemCategory (categoryID, categoryName) VALUES (?,?)''', (category_id, category_name))
    connection.commit()


def delete_by_id(connection, category_id):
    if not category_id:
        raise TypeError("Argument 'category_id' is required!")

    cur = connection.cursor()
    cur.execute('''DELETE FROM ItemCategory WHERE categoryID = ?''', (category_id,))
    connection.commit()


def delete_by_name(connection, category_name):
    if not category_name:
        raise TypeError("Argument 'category_name' is required!")

    cur = connection.cursor()
    cur.execute('''DELETE FROM ItemCategory WHERE categoryName = ?''', (category_name,))
    connection.commit()


def search_by_id(connection, category_id):
    if not category_id:
        raise TypeError("Argument 'category_id' is required!")

    cur = connection.cursor()
    return cur.execute('''SELECT * FROM ItemCategory WHERE categoryID LIKE ?''', ('%' + category_id + '%',))


def search_by_name(connection, category_name):
    if not category_name:
        raise TypeError("Argument 'category_name' is required!")

    cur = connection.cursor()
    return cur.execute('''SELECT * FROM ItemCategory WHERE categoryName LIKE ?''', ('%' + category_name + '%',))


def get_all(connection):
    return connection.cursor().execute('''SELECT * FROM ItemCategory''')