import psycopg2
import json
from config import load_config

def get_connection():
    params = load_config()
    return psycopg2.connect(**params)

def execute_query(query, params=(), fetch=False):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                if fetch:
                    return cur.fetchall()
                conn.commit()
    except Exception as e:
        print(f"Ошибка БД: {e}")
        return []

def advanced_search():
    print("\n1. Filter by group\n2. Search by email\n3. Sort results\n4. Search pattern")
    choice = input("Choice: ")
    
    query = "SELECT c.name, c.email, c.birthday, g.name FROM contacts c LEFT JOIN groups g ON c.group_id = g.id"
    params = ()
    
    if choice == '1':
        grp = input("Group name (e.g. Family, Work): ")
        query += " WHERE g.name = %s"
        params = (grp,)
        rows = execute_query(query, params, True)
        for r in rows: print(r)
    elif choice == '2':
        em = input("Email partial (e.g. gmail): ")
        query += " WHERE c.email ILIKE %s"
        params = ('%' + em + '%',)
        rows = execute_query(query, params, True)
        for r in rows: print(r)
    elif choice == '3':
        sort_by = input("Sort by (name/birthday/id): ")
        if sort_by in ['name', 'birthday', 'id']:
            query += f" ORDER BY c.{sort_by}"
        rows = execute_query(query, params, True)
        for r in rows: print(r)
    elif choice == '4':
        pat = input("Pattern: ")
        rows = execute_query("SELECT * FROM search_contacts(%s);", (pat,), True)
        for r in rows: print(r)

def get_paginated():
    try:
        limit = int(input("Limit per page: "))
    except ValueError:
        print("Invalid number!")
        return
        
    offset = 0
    while True:
        print(f"\n--- Page Offset: {offset} ---")
        rows = execute_query("SELECT * FROM get_contacts_paginated(%s, %s);", (limit, offset), True)
        if not rows:
            print("No more contacts.")
        else:
            for row in rows:
                print(row)
                
        action = input("\nType 'next', 'prev', or 'quit': ").strip().lower()
        if action == 'next':
            offset += limit
        elif action == 'prev':
            offset = max(0, offset - limit)
        elif action == 'quit':
            break

def export_json():
    filename = input("Filename to save (e.g. contacts.json): ")
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT c.name, c.email, TO_CHAR(c.birthday, 'YYYY-MM-DD'), g.name,
                           COALESCE(json_agg(json_build_object('phone', p.phone, 'type', p.type)) FILTER (WHERE p.phone IS NOT NULL), '[]')
                    FROM contacts c
                    LEFT JOIN groups g ON c.group_id = g.id
                    LEFT JOIN phones p ON c.id = p.contact_id
                    GROUP BY c.id, g.name
                """)
                rows = cur.fetchall()
                data = [{"name": r[0], "email": r[1], "birthday": r[2], "group": r[3], "phones": r[4]} for r in rows]
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print("Export successful!")
    except Exception as e:
        print(f"Export error: {e}")

def import_json():
    filename = input("Filename to load (e.g. contacts.json): ")
    mode = input("On duplicate (skip/overwrite): ").strip().lower()
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        with get_connection() as conn:
            with conn.cursor() as cur:
                for item in data:
                    cur.execute("SELECT id FROM contacts WHERE name = %s", (item['name'],))
                    res = cur.fetchone()
                    if res and mode == 'skip': continue
                    
                    group_id = None
                    if item.get('group'):
                        cur.execute("INSERT INTO groups (name) VALUES (%s) ON CONFLICT DO NOTHING", (item['group'],))
                        cur.execute("SELECT id FROM groups WHERE name = %s", (item['group'],))
                        group_id = cur.fetchone()[0]
                        
                    if res and mode == 'overwrite':
                        cur.execute("UPDATE contacts SET email=%s, birthday=%s, group_id=%s WHERE id=%s", 
                                    (item.get('email'), item.get('birthday'), group_id, res[0]))
                        cur.execute("DELETE FROM phones WHERE contact_id=%s", (res[0],))
                        c_id = res[0]
                    elif not res:
                        cur.execute("INSERT INTO contacts (name, email, birthday, group_id) VALUES (%s, %s, %s, %s) RETURNING id",
                                    (item['name'], item.get('email'), item.get('birthday'), group_id))
                        c_id = cur.fetchone()[0]
                    
                    for p in item.get('phones', []):
                        cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                                    (c_id, p['phone'], p['type']))
                conn.commit()
        print("Import successful!")
    except Exception as e:
        print(f"Import error: {e}")

def call_procedures():
    print("\n1. Add Phone to existing contact\n2. Move contact to Group")
    choice = input("Choice: ")
    if choice == '1':
        name = input("Contact name: ")
        phone = input("Phone: ")
        ptype = input("Type (home/work/mobile): ")
        execute_query("CALL add_phone(%s, %s, %s);", (name, phone, ptype))
        print("Done!")
    elif choice == '2':
        name = input("Contact name: ")
        gname = input("Group name: ")
        execute_query("CALL move_to_group(%s, %s);", (name, gname))
        print("Done!")

def main_menu():
    while True:
        print("\n=== PHONEBOOK TSIS 1 ===")
        print("1. Advanced Search / Filter")
        print("2. Paginated Query (Next/Prev)")
        print("3. Export to JSON")
        print("4. Import from JSON")
        print("5. Use Procedures (Add Phone / Move Group)")
        print("0. Exit")
        choice = input("Choice: ")
        
        if choice == '1': advanced_search()
        elif choice == '2': get_paginated()
        elif choice == '3': export_json()
        elif choice == '4': import_json()
        elif choice == '5': call_procedures()
        elif choice == '0': break

if __name__ == '__main__':
    main_menu()