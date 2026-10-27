"""Teacher-prepared fictional data for the first database lessons."""

from pathlib import Path
import sqlite3


PROJECT_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_DIR / "data" / "dashboard.db"


def prepare_demo_database():
    if DATABASE_PATH.exists():
        print(f"Existing database preserved: {DATABASE_PATH}")
        return

    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    try:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript("""
            CREATE TABLE accounts (
                account_id TEXT PRIMARY KEY,
                account_type TEXT NOT NULL,
                name TEXT NOT NULL,
                base_currency TEXT NOT NULL,
                source TEXT NOT NULL
            );

            CREATE TABLE snapshots (
                snapshot_id INTEGER PRIMARY KEY,
                account_id TEXT NOT NULL REFERENCES accounts(account_id),
                as_of TEXT NOT NULL,
                received_at TEXT NOT NULL,
                netvalue TEXT NOT NULL,
                note TEXT,
                UNIQUE (account_id, as_of)
            );

            CREATE TABLE holdings (
                snapshot_id INTEGER NOT NULL REFERENCES snapshots(snapshot_id),
                symbol TEXT NOT NULL,
                quantity TEXT NOT NULL,
                PRIMARY KEY (snapshot_id, symbol)
            );

            -- Temporary legacy table while notes move into snapshots.
            CREATE TABLE notes (
                id INTEGER PRIMARY KEY,
                account_id TEXT NOT NULL REFERENCES accounts(account_id),
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                snapshot_id INTEGER REFERENCES snapshots(snapshot_id)
            );

            CREATE UNIQUE INDEX idx_notes_snapshot_id ON notes(snapshot_id);
        """)
        with connection:
            connection.executemany(
                "INSERT INTO accounts VALUES (?, ?, ?, ?, ?)",
                [
                    ("demo_paper", "paper", "paper_account", "usd", "demo"),
                    ("demo_live", "live", "live_account", "usd", "demo"),
                ],
            )
            connection.executemany(
                "INSERT INTO snapshots (snapshot_id, account_id, as_of, received_at, netvalue) VALUES (?, ?, ?, ?, ?)",
                [
                    (1, "demo_paper", "2026-10-20T20:00:00+08:00",
                     "2026-10-20T20:01:00+08:00", "15000.00"),
                    (2, "demo_paper", "2026-10-21T20:00:00+08:00",
                     "2026-10-21T20:01:00+08:00", "15200.00"),
                    (3, "demo_live", "2026-10-20T20:00:00+08:00",
                     "2026-10-20T20:01:00+08:00", "14000.00"),
                ],
            )
            connection.executemany(
                "INSERT INTO holdings VALUES (?, ?, ?)",
                [(1, "TSM", "2.5"), (2, "TSM", "2.5"), (3, "GOOGL", "3")],
            )
        print(f"Created fictional demo database: {DATABASE_PATH}")
    finally:
        connection.close()


if __name__ == "__main__":
    prepare_demo_database()
