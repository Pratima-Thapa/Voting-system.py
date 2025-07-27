import hashlib
import json
import os
import uuid
import time

USERS_FILE = 'users.json'
VOTES_FILE = 'votes.json'
TOKENS_FILE = 'tokens.json'

# Predefined valid candidates/groups
CANDIDATES = ["Group A", "Group B", "Group C"]

def load_data(file):
    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump({}, f)
    with open(file, 'r') as f:
        return json.load(f)

def save_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

def hash_password(password):
    if password is None:
        return None
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    if not username or not password:
        return False, "Username or password cannot be empty."

    users = load_data(USERS_FILE)
    if username in users:
        return False, "User already exists."

    users[username] = {
        'password': hash_password(password),
        'voted': False
    }
    save_data(USERS_FILE, users)
    return True, "Registration successful."

def authenticate_user(username, password):
    users = load_data(USERS_FILE)
    if username not in users:
        return False, "User not found."
    if users[username]['password'] != hash_password(password):
        return False, "Incorrect password."
    return True, "Login successful."

def generate_token(username):
    tokens = load_data(TOKENS_FILE)
    token = str(uuid.uuid4())
    tokens[username] = {
        'token': token,
        'timestamp': time.time()
    }
    save_data(TOKENS_FILE, tokens)
    return token

def verify_token(username, token):
    tokens = load_data(TOKENS_FILE)
    if username not in tokens:
        return False
    if tokens[username]['token'] != token:
        return False
    del tokens[username]  # Prevent replay
    save_data(TOKENS_FILE, tokens)
    return True

def cast_vote(username, token, candidate):
    if candidate not in CANDIDATES:
        return False, f"Invalid candidate. Choose from {', '.join(CANDIDATES)}."

    users = load_data(USERS_FILE)
    votes = load_data(VOTES_FILE)

    if users[username]['voted']:
        return False, "You have already voted."

    if not verify_token(username, token):
        return False, "Invalid or expired token."

    if candidate not in votes:
        votes[candidate] = 0
    votes[candidate] += 1

    users[username]['voted'] = True
    save_data(USERS_FILE, users)
    save_data(VOTES_FILE, votes)
    return True, "Vote cast successfully!"

def get_results():
    return load_data(VOTES_FILE)
