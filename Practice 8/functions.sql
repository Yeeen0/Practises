-- functions.sql
-- Run this file in psql to create the functions:
-- psql -d phonebook_db -f functions.sql


-- ─────────────────────────────────────────
-- FUNCTION 1: Search by pattern
-- Returns all contacts where name OR phone
-- contains the search text.
-- Usage: SELECT * FROM search_contacts('Ali');
-- ─────────────────────────────────────────

CREATE OR REPLACE FUNCTION search_contacts(pattern TEXT)
RETURNS TABLE(id INT, first_name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
        SELECT p.id, p.first_name, p.phone
        FROM phonebook p
        WHERE p.first_name ILIKE '%' || pattern || '%'
           OR p.phone      ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;


-- ─────────────────────────────────────────
-- FUNCTION 2: Get contacts with pagination
-- page_size = how many contacts per page
-- page_num  = which page (starts from 1)
-- Usage: SELECT * FROM get_contacts_page(3, 1);
-- ─────────────────────────────────────────

CREATE OR REPLACE FUNCTION get_contacts_page(page_size INT, page_num INT)
RETURNS TABLE(id INT, first_name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
        SELECT p.id, p.first_name, p.phone
        FROM phonebook p
        ORDER BY p.id
        LIMIT page_size
        OFFSET (page_num - 1) * page_size;
END;
$$ LANGUAGE plpgsql;
