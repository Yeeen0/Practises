# phonebook.py
# PhoneBook app using Python + PostgreSQL
# Run: python phonebook.py

import csv
import psycopg2
import config  # our config.py file


# ─────────────────────────────────────────
# STEP 1: Connect to the database
# ─────────────────────────────────────────

def connect():
    """Open a connection to PostgreSQL and return it."""
    conn = psycopg2.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASS
    )
    return conn


# ─────────────────────────────────────────
# STEP 2: Create the table (only once)
# ─────────────────────────────────────────

def create_table():
    """Create the phonebook table if it does not exist yet."""
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id         SERIAL PRIMARY KEY,
            first_name VARCHAR(100),
            phone      VARCHAR(20) UNIQUE
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Table is ready!")


# ─────────────────────────────────────────
# INSERT from CSV file
# ─────────────────────────────────────────

def insert_from_csv():
    """Read contacts.csv and add all contacts to the database."""
    conn = connect()
    cur = conn.cursor()

    with open("contacts.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)  # reads header row automatically
        for row in reader:
            name  = row["first_name"]
            phone = row["phone"]

            # ON CONFLICT DO NOTHING = skip if phone already exists
            cur.execute(
                "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING;",
                (name, phone)
            )

    conn.commit()
    cur.close()
    conn.close()
    print("Contacts imported from CSV!")


# ─────────────────────────────────────────
# INSERT from keyboard
# ─────────────────────────────────────────

def insert_from_console():
    """Ask the user to type a name and phone, then save it."""
    name  = input("Enter first name: ")
    phone = input("Enter phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING;",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()
    print(f"Contact '{name}' added!")


# ─────────────────────────────────────────
# SHOW all contacts
# ─────────────────────────────────────────

def show_all():
    """Print all contacts in the database."""
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT id, first_name, phone FROM phonebook ORDER BY id;")
    rows = cur.fetchall()  # get all results as a list

    cur.close()
    conn.close()

    if rows:
        print(f"\n{'ID':<5} {'Name':<20} {'Phone'}")
        print("-" * 40)
        for row in rows:
            print(f"{row[0]:<5} {row[1]:<20} {row[2]}")
    else:
        print("No contacts found.")


# ─────────────────────────────────────────
# SEARCH by name
# ─────────────────────────────────────────

def search_by_name():
    """Find contacts whose name contains what the user types."""
    name = input("Enter name to search: ")

    conn = connect()
    cur = conn.cursor()

    # ILIKE = case-insensitive search, % means "anything"
    cur.execute(
        "SELECT id, first_name, phone FROM phonebook WHERE first_name ILIKE %s;",
        ("%" + name + "%",)
    )
    rows = cur.fetchall()

    cur.close()
    conn.close()

    if rows:
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")
    else:
        print("No contacts found.")


# ─────────────────────────────────────────
# SEARCH by phone prefix
# ─────────────────────────────────────────

def search_by_phone():
    """Find contacts whose phone starts with what the user types."""
    prefix = input("Enter phone prefix (e.g. +7701): ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, first_name, phone FROM phonebook WHERE phone LIKE %s;",
        (prefix + "%",)
    )
    rows = cur.fetchall()

    cur.close()
    conn.close()

    if rows:
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")
    else:
        print("No contacts found.")


# ─────────────────────────────────────────
# UPDATE a contact
# ─────────────────────────────────────────

def update_contact():
    """Change a contact's name or phone number."""
    print("What do you want to update?")
    print("1 - Change name")
    print("2 - Change phone")
    choice = input("Your choice: ")

    conn = connect()
    cur = conn.cursor()

    if choice == "1":
        old_name = input("Enter current name: ")
        new_name = input("Enter new name: ")
        cur.execute(
            "UPDATE phonebook SET first_name = %s WHERE first_name = %s;",
            (new_name, old_name)
        )

    elif choice == "2":
        old_phone = input("Enter current phone: ")
        new_phone = input("Enter new phone: ")
        cur.execute(
            "UPDATE phonebook SET phone = %s WHERE phone = %s;",
            (new_phone, old_phone)
        )

    else:
        print("Invalid choice.")
        cur.close()
        conn.close()
        return

    conn.commit()
    cur.close()
    conn.close()
    print("Contact updated!")


# ─────────────────────────────────────────
# DELETE a contact
# ─────────────────────────────────────────

def delete_contact():
    """Remove a contact from the database."""
    print("Delete by:")
    print("1 - Name")
    print("2 - Phone")
    choice = input("Your choice: ")

    conn = connect()
    cur = conn.cursor()

    if choice == "1":
        name = input("Enter name to delete: ")
        cur.execute("DELETE FROM phonebook WHERE first_name = %s;", (name,))

    elif choice == "2":
        phone = input("Enter phone to delete: ")
        cur.execute("DELETE FROM phonebook WHERE phone = %s;", (phone,))

    else:
        print("Invalid choice.")
        cur.close()
        conn.close()
        return

    conn.commit()
    cur.close()
    conn.close()
    print("Contact deleted!")


# ─────────────────────────────────────────
# MAIN MENU
# ─────────────────────────────────────────

def main():
    # Create the table when the program starts
    create_table()

    while True:
        print("\n--- PhoneBook Menu ---")
        print("1. Import from CSV")
        print("2. Add contact")
        print("3. Show all contacts")
        print("4. Search by name")
        print("5. Search by phone prefix")
        print("6. Update contact")
        print("7. Delete contact")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            insert_from_csv()
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            show_all()
        elif choice == "4":
            search_by_name()
        elif choice == "5":
            search_by_phone()
        elif choice == "6":
            update_contact()
        elif choice == "7":
            delete_contact()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Please enter a number from 0 to 7.")


# This line means: run main() only when we run this file directly
if __name__ == "__main__":
    main()
