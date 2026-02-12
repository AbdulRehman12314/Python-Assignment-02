import json
import os
import random
import hashlib
from datetime import datetime

ADMIN_PASSWORD = "Abdul-Rehman 786 Owner"   
USERS_FILE = "users_data.json"
LIBRARY_FILE = "library_data.json"

# ==========================================================
# FILE HANDLING
# ==========================================================

def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)
    with open(USERS_FILE, "r") as f:
        users = json.load(f)
   
    for user_data in users.values():
        user_data.setdefault("highest_score", 0)
        user_data.setdefault("total_points", 0)
        user_data.setdefault("total_games", 0)
        user_data.setdefault("total_wins", 0)
        user_data.setdefault("history", [])
    return users

def save_users(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def safe_int_input(message):
    try:
        return int(input(message))
    except:
        print("Invalid input! Numbers only.")
        return None

# ==========================================================
# ENIGMA TRANSLATOR
# ==========================================================

def encode(text, shift=3):
    result = ""
    for char in text:
        if char.isalpha():
            base = 65 if char.isupper() else 97
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

def enigma_menu():
    while True:
        print("\n1. ENCODE\n2. DECODE\n3. Back")
        c = input("Choose any one option : ")

        if c == "1":
            print("Encoded:", encode(input("Enter some text to Encode: ")))
        elif c == "2":
            print("Decoded:", encode(input("Enter some text to decode: "), -3))
        elif c == "3":
            break

# ==========================================================
# LIBRARY SYSTEM
# ==========================================================

def library_menu():
    books = []
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as f:
            books = json.load(f)

    while True:
        print("\n1.Add Book\n2.Delete Book\n3.Search Book\n4.Show All\n5.Back")
        c = input("Choose: ")

        if c == "1":
            b = input("Enter Book Name: ")
            if b in books:
                print("Book already exists!")
            else:
                books.append(b)
                print("Book Added!")

        elif c == "2":
            b = input("Enter Book Name: ")
            if b in books:
                books.remove(b)
                print("Deleted!")
            else:
                print("Not Found!")

        elif c == "3":
            b = input("Search Book: ")
            print("Found!" if b in books else "Not Found!")

        elif c == "4":
            print("\nTotal Books:", len(books))
            for book in books:
                print("-", book)

        elif c == "5":
            break

        with open(LIBRARY_FILE, "w") as f:
            json.dump(books, f, indent=4)

# ==========================================================
# ACCOUNT SYSTEM
# ==========================================================

def create_account():
    users = load_users()
    u = input("Enter Username: ")

    if u in users:
        print("Username already exists!")
        return

    p = input("Enter Password (min 4 chars): ")
    if len(p) < 4:
        print("Password too short!")
        return

    users[u] = {
        "password": hash_password(p),
        "highest_score": 0,
        "total_points": 0,
        "total_games": 0,
        "total_wins": 0,
        "history": []
    }

    save_users(users)
    print("Account Created Successfully!")
    user_dashboard(u)

def login():
    users = load_users()
    u = input("Username: ")
    p = input("Password: ")

    if u in users and users[u]["password"] == hash_password(p):
        print("Login Successful!")
        user_dashboard(u)
    elif u in users:
        print("Wrong password!")
    else:
        print("Account does not exist!")

def delete_account():
    users = load_users()
    u = input("Username: ")
    p = input("Password: ")

    if u in users and users[u]["password"] == hash_password(p):
        confirm = input("Type YES to delete permanently: ")
        if confirm == "YES":
            del users[u]
            save_users(users)
            print("Account Deleted.")
    else:
        print("Invalid credentials!")

# ==========================================================
# ADMIN PANEL
# ==========================================================

def admin_panel():
    password = input("Enter Admin Password: ")

    if password != ADMIN_PASSWORD:
        print("Access Denied!")
        return

    while True:
        print("\n===== ADMIN CONTROL PANEL =====")
        print("1.View All Users")
        print("2.Delete User")
        print("3.Reset User Score")
        print("4.System Statistics")
        print("5.Back")

        choice = input("Choose: ")

        users = load_users()

        if choice == "1":
            if not users:
                print("No users found.")
            else:
                print("\nRegistered Users:")
                for username in users:
                    print("-", username)

        elif choice == "2":
            u = input("Enter username to delete: ")
            if u in users:
                confirm = input("Type YES to confirm deletion: ")
                if confirm == "YES":
                    del users[u]
                    save_users(users)
                    print("User deleted successfully.")
            else:
                print("User not found.")

        elif choice == "3":
            u = input("Enter username to reset score: ")
            if u in users:
                users[u]["highest_score"] = 0
                users[u]["total_points"] = 0
                users[u]["total_games"] = 0
                users[u]["total_wins"] = 0
                users[u]["history"] = []
                save_users(users)
                print("User score reset successfully.")
            else:
                print("User not found.")

        elif choice == "4":
            total_users = len(users)
            total_games = sum(u["total_games"] for u in users.values())
            total_points = sum(u["total_points"] for u in users.values())

            print("\n===== SYSTEM STATS =====")
            print("Total Registered Users:", total_users)
            print("Total Games Played:", total_games)
            print("Total Points Earned (All Users):", total_points)

        elif choice == "5":
            break

# ==========================================================
# PROFILE
# ==========================================================

def view_profile(username):
    users = load_users()
    user = users[username]

    win_ratio = 0
    if user["total_games"] > 0:
        win_ratio = (user["total_wins"] / user["total_games"]) * 100

    print("\n===== PROFILE =====")
    print("Username:", username)
    print("Highest Score:", user["highest_score"])
    print("Total Points:", user["total_points"])
    print("Total Games Played:", user["total_games"])
    print("Total Wins:", user["total_wins"])
    print("Win Ratio: {:.2f}%".format(win_ratio))
    print("\nRecent History:")
    for h in user["history"][-5:]:
        print(f"{h['date']} | {h['game']} | {h['result']} | +{h['points']}")

# ==========================================================
# LEADERBOARD
# ==========================================================

def show_leaderboard():
    users = load_users()
    sorted_users = sorted(users.items(),
                          key=lambda x: x[1]["total_points"],
                          reverse=True)

    print("\n===== TOP 5 LEADERBOARD =====")
    for i, (u, data) in enumerate(sorted_users[:5], 1):
        print(f"{i}. {u} - {data['total_points']} pts")

# ==========================================================
# GAME ENGINE
# ==========================================================

def record_game(username, game_name, points):
    users = load_users()
    user = users[username]

    result = "Win" if points > 0 else "Loss"

    user["total_games"] += 1
    user["total_points"] += points
    if points > 0:
        user["total_wins"] += 1

    if user["total_points"] > user["highest_score"]:
        user["highest_score"] = user["total_points"]

    user["history"].append({
        "game": game_name,
        "result": result,
        "points": points,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    })

    save_users(users)

# ---------------- GAMES ----------------

def game_rps():
    choices = ["rock", "paper", "scissors"]
    while True:
        user = input("Choose rock/paper/scissors: ").lower()
        if user in choices:
            break
        print("Invalid choice!")

    comp = random.choice(choices)
    print("Computer:", comp)

    if user == comp:
        return 5
    elif (user == "rock" and comp == "scissors") or \
         (user == "paper" and comp == "rock") or \
         (user == "scissors" and comp == "paper"):
        return 10
    return 0

def game_number():
    secret = random.randint(1, 10)
    for attempt in range(3):
        guess = safe_int_input("Guess number (1-10): ")
        if guess is None:
            continue
        if guess == secret:
            return 20
        elif guess < secret:
            print("Too Low!")
        else:
            print("Too High!")
    print("Number was:", secret)
    return 0

def game_quiz():
    a = random.randint(10,200)
    b = random.randint(10,200)
    ans = a + b
    user = safe_int_input(f"What is {a} + {b}? ")
    return 15 if user == ans else 0

def game_memory(): 
  number = str(random.randint(100,999)) 
  print("Memorize:", number) 
  input("Press Enter...") 
  print("\n"*30) 
  guess = input("Enter number: ") 
  return 25 if guess == number else 0 

def game_reverse():
    words = ["python","developer","challenge","project","gaming"]
    word = random.choice(words)
    print("Reverse this word:", word)
    guess = input("Enter reversed: ")
    return 15 if guess == word[::-1] else 0


# ==========================================================
# GAME MENU
# ==========================================================

def start_games(username=None):
    while True:
        print("\n1.Rock Paper Scissors")
        print("2.Number Guess")
        print("3.Math Challenge")
        print("4.Memory Game")
        print("5.Word Reverse")
        print("6.Leaderboard")
        print("7.Back")

        c = input("Choose any one option: ")

        if c == "1":
            pts = game_rps()
            name = "RPS"
        elif c == "2":
            pts = game_number()
            name = "Number Guess"
        elif c == "3":
            pts = game_quiz()
            name = "Math Quiz"
        elif c == "4":
            pts = game_memory()
            name = "Memory"
        elif c == "5":
            pts = game_reverse()
            name = "Reverse"
        elif c == "6":
            show_leaderboard()
            continue
        elif c == "7":
            break
        else:
            continue

        print("Points Gained:", pts)

        if username:
            record_game(username, name, pts)

# ==========================================================
# DASHBOARD
# ==========================================================

def user_dashboard(username):
    while True:
        print("\n1.View Profile\n2.Play Games\n3.Logout")
        c = input("Choose: ")

        if c == "1":
            view_profile(username)
        elif c == "2":
            start_games(username)
        elif c == "3":
            break

# ==========================================================
# GIANT HUB
# ==========================================================

def giant_hub():
    while True:
        print("\n1.Create Account")
        print("2.Login")
        print("3.Delete Account")
        print("4.Guest Mode")
        print("5.Admin Panel")
        print("6.Back")

        c = input("Choose any one option: ")

        if c == "1":
            create_account()
        elif c == "2":
            login()
        elif c == "3":
            delete_account()
        elif c == "4":
            start_games()
        elif c == "5":
            admin_panel()
        elif c == "6":
            break


# ==========================================================
# MAIN MENU
# ==========================================================

def main():
    while True:
        print("\n===== 🏆 NEXUSARC INTERACTIVE SUITE =====")
        print("1.Enigma Translator")
        print("2.Library Management")
        print("3.Game Hub")
        print("4.Exit")

        c = input("Choose any one option: ")

        if c == "1":
            enigma_menu()
        elif c == "2":
            library_menu()
        elif c == "3":
            giant_hub()
        elif c == "4":
            break

if __name__ == "__main__":
    main()
