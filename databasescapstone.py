import sqlite3

# connect to the ebookstore database
db = sqlite3.connect('ebookstore.db')
cursor = db.cursor()

# create new table called books
# use a try/except/finally clause to catch any exception in the code
try:
    cursor.execute('''
        CREATE TABLE books(book_id INTEGER PRIMARY KEY, Title TEXT, Author TEXT, Qty INTEGER)
    ''')
    db.commit()
except Exception as e:
    # Roll back any change if something goes wrong
    db.rollback()

books = [
    (3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
    (3002, 'Harry Potter and the Philosophers Stone', 'J.K. Rowling', 40),
    (3003, 'The Lion, the Witch and the Wardrobe', 'C. S. Lewis', 25),
    (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
    (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)
]

try:
    cursor.executemany('INSERT INTO books VALUES (?,?,?,?)', books)
    db.commit()
except Exception as e:
    # Roll back any change if something goes wrong
    db.rollback()

# Function to add a new book to the database
def add_book():
    book_id = int(input("Enter the book id: "))
    title = input("Enter the book title: ")
    author = input("Enter the book author: ")
    qty = int(input("Enter the quantity: "))
    
    cursor.execute("INSERT INTO books (ID, Title, Author, Quantity) VALUES (?, ?, ?, ?)",
              (book_id, title, author, qty))
    db.commit()
    print("Book added successfully!")

# Function to update book information
def update_book():
    book_id = int(input("Enter the book ID to update: "))
    
    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()
    
    if book:
        title = input("Enter the new title (current: {}): ".format(book[1]))
        author = input("Enter the new author (current: {}): ".format(book[2]))
        qty = int(input("Enter the new quantity (current: {}): ".format(book[3])))
        
        cursor.execute("UPDATE books SET title = ?, author = ?, qty = ? WHERE id = ?",
                  (title, author, qty, book_id))
        db.commit()
        print("Book updated successfully!")
    else:
        print("Book not found.")

# Function to delete a book from the database
def delete_book():
    book_id = int(input("Enter the book ID to delete: "))
    
    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()
    
    if book:
        confirm = input("Are you sure you want to delete '{}' by {}? (y/n): ".format(book[1], book[2]))
        
        if confirm.lower() == 'y':
            cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
            db.commit()
            print("Book deleted successfully!")
        else:
            print("Deletion canceled.")
    else:
        print("Book not found.")

# Function to search for a book by ID
def search_books():
    book_id = int(input("Enter the book ID: "))

    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()

    if book:
        print("Book found:")
        print("ID: {}, Title: {}, Author: {}, Qty: {}".format(book[0], book[1], book[2], book[3]))
    else:
        print("Book not found.")


# Main program loop
choice = None

while choice != '0':
    print("\nWhat would you like to do?")
    print("1. Enter book")
    print("2. Update book")
    print("3. Delete book")
    print("4. Search books")
    print("0. Exit")
    choice = input("Enter your choice (0-4): ")
    
    if choice == '1':
        add_book()
    elif choice == '2':
        update_book()
    elif choice == '3':
        delete_book()
    elif choice == '4':
        search_books()
    elif choice == '0':
        break
    else:
        print("Invalid choice. Please try again.")