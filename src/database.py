#!/usr/bin/env python3

import sqlite3
import sys
import os
import argparse
import bcrypt
import uuid
import account
from pathlib import Path
import util

# Constants
DUMMY_HASH = b"$2b$12$Kb7e5zCPlzvHg9ZpRJK7e.YBZsWZnqj/SG4eS2A3Yk5C23w6a7WPS"  # pre-generated

# Load database path
DATABASE_PATH = os.getenv('DATABASE_PATH')
USER_PATH     = os.getenv('USER_PATH')
if not DATABASE_PATH:
    util.logger.error("DATABASE_PATH environment variable must be set. Either modify the default.nix file or manually set it.")
    sys.exit(1)
if not USER_PATH:
    util.logger.error("USER_PATH environment variable must be set.")
    sys.exit(1)
USER_PATH = Path(USER_PATH)
DATABASE_PATH = Path(DATABASE_PATH)

def regenerate_database(location: Path):
    """Create or reset the database schema."""
    con = sqlite3.connect(str(location))
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Users(
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            hash BLOB NOT NULL
        )
    """)
    con.commit()
    con.close()
    util.logger.info("Database schema regenerated.")

def create_account(username: str, password: str):
    """Create a new user account with a hashed password."""
    con = sqlite3.connect(str(DATABASE_PATH))
    cur = con.cursor()
    try:
        with con:
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            uid = str(uuid.uuid4())
            cur.execute("""
                INSERT INTO Users (id, username, hash)
                VALUES (?, ?, ?)
            """, (uid, username, hashed))
        util.logger.info(f"Account created for user '{username}' with ID {uid}.")
    except sqlite3.IntegrityError:
        util.logger.error(f"Username '{username}' already exists.")
        sys.exit(1)
    except Exception as e:
        util.logger.exception(f"Error creating account: {e}")
        sys.exit(1)
    finally:
        con.close()

def authenticate_account(username: str, password: str) -> account.Account:
    """Authenticate a user using bcrypt with timing attack mitigation."""
    con = sqlite3.connect(str(DATABASE_PATH))
    con.row_factory = sqlite3.Row  # This enables dict-like access.
    cur = con.cursor()
    try:
        res = cur.execute("SELECT * FROM Users WHERE username=?", (username,))
        row = res.fetchone()
        if row is None:
            bcrypt.checkpw(password.encode('utf-8'), DUMMY_HASH)  # timing resistance
            return False
        if bcrypt.checkpw(password.encode('utf-8'), row['hash']):
            util.logger.info("Authentication successful.")
            act = account.Account(username, row['id'])
            # util.pdb.set_trace()
            act.load_json()
            return act
        return False
    except Exception as e:
        util.logger.exception(f"Authentication error for user '{username}': {e}")
        return False
    finally:
        con.close()

def fetch_user_data(uid):
    FILEPATH = f'{USER_PATH}/{uid}'
    if not os.path.exists(FILEPATH):
        os.mkdir(FILEPATH)
    # TODO 1) Create Account file
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='account.py',
        description='Manage the database and authentication of accounts',
        epilog='Use one flag at a time. Authentication and creation cannot be combined.'
    )
    parser.add_argument('-r', '--regenerate', action='store_true', help='Regenerate the database')
    parser.add_argument('-c', '--create', nargs=2, metavar=('USERNAME', 'PASSWORD'), help='Create a new user')
    parser.add_argument('-a', '--authenticate', nargs=2, metavar=('USERNAME', 'PASSWORD'), help='Authenticate a user')

    args = parser.parse_args()

    if args.regenerate:
        regenerate_database(DATABASE_PATH)
        sys.exit(0)

    if not DATABASE_PATH.exists():
        util.logger.error(f"Database file not found at {DATABASE_PATH}")
        util.logger.error("Regenerate with -r or check DATABASE_PATH configuration")
        sys.exit(1)

    if args.create and args.authenticate:
        util.logger.error("Do not authenticate and create at the same time.")
        sys.exit(1)

    if args.create:
        username, password = args.create
        create_account(username, password)

    if args.authenticate:
        username, password = args.authenticate
        act = authenticate_account(username, password)
        if act:
            print(act.inventory)
        else:
            print(act)
            util.logger.error("Authentication failed.")
