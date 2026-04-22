# phonebook.py
# PhoneBook app — Practice 8
# Uses PostgreSQL functions and stored procedures

from connect import connect


def print_rows(rows):
    """Helper to nicely print a list of contacts."""
    if not rows:
        print("  (no results)")
        return
    print(f"\n  {'ID':<5} {'Name':<20} {'Phone'}")
    print("  " + "-" * 40)
    for row in rows:
        print(f"  {row[0]:<5} {row[1]:<20} {row[2]}")


# ─────────────────────────────────────────
# 1. Search by pattern (uses FUNCTION)
# ─────────────────────────────────────────

def search_contacts():
    """Search contacts by name or phone using the SQL function."""
    pattern = input("  Enter search text: ")

    conn = connect()
    cur = conn.cursor()

    # Call our SQL function with SELECT
    cur.execute("SELECT * FROM search_contacts(%s);", (pattern,))
    rows = cur.fetchall()

    cur.close()
    conn.close()

    print_rows(rows)


# ─────────────────────────────────────────
# 2. Upsert one contact (uses PROCEDURE)
#    Insert if new, update phone if exists
# ─────────────────────────────────────────

def upsert_contact():
    """Insert a new contact, or update their phone if name already exists."""
    name  = input("  Enter name  : ")
    phone = input("  Enter phone : ")

    conn = connect()
    cur = conn.cursor()

    # Call our SQL procedure with CALL
    cur.execute("CALL upsert_contact(%s, %s);", (name, phone))

    conn.commit()
    cur.close()
    conn.close()
    print(f"  [OK] Contact '{name}' saved!")


# ─────────────────────────────────────────
# 3. Bulk insert many contacts (uses PROCEDURE)
#    Validates phones, shows invalid ones
# ─────────────────────────────────────────

def bulk_insert():
    """Insert many contacts at once. Invalid phones will be shown."""
    print("  Enter contacts one by one.")
    print("  Type 'done' as name when finished.\n")

    names  = []
    phones = []

    while True:
        name = input("  Name  : ").strip()
        if name.lower() == "done":
            break
        phone = input("  Phone : ").strip()
        names.append(name)
        phones.append(phone)

    if not names:
        print("  No contacts entered.")
        return

    conn = connect()
    cur = conn.cursor()

    # Pass Python lists as PostgreSQL arrays
    cur.execute(
        "CALL bulk_insert_contacts(%s::VARCHAR[], %s::VARCHAR[]);",
        (names, phones)
    )
    conn.commit()

    # Read invalid contacts from the temp table the procedure created
    cur.execute("SELECT first_name, phone, reason FROM invalid_contacts;")
    invalid = cur.fetchall()

    cur.close()
    conn.close()

    print(f"\n  [OK] Bulk insert done!")

    if invalid:
        print("\n  The following contacts were SKIPPED (invalid phone):")
        for row in invalid:
            print(f"    Name: {row[0]}, Phone: {row[1]}, Reason: {row[2]}")
    else:
        print("  All contacts were valid!")


# ─────────────────────────────────────────
# 4. Paginated view (uses FUNCTION)
# ─────────────────────────────────────────

def view_with_pagination():
    """Show contacts page by page."""
    size = input("  How many contacts per page? [default 3]: ").strip()
    size = int(size) if size.isdigit() else 3

    page = 1
    while True:
        conn = connect()
        cur = conn.cursor()

        cur.execute("SELECT * FROM get_contacts_page(%s, %s);", (size, page))
        rows = cur.fetchall()

        cur.close()
        conn.close()

        print(f"\n  --- Page {page} ---")
        print_rows(rows)

        if len(rows) < size:
            print("\n  (end of contacts)")
            break

        go = input("\n  Next page? [y/n]: ").strip().lower()
        if go != "y":
            break
        page += 1


# ─────────────────────────────────────────
# 5. Delete contact (uses PROCEDURE)
# ─────────────────────────────────────────

def delete_contact():
    """Delete a contact by name or phone using the SQL procedure."""
    print("  Delete by: [1] Name  [2] Phone")
    choice = input("  Choice: ").strip()

    conn = connect()
    cur = conn.cursor()

    if choice == "1":
        name = input("  Enter name to delete: ")
        cur.execute("CALL delete_contact('name', %s, '');", (name,))
        print(f"  [OK] Deleted contact with name '{name}'")

    elif choice == "2":
        phone = input("  Enter phone to delete: ")
        cur.execute("CALL delete_contact('phone', '', %s);", (phone,))
        print(f"  [OK] Deleted contact with phone '{phone}'")

    else:
        print("  Invalid choice.")
        cur.close()
        conn.close()
        return

    conn.commit()
    cur.close()
    conn.close()


# ─────────────────────────────────────────
# MAIN MENU
# ─────────────────────────────────────────

def main():
    while True:
        print("\n--- PhoneBook Menu (Practice 8) ---")
        print("1. Search contacts by name or phone")
        print("2. Add or update one contact")
        print("3. Bulk insert many contacts")
        print("4. View contacts (page by page)")
        print("5. Delete a contact")
        print("0. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            search_contacts()
        elif choice == "2":
            upsert_contact()
        elif choice == "3":
            bulk_insert()
        elif choice == "4":
            view_with_pagination()
        elif choice == "5":
            delete_contact()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Please enter a number from 0 to 5.")


if __name__ == "__main__":
    main()
