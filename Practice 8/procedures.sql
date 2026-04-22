-- procedures.sql
-- Run this file in psql to create the procedures:
-- psql -d phonebook_db -f procedures.sql


-- ─────────────────────────────────────────
-- PROCEDURE 1: Upsert (insert OR update)
-- If name already exists → update their phone
-- If name is new → insert them
-- Usage: CALL upsert_contact('Alice', '+77011111111');
-- ─────────────────────────────────────────

CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = p_name) THEN
        -- Name already exists, update their phone
        UPDATE phonebook SET phone = p_phone WHERE first_name = p_name;
    ELSE
        -- New contact, insert them
        INSERT INTO phonebook (first_name, phone) VALUES (p_name, p_phone);
    END IF;
END;
$$;


-- ─────────────────────────────────────────
-- PROCEDURE 2: Bulk insert with validation
-- Takes arrays of names and phones.
-- Skips invalid phones (must start with + and be 10+ chars).
-- Creates a temp table with invalid entries so Python can read them.
-- Usage: CALL bulk_insert_contacts(ARRAY['Ali','Bo'], ARRAY['+7701...','abc']);
-- ─────────────────────────────────────────

CREATE OR REPLACE PROCEDURE bulk_insert_contacts(
    p_names  VARCHAR[],
    p_phones VARCHAR[]
)
LANGUAGE plpgsql AS $$
DECLARE
    i         INT;
    v_name    VARCHAR;
    v_phone   VARCHAR;
BEGIN
    -- Create a temp table to store invalid rows (dropped after session ends)
    DROP TABLE IF EXISTS invalid_contacts;
    CREATE TEMP TABLE invalid_contacts (
        first_name VARCHAR,
        phone      VARCHAR,
        reason     VARCHAR
    );

    -- Loop through each name/phone pair
    FOR i IN 1 .. array_length(p_names, 1) LOOP
        v_name  := p_names[i];
        v_phone := p_phones[i];

        -- Validate: phone must start with '+' and be at least 10 characters
        IF v_phone NOT LIKE '+%' OR length(v_phone) < 10 THEN
            -- Invalid phone → save to temp table, skip insert
            INSERT INTO invalid_contacts VALUES (v_name, v_phone, 'Invalid phone format');
        ELSE
            -- Valid → upsert (insert or update)
            CALL upsert_contact(v_name, v_phone);
        END IF;
    END LOOP;
END;
$$;


-- ─────────────────────────────────────────
-- PROCEDURE 3: Delete by name or phone
-- Usage: CALL delete_contact('name', 'Alice', '');
--        CALL delete_contact('phone', '', '+77011234567');
-- ─────────────────────────────────────────

CREATE OR REPLACE PROCEDURE delete_contact(
    p_by    VARCHAR,   -- 'name' or 'phone'
    p_name  VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    IF p_by = 'name' THEN
        DELETE FROM phonebook WHERE first_name = p_name;
    ELSIF p_by = 'phone' THEN
        DELETE FROM phonebook WHERE phone = p_phone;
    END IF;
END;
$$;
