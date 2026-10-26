CREATE TABLE notes(
    id INTEGER PRIMARY KEY,
    account_id TEXT NOT NULL REFERENCES accounts(account_id),
    content TEXT NOT NULL,
    created_at TEXT NOT NULL
);