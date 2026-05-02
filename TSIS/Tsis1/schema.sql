CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

ALTER TABLE contacts
    ADD COLUMN email VARCHAR(100),
    ADD COLUMN birthday DATE,
    ADD COLUMN group_id INTEGER REFERENCES groups(id);

CREATE TABLE IF NOT EXISTS phones (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
    phone VARCHAR(20) NOT NULL,
    type VARCHAR(10) CHECK (type IN ('home', 'work', 'mobile'))
);

INSERT INTO phones (contact_id, phone, type)
SELECT id, phone, 'mobile' FROM contacts WHERE phone IS NOT NULL;

ALTER TABLE contacts DROP COLUMN phone;